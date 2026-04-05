"""Tests for pipeline/enhancement.py — no GPU or Real-ESRGAN required."""

from unittest.mock import MagicMock, patch

import cv2
import numpy as np
import pytest

from pipeline.enhancement import ImageEnhancer
from utils.exceptions import EnhancementError


@pytest.fixture
def enhancer(sample_config):
    """Create an ImageEnhancer with enhancement disabled (no model needed)."""
    sample_config["enhancement"]["enabled"] = False
    return ImageEnhancer(sample_config)


@pytest.fixture
def enhancer_enabled(sample_config):
    """Create an ImageEnhancer with enabled=True but no upsampler loaded."""
    sample_config["enhancement"]["enabled"] = True
    e = ImageEnhancer(sample_config)
    # _upsampler stays None since we don't call load()
    return e


class TestQualityScore:
    def test_sharp_image_high_score(self, enhancer):
        """Checkerboard pattern has high Laplacian variance → high quality."""
        img = np.zeros((200, 200, 3), dtype=np.uint8)
        img[::2, ::2] = 255  # checkerboard
        score = enhancer.quality_score(img)
        assert score > 0.8

    def test_uniform_image_low_score(self, enhancer):
        """Flat gray image has zero Laplacian variance → quality 0.0."""
        img = np.full((200, 200, 3), 128, dtype=np.uint8)
        score = enhancer.quality_score(img)
        assert score < 0.05

    def test_blurry_image_moderate_score(self, enhancer):
        """Gaussian-blurred edges → moderate quality."""
        img = np.zeros((200, 200, 3), dtype=np.uint8)
        img[50:150, 50:150] = 255
        blurred = cv2.GaussianBlur(img, (21, 21), 0)
        score = enhancer.quality_score(blurred)
        assert 0.0 < score < 0.8

    def test_returns_float_in_range(self, enhancer):
        img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        score = enhancer.quality_score(img)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_score_clamped_to_one(self, enhancer):
        """Very high-contrast noise should be clamped to 1.0."""
        # Random noise has very high Laplacian variance
        img = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        score = enhancer.quality_score(img)
        assert score <= 1.0


class TestDownscaleIfNeeded:
    def test_small_image_unchanged(self, enhancer):
        img = np.zeros((200, 200, 3), dtype=np.uint8)
        result = enhancer._downscale_if_needed(img)
        assert result.shape == (200, 200, 3)

    def test_large_image_reduced(self, enhancer):
        img = np.zeros((4000, 3000, 3), dtype=np.uint8)
        result = enhancer._downscale_if_needed(img)
        h, w = result.shape[:2]
        assert h * w <= ImageEnhancer.MAX_ENHANCE_PIXELS * 1.01  # small rounding tolerance

    def test_preserves_aspect_ratio(self, enhancer):
        img = np.zeros((4000, 2000, 3), dtype=np.uint8)
        result = enhancer._downscale_if_needed(img)
        h, w = result.shape[:2]
        ratio = w / h
        assert abs(ratio - 0.5) < 0.02  # original ratio 2000/4000 = 0.5

    def test_exact_boundary_unchanged(self, enhancer):
        """Image exactly at MAX_ENHANCE_PIXELS should not be downscaled."""
        # MAX_ENHANCE_PIXELS = 1536 * 2048
        img = np.zeros((1536, 2048, 3), dtype=np.uint8)
        result = enhancer._downscale_if_needed(img)
        assert result.shape == (1536, 2048, 3)


class TestEnhance:
    def test_returns_input_when_disabled(self, enhancer):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        result = enhancer.enhance(img)
        assert result is img  # same object, not just equal

    def test_returns_input_when_no_upsampler(self, enhancer_enabled):
        """enabled=True but _upsampler=None → return input unchanged."""
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        result = enhancer_enabled.enhance(img)
        assert result is img

    def test_raises_on_upsampler_failure(self, enhancer_enabled):
        """Mock upsampler that raises → should wrap in EnhancementError."""
        mock_upsampler = MagicMock()
        mock_upsampler.enhance.side_effect = RuntimeError("GPU OOM")
        enhancer_enabled._upsampler = mock_upsampler
        with pytest.raises(EnhancementError, match="Real-ESRGAN enhancement failed"):
            enhancer_enabled.enhance(np.zeros((100, 100, 3), dtype=np.uint8))


class TestMaybeEnhance:
    def test_skips_when_quality_high(self, enhancer):
        """Sharp image + disabled enhancer → return same image."""
        img = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        result_img, score = enhancer.maybe_enhance(img)
        assert result_img is img

    def test_returns_tuple(self, enhancer):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        result = enhancer.maybe_enhance(img)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], np.ndarray)
        assert isinstance(result[1], float)

    def test_warns_when_quality_low_but_unavailable(self, enhancer_enabled, caplog):
        """Low quality + no upsampler → warning logged."""
        import logging
        with caplog.at_level(logging.WARNING):
            flat = np.full((200, 200, 3), 128, dtype=np.uint8)
            enhancer_enabled.maybe_enhance(flat)
        assert "enhancement unavailable" in caplog.text
