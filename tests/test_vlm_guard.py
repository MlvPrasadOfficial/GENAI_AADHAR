"""Tests for pipeline/vlm_guard.py — uses mocked model, no GPU needed."""

from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from pipeline.vlm_guard import VLMGuard, VLMVerdict


@pytest.fixture
def guard(sample_config):
    return VLMGuard(sample_config)


@pytest.fixture
def face_crops():
    """Two dummy 112x112 BGR face crops."""
    crop1 = np.random.randint(0, 255, (112, 112, 3), dtype=np.uint8)
    crop2 = np.random.randint(0, 255, (112, 112, 3), dtype=np.uint8)
    return crop1, crop2


class TestVLMGuardDisabled:
    def test_disabled_returns_none(self, sample_config, face_crops):
        sample_config["vlm_guard"]["enabled"] = False
        guard = VLMGuard(sample_config)
        verdict = guard.verify(*face_crops, cosine_score=0.5)
        assert verdict.same_person is None
        assert verdict.reasoning == "VLM guard disabled"


class TestVLMGuardParsing:
    def test_valid_json_response(self, guard):
        raw = '{"same_person": true, "confidence": "high", "reasoning": "Match", "quality_issues": null}'
        verdict = guard._parse_response(raw)
        assert verdict.same_person is True
        assert verdict.confidence == "high"
        assert verdict.reasoning == "Match"

    def test_json_with_code_fence(self, guard):
        raw = '```json\n{"same_person": false, "confidence": "low", "reasoning": "No match", "quality_issues": "blurry"}\n```'
        verdict = guard._parse_response(raw)
        assert verdict.same_person is False
        assert verdict.confidence == "low"

    def test_regex_fallback(self, guard):
        raw = 'Based on my analysis, {"same_person": true, "confidence": "medium"} and more text'
        verdict = guard._parse_response(raw)
        assert verdict.same_person is True
        assert verdict.confidence == "medium"

    def test_unparseable_returns_none(self, guard):
        raw = "I cannot determine if these faces match."
        verdict = guard._parse_response(raw)
        assert verdict.same_person is None

    def test_empty_response(self, guard):
        verdict = guard._parse_response("")
        assert verdict.same_person is None

    def test_string_true_handled(self, guard):
        raw = '{"same_person": "true", "confidence": "high", "reasoning": "Match", "quality_issues": null}'
        verdict = guard._parse_response(raw)
        assert verdict.same_person is True

    def test_string_false_handled(self, guard):
        raw = '{"same_person": "false", "confidence": "low", "reasoning": "No", "quality_issues": null}'
        verdict = guard._parse_response(raw)
        assert verdict.same_person is False

    def test_integer_same_person_returns_none(self, guard):
        raw = '{"same_person": 1, "confidence": "high", "reasoning": "Match", "quality_issues": null}'
        verdict = guard._parse_response(raw)
        assert verdict.same_person is None

    def test_boolean_true_preserved(self, guard):
        raw = '{"same_person": true, "confidence": "high", "reasoning": "Match", "quality_issues": null}'
        verdict = guard._parse_response(raw)
        assert verdict.same_person is True

    def test_boolean_false_preserved(self, guard):
        raw = '{"same_person": false, "confidence": "low", "reasoning": "No", "quality_issues": null}'
        verdict = guard._parse_response(raw)
        assert verdict.same_person is False

    def test_missing_required_keys_still_parses(self, guard):
        """JSON with missing keys should still parse but use defaults."""
        raw = '{"same_person": true}'
        verdict = guard._parse_response(raw)
        assert verdict.same_person is True
        assert verdict.confidence == "unknown"
        assert verdict.reasoning == ""

    def test_invalid_confidence_normalized_to_unknown(self, guard):
        """Unexpected confidence value should be normalized to 'unknown'."""
        raw = '{"same_person": true, "confidence": "SUPER_HIGH", "reasoning": "ok", "quality_issues": null}'
        verdict = guard._parse_response(raw)
        assert verdict.confidence == "unknown"

    def test_json_embedded_in_text_uses_regex(self, guard):
        """Partial JSON embedded in prose should fall back to regex."""
        raw = 'I think the answer is "same_person": true and "confidence": "medium" based on analysis'
        verdict = guard._parse_response(raw)
        assert verdict.same_person is True
        assert verdict.confidence == "medium"

    def test_regex_invalid_confidence_normalized(self, guard):
        """Regex fallback with unexpected confidence should normalize to unknown."""
        raw = 'Result: "same_person": false, "confidence": "EXTREME"'
        verdict = guard._parse_response(raw)
        assert verdict.same_person is False
        assert verdict.confidence == "unknown"


class TestVLMGuardNotLoaded:
    def test_not_loaded_returns_none(self, guard, face_crops):
        """If model not loaded, verify should return None."""
        verdict = guard.verify(*face_crops, cosine_score=0.55)
        assert verdict.same_person is None
        assert "not loaded" in verdict.reasoning


