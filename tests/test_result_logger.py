"""Tests for utils/result_logger.py — log folder creation and content."""

import re
from dataclasses import dataclass, field
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

from utils.result_logger import log_result


@dataclass
class _FakeResult:
    """Minimal PipelineResult stand-in for testing."""

    match: bool = False
    confidence_pct: float = 50.0
    cosine_score: float = 0.55
    vlm_same_person: bool | None = None
    vlm_reasoning: str | None = None
    stage_timings: dict = field(default_factory=lambda: {"load_ms": 10, "face_processing_ms": 100})
    aadhaar_quality: float = 0.8
    selfie_quality: float = 0.9
    aadhaar_crop: np.ndarray | None = None
    selfie_crop: np.ndarray | None = None
    aadhaar_gender: str = "M"
    aadhaar_age: int = 30
    selfie_gender: str = "M"
    selfie_age: int = 30
    error: str | None = None


class TestLogResult:
    def test_creates_run_folder(self, tmp_path):
        result = _FakeResult()
        run_dir = log_result(result, "card.jpg", "selfie.jpg", log_dir=str(tmp_path))
        assert run_dir.exists()
        assert (run_dir / "result.txt").exists()

    def test_folder_name_contains_status(self, tmp_path):
        result = _FakeResult(match=True)
        run_dir = log_result(result, "a.jpg", "b.jpg", log_dir=str(tmp_path))
        assert "MATCH" in run_dir.name

    def test_folder_name_contains_hash(self, tmp_path):
        result = _FakeResult()
        run_dir = log_result(result, "a.jpg", "b.jpg", log_dir=str(tmp_path))
        # Folder name should end with _<8-char-hex>
        assert re.search(r"_[a-f0-9]{8}$", run_dir.name)

    def test_error_status_in_folder_name(self, tmp_path):
        result = _FakeResult(error="something broke")
        run_dir = log_result(result, "a.jpg", "b.jpg", log_dir=str(tmp_path))
        assert "ERROR" in run_dir.name

    def test_result_txt_contains_scores(self, tmp_path):
        result = _FakeResult(cosine_score=0.5470, confidence_pct=44.7)
        run_dir = log_result(result, "a.jpg", "b.jpg", log_dir=str(tmp_path))
        text = (run_dir / "result.txt").read_text(encoding="utf-8")
        assert "0.5470" in text
        assert "44.7%" in text

    def test_face_crops_saved(self, tmp_path):
        crop = np.zeros((112, 112, 3), dtype=np.uint8)
        result = _FakeResult(aadhaar_crop=crop, selfie_crop=crop)
        run_dir = log_result(result, "a.jpg", "b.jpg", log_dir=str(tmp_path))
        assert (run_dir / "aadhaar_crop.jpg").exists()
        assert (run_dir / "selfie_crop.jpg").exists()

    def test_no_crops_when_none(self, tmp_path):
        result = _FakeResult()
        run_dir = log_result(result, "a.jpg", "b.jpg", log_dir=str(tmp_path))
        assert not (run_dir / "aadhaar_crop.jpg").exists()

    def test_decision_trace_with_config(self, tmp_path):
        config = {
            "similarity": {"match_threshold": 0.60, "uncertain_low": 0.40},
            "enhancement": {"quality_threshold": 0.4},
            "vlm_guard": {"enabled": True},
            "confidence_adjustments": {
                "vlm_confirmation_bonus": 8.0,
                "vlm_rejection_above_threshold": -20.0,
                "vlm_rejection_uncertain": -10.0,
                "quality_penalty": -5.0,
            },
        }
        result = _FakeResult(
            cosine_score=0.55, vlm_same_person=False, vlm_reasoning="No match"
        )
        run_dir = log_result(result, "a.jpg", "b.jpg", config=config, log_dir=str(tmp_path))
        text = (run_dir / "result.txt").read_text(encoding="utf-8")
        assert "Decision Trace" in text
        assert "VLM rejection" in text

    def test_timings_in_output(self, tmp_path):
        result = _FakeResult(stage_timings={"load_ms": 50, "vlm_ms": 5000})
        run_dir = log_result(result, "a.jpg", "b.jpg", log_dir=str(tmp_path))
        text = (run_dir / "result.txt").read_text(encoding="utf-8")
        assert "TOTAL" in text
        assert "5050" in text

    def test_decision_trace_includes_age_relaxation(self, tmp_path):
        """Large age gap should produce an age-gap relaxation line in the trace."""
        config = {
            "similarity": {
                "match_threshold": 0.60, "uncertain_low": 0.40,
                "age_gap_threshold": 5, "age_gap_relaxation_per_year": 0.01,
                "max_age_gap_relaxation": 0.10,
            },
            "enhancement": {"quality_threshold": 0.4},
            "vlm_guard": {"enabled": True},
            "confidence_adjustments": {},
        }
        result = _FakeResult(cosine_score=0.55, aadhaar_age=25, selfie_age=35)
        run_dir = log_result(result, "a.jpg", "b.jpg", config=config, log_dir=str(tmp_path))
        text = (run_dir / "result.txt").read_text(encoding="utf-8")
        assert "Age-gap relaxation" in text
        assert "10yr gap" in text

    def test_decision_trace_no_relaxation_for_small_gap(self, tmp_path):
        """Small age gap should NOT produce a relaxation line."""
        config = {
            "similarity": {
                "match_threshold": 0.60, "uncertain_low": 0.40,
                "age_gap_threshold": 5, "age_gap_relaxation_per_year": 0.01,
                "max_age_gap_relaxation": 0.10,
            },
            "enhancement": {"quality_threshold": 0.4},
            "vlm_guard": {"enabled": True},
            "confidence_adjustments": {},
        }
        result = _FakeResult(cosine_score=0.55, aadhaar_age=30, selfie_age=32)
        run_dir = log_result(result, "a.jpg", "b.jpg", config=config, log_dir=str(tmp_path))
        text = (run_dir / "result.txt").read_text(encoding="utf-8")
        assert "Age-gap relaxation" not in text
