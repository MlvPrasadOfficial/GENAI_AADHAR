"""Integration tests for the full pipeline.

These tests require:
  - Downloaded model weights (Real-ESRGAN, InsightFace buffalo_l)
  - GPU available

Mark with pytest.mark.integration so they can be skipped in CI:
    pytest tests/test_pipeline.py -v -m integration
"""

import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import numpy as np
import pytest

from pipeline.orchestrator import KYCPipelineOrchestrator, PipelineResult

# Skip all tests in this file if models aren't downloaded
MODELS_DIR = Path(__file__).parent.parent / "models"
BUFFALO_DIR = MODELS_DIR / "insightface" / "models" / "buffalo_l"

models_available = BUFFALO_DIR.exists() and any(BUFFALO_DIR.glob("*.onnx"))

pytestmark = pytest.mark.skipif(
    not models_available,
    reason="Models not downloaded. Run: python scripts/download_models.py",
)


@pytest.fixture(scope="module")
def pipeline(sample_config_module):
    """Load pipeline once for all tests in this module."""
    pipe = KYCPipelineOrchestrator(sample_config_module)
    pipe.load()
    return pipe


@pytest.fixture(scope="module")
def sample_config_module():
    """Module-scoped config."""
    return {
        "enhancement": {
            "enabled": False,  # skip enhancement for speed in tests
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
        },
        "vlm_guard": {
            "enabled": False,  # skip VLM in integration tests
            "ollama_url": "http://localhost:11434",
            "model": "llava:13b",
            "timeout_s": 30,
            "temperature": 0.1,
        },
    }


@pytest.mark.integration
class TestPipelineWithBlankImage:
    """Test pipeline error handling with images that have no faces."""

    def test_blank_image_returns_error(self, pipeline):
        """A blank white image should return error, not crash."""
        import cv2
        blank = np.ones((200, 200, 3), dtype=np.uint8) * 255
        _, buf = cv2.imencode(".jpg", blank)
        blank_bytes = buf.tobytes()

        result = pipeline.run(blank_bytes, blank_bytes)
        assert result.match is False
        assert result.error is not None
        assert "No face detected" in result.error


@pytest.mark.integration
class TestPipelineResultStructure:
    """Verify PipelineResult has all expected fields."""

    def test_result_fields(self):
        result = PipelineResult(
            match=True,
            confidence_pct=85.0,
            cosine_score=0.72,
            vlm_same_person=None,
            vlm_reasoning=None,
        )
        assert result.match is True
        assert result.confidence_pct == 85.0
        assert result.cosine_score == 0.72
        assert result.stage_timings == {}
        assert result.error is None
