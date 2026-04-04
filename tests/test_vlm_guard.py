"""Tests for pipeline/vlm_guard.py — uses mocked HTTP calls, no Ollama needed."""

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


class TestVLMGuardHTTP:
    @patch("pipeline.vlm_guard.requests.post")
    def test_successful_call(self, mock_post, guard, face_crops):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {
            "message": {
                "content": '{"same_person": true, "confidence": "high", "reasoning": "Eyes match", "quality_issues": null}'
            }
        }
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        verdict = guard.verify(*face_crops, cosine_score=0.55)
        assert verdict.same_person is True
        assert verdict.reasoning == "Eyes match"
        mock_post.assert_called_once()

    @patch("pipeline.vlm_guard.requests.post")
    def test_connection_error_returns_none(self, mock_post, guard, face_crops):
        import requests as req
        mock_post.side_effect = req.ConnectionError("refused")

        verdict = guard.verify(*face_crops, cosine_score=0.55)
        assert verdict.same_person is None
        assert "unreachable" in verdict.reasoning

    @patch("pipeline.vlm_guard.requests.post")
    def test_timeout_returns_none(self, mock_post, guard, face_crops):
        import requests as req
        mock_post.side_effect = req.Timeout("timed out")

        verdict = guard.verify(*face_crops, cosine_score=0.55)
        assert verdict.same_person is None