class TestVLMGuardInference:
    def test_successful_inference(self, sample_config, face_crops):
        """Mock the full inference pipeline."""
        guard = VLMGuard(sample_config)

        mock_processor = MagicMock()
        mock_model = MagicMock()

        guard._processor = mock_processor
        guard._model = mock_model

        mock_processor.apply_chat_template.return_value = "formatted prompt"
        mock_inputs = MagicMock()
        mock_inputs.input_ids.shape = [1, 10]
        mock_inputs.to.return_value = mock_inputs
        mock_processor.return_value = mock_inputs

        import torch
        mock_model.device = torch.device("cpu")
        mock_model.generate.return_value = torch.tensor([[1, 2, 3, 4, 5]])

        mock_processor.decode.return_value = '{"same_person": true, "confidence": "high", "reasoning": "Eyes match", "quality_issues": null}'

        verdict = guard.verify(*face_crops, cosine_score=0.55)
        assert verdict.same_person is True
        assert verdict.reasoning == "Eyes match"

    def test_inference_error_returns_none(self, sample_config, face_crops):
        """If inference raises, should return None gracefully."""
        guard = VLMGuard(sample_config)
        guard._model = MagicMock()
        guard._processor = MagicMock()
        guard._processor.apply_chat_template.side_effect = RuntimeError("OOM")

        verdict = guard.verify(*face_crops, cosine_score=0.55)
        assert verdict.same_person is None
        assert "error" in verdict.reasoning.lower()


class TestVLMGuardAgePrompt:
    """Tests for age-conditioned VLM prompt injection."""

    def test_no_age_supplement_when_gap_lte_3(self, guard, face_crops):
        """Gap <= 3 years should NOT inject age supplement."""
        guard._model = MagicMock()
        guard._processor = MagicMock()
        guard._processor.apply_chat_template.return_value = "prompt"
        mock_inputs = MagicMock()
        mock_inputs.input_ids.shape = [1, 10]
        mock_inputs.to.return_value = mock_inputs
        guard._processor.return_value = mock_inputs

        import torch
        guard._model.device = torch.device("cpu")
        guard._model.generate.return_value = torch.tensor([[1, 2, 3]])
        guard._processor.decode.return_value = '{"same_person": true, "confidence": "high", "reasoning": "ok", "quality_issues": null}'

        guard.verify(*face_crops, cosine_score=0.55, aadhaar_age=30, selfie_age=32)
        sent_messages = guard._processor.apply_chat_template.call_args[0][0]
        prompt_text = sent_messages[0]["content"][-1]["text"]
        assert "AGE CONTEXT" not in prompt_text

    def test_age_supplement_injected_when_gap_gt_3(self, guard, face_crops):
        """Gap > 3 years should inject age supplement with structural features guidance."""
        guard._model = MagicMock()
        guard._processor = MagicMock()
        guard._processor.apply_chat_template.return_value = "prompt"
        mock_inputs = MagicMock()
        mock_inputs.input_ids.shape = [1, 10]
        mock_inputs.to.return_value = mock_inputs
        guard._processor.return_value = mock_inputs

        import torch
        guard._model.device = torch.device("cpu")
        guard._model.generate.return_value = torch.tensor([[1, 2, 3]])
        guard._processor.decode.return_value = '{"same_person": true, "confidence": "high", "reasoning": "ok", "quality_issues": null}'

        guard.verify(*face_crops, cosine_score=0.55, aadhaar_age=25, selfie_age=35)
        sent_messages = guard._processor.apply_chat_template.call_args[0][0]
        prompt_text = sent_messages[0]["content"][-1]["text"]
        assert "AGE CONTEXT" in prompt_text
        assert "bone geometry" in prompt_text

    def test_age_gap_value_in_prompt(self, guard, face_crops):
        """The actual age gap number should appear in the injected supplement."""
        guard._model = MagicMock()
        guard._processor = MagicMock()
        guard._processor.apply_chat_template.return_value = "prompt"
        mock_inputs = MagicMock()
        mock_inputs.input_ids.shape = [1, 10]
        mock_inputs.to.return_value = mock_inputs
        guard._processor.return_value = mock_inputs

        import torch
        guard._model.device = torch.device("cpu")
        guard._model.generate.return_value = torch.tensor([[1, 2, 3]])
        guard._processor.decode.return_value = '{"same_person": true, "confidence": "high", "reasoning": "ok", "quality_issues": null}'

        guard.verify(*face_crops, cosine_score=0.55, aadhaar_age=22, selfie_age=34)
        sent_messages = guard._processor.apply_chat_template.call_args[0][0]
        prompt_text = sent_messages[0]["content"][-1]["text"]
        assert "12 year gap" in prompt_text

    def test_no_supplement_when_age_unknown(self, guard, face_crops):
        """Age=0 (unknown) should NOT inject supplement even with large gap."""
        guard._model = MagicMock()
        guard._processor = MagicMock()
        guard._processor.apply_chat_template.return_value = "prompt"
        mock_inputs = MagicMock()
        mock_inputs.input_ids.shape = [1, 10]
        mock_inputs.to.return_value = mock_inputs
        guard._processor.return_value = mock_inputs

        import torch
        guard._model.device = torch.device("cpu")
        guard._model.generate.return_value = torch.tensor([[1, 2, 3]])
        guard._processor.decode.return_value = '{"same_person": true, "confidence": "high", "reasoning": "ok", "quality_issues": null}'

        guard.verify(*face_crops, cosine_score=0.55, aadhaar_age=0, selfie_age=35)
        sent_messages = guard._processor.apply_chat_template.call_args[0][0]
        prompt_text = sent_messages[0]["content"][-1]["text"]
        assert "AGE CONTEXT" not in prompt_text
