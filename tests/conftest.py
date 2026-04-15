"""Shared fixtures for the test suite."""

import numpy as np
import pytest


@pytest.fixture
def sample_config():
    """Minimal config dict for testing."""
    return {
        "preprocessing": {
            "aadhaar_clahe": False,
            "clahe_clip_limit": 2.0,
            "clahe_tile_size": 8,
            "dual_path": False,
            "grayscale_normalize": False,
        },
        "enhancement": {
            "enabled": False,
            "model": "RealESRGAN_x4plus",
            "model_path": "models/realesrgan/RealESRGAN_x4plus.pth",
            "upscale": 2,
            "quality_threshold": 0.4,
        },
        "face": {
            "model_pack": "buffalo_l",
            "insightface_root": "models/insightface",
            "det_size": [640, 640],
            "det_thresh": 0.7,
            "det_thresh_fallback": 0.5,
            "ctx_id": 0,
        },
        "similarity": {
            "match_threshold": 0.60,
            "uncertain_low": 0.40,
            "age_gap_threshold": 5,
            "age_gap_relaxation_per_year": 0.01,
            "max_age_gap_relaxation": 0.10,
            "adaptive_thresholds": False,
            "quality_weighted_fusion": False,
        },
        "adaface": {
            "enabled": False,
            "model_path": "models/adaface/adaface_ir101_webface12m.ckpt",
            "fusion_weight": 0.3,
        },
        "score_norm": {
            "enabled": False,
            "cohort_path": "models/snorm_cohort.npy",
            "cohort_size": 100,
        },
        "calibration": {
            "enabled": False,
            "platt_a": 15.0,
            "platt_b": -7.5,
        },
        "crop_restore": {
            "enabled": False,
            "backend": "bilateral",
        },
        "cache": {
            "max_size": 64,
        },
        "batch": {
            "parallel": False,
            "max_workers": 2,
        },
        "vlm_guard": {
            "enabled": True,
            "model_path": "models/qwen2.5-vl-7b-instruct",
            "temperature": 0.1,
            "max_new_tokens": 256,
        },
        "confidence_adjustments": {
            "vlm_confirmation_bonus": 8.0,
            "vlm_rejection_above_threshold": -20.0,
            "vlm_rejection_uncertain": -10.0,
            "quality_penalty": -5.0,
            "age_gap_vlm_bonus": 5.0,
            "gender_mismatch_penalty": 0.0,
        },
    }


@pytest.fixture
def random_embedding():
    """Generate a random L2-normalized 512-d embedding."""
    def _make():
        v = np.random.randn(512).astype(np.float32)
        v /= np.linalg.norm(v)
        return v
    return _make


@pytest.fixture
def dummy_face_crop():
    """Generate a dummy 112x112 BGR face image."""
    return np.random.randint(0, 255, (112, 112, 3), dtype=np.uint8)
