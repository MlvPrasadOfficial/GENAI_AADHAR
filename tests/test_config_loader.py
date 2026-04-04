"""Tests for utils/config_loader.py — validation logic."""

import pytest

from utils.config_loader import _validate


def _base_config():
    return {
        "enhancement": {"enabled": False, "model": "x", "model_path": "x", "upscale": 2, "quality_threshold": 0.4},
        "face": {"model_pack": "buffalo_l", "insightface_root": "x", "det_size": [640, 640],
                 "det_thresh": 0.7, "det_thresh_fallback": 0.5, "ctx_id": 0},
        "similarity": {"match_threshold": 0.60, "uncertain_low": 0.40},
        "vlm_guard": {"enabled": False, "ollama_url": "http://localhost:11434",
                      "model": "x", "timeout_s": 30, "temperature": 0.1},
    }


class TestValidation:
    def test_valid_config_passes(self):
        _validate(_base_config())

    def test_missing_section_raises(self):
        cfg = _base_config()
        del cfg["face"]
        with pytest.raises(ValueError, match="Missing required"):
            _validate(cfg)

    def test_uncertain_low_gte_match_threshold_raises(self):
        cfg = _base_config()
        cfg["similarity"]["uncertain_low"] = 0.60
        with pytest.raises(ValueError, match="uncertain_low"):
            _validate(cfg)

    def test_threshold_above_one_raises(self):
        cfg = _base_config()
        cfg["similarity"]["match_threshold"] = 1.5
        with pytest.raises(ValueError, match="\\[0.0, 1.0\\]"):
            _validate(cfg)

    def test_threshold_below_zero_raises(self):
        cfg = _base_config()
        cfg["similarity"]["uncertain_low"] = -0.1
        with pytest.raises(ValueError, match="\\[0.0, 1.0\\]"):
            _validate(cfg)

    def test_det_thresh_above_one_raises(self):
        cfg = _base_config()
        cfg["face"]["det_thresh"] = 1.5
        with pytest.raises(ValueError, match="det_thresh"):
            _validate(cfg)

    def test_fallback_gte_primary_raises(self):
        cfg = _base_config()
        cfg["face"]["det_thresh_fallback"] = 0.8
        with pytest.raises(ValueError, match="det_thresh_fallback"):
            _validate(cfg)
