"""Tests for utils/image_utils.py — bytes_to_bgr and bgr_to_base64_jpeg."""

import base64

import cv2
import numpy as np
import pytest

from utils.image_utils import (
    apply_clahe, bgr_to_base64_jpeg, bytes_to_bgr, match_histogram,
    to_grayscale_bgr, validate_image_dimensions,
)


class TestBytesToBGR:
    def test_valid_jpeg(self):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        _, buf = cv2.imencode(".jpg", img)
        result = bytes_to_bgr(buf.tobytes())
        assert result.shape[2] == 3
        assert result.dtype == np.uint8

    def test_valid_png(self):
        img = np.zeros((50, 50, 3), dtype=np.uint8)
        _, buf = cv2.imencode(".png", img)
        result = bytes_to_bgr(buf.tobytes())
        assert result.shape == (50, 50, 3)

    def test_corrupt_bytes_raises(self):
        with pytest.raises(Exception):
            bytes_to_bgr(b"not an image at all")

    def test_empty_bytes_raises(self):
        with pytest.raises(Exception):
            bytes_to_bgr(b"")

    def test_rgba_converted_to_bgr(self):
        """RGBA images (PNGs with alpha) should be converted to 3-channel BGR."""
        from PIL import Image
        import io
        rgba = Image.new("RGBA", (50, 50), (255, 0, 0, 128))
        buf = io.BytesIO()
        rgba.save(buf, format="PNG")
        result = bytes_to_bgr(buf.getvalue())
        assert result.shape[2] == 3


class TestPDFSupport:
    """Test PDF image extraction in bytes_to_bgr."""

    def test_pdf_magic_bytes_detected(self):
        """Non-PDF bytes should not trigger PDF path."""
        jpeg = cv2.imencode(".jpg", np.zeros((10, 10, 3), dtype=np.uint8))[1].tobytes()
        assert not jpeg.startswith(b"%PDF-")
        img = bytes_to_bgr(jpeg)
        assert img.shape == (10, 10, 3)

    def test_pdf_missing_pymupdf_raises(self):
        """PDF bytes without PyMuPDF should raise ValueError."""
        import unittest.mock as mock
        pdf_bytes = b"%PDF-1.4 fake content"
        with mock.patch.dict("sys.modules", {"fitz": None}):
            with pytest.raises((ValueError, ImportError)):
                bytes_to_bgr(pdf_bytes)

    def test_pdf_empty_raises(self):
        """Empty bytes should raise ValueError."""
        with pytest.raises(ValueError, match="empty"):
            bytes_to_bgr(b"")


class TestBGRToBase64:
    def test_roundtrip(self):
        img = np.random.randint(0, 255, (112, 112, 3), dtype=np.uint8)
        b64 = bgr_to_base64_jpeg(img)
        decoded = base64.b64decode(b64)
        # Should start with JPEG magic bytes
        assert decoded[:2] == b'\xff\xd8'

    def test_quality_parameter(self):
        img = np.random.randint(0, 255, (112, 112, 3), dtype=np.uint8)
        low_q = bgr_to_base64_jpeg(img, quality=10)
        high_q = bgr_to_base64_jpeg(img, quality=95)
        # Lower quality should produce smaller output
        assert len(low_q) < len(high_q)


class TestInputValidation:
    """Tests for input validation added to image_utils."""

    def test_bytes_to_bgr_rejects_string(self):
        with pytest.raises(ValueError, match="Expected bytes"):
            bytes_to_bgr("not bytes")

    def test_bytes_to_bgr_rejects_empty(self):
        with pytest.raises(ValueError, match="empty"):
            bytes_to_bgr(b"")

    def test_bgr_to_base64_rejects_non_array(self):
        with pytest.raises(ValueError, match="numpy array"):
            bgr_to_base64_jpeg("not an array")

    def test_bgr_to_base64_rejects_grayscale(self):
        gray = np.zeros((112, 112), dtype=np.uint8)
        with pytest.raises(ValueError, match="HxWx3"):
            bgr_to_base64_jpeg(gray)

    def test_bgr_to_base64_rejects_4channel(self):
        rgba = np.zeros((112, 112, 4), dtype=np.uint8)
        with pytest.raises(ValueError, match="HxWx3"):
            bgr_to_base64_jpeg(rgba)

    def test_bgr_to_base64_rejects_quality_zero(self):
        img = np.zeros((10, 10, 3), dtype=np.uint8)
        with pytest.raises(ValueError, match="quality"):
            bgr_to_base64_jpeg(img, quality=0)

    def test_bgr_to_base64_rejects_quality_over_100(self):
        img = np.zeros((10, 10, 3), dtype=np.uint8)
        with pytest.raises(ValueError, match="quality"):
            bgr_to_base64_jpeg(img, quality=101)


class TestApplyCLAHE:
    def test_output_same_shape(self):
        img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        result = apply_clahe(img)
        assert result.shape == img.shape
        assert result.dtype == np.uint8

    def test_improves_contrast_on_dark_image(self):
        """CLAHE should increase the dynamic range of a uniformly dark image."""
        dark = np.full((100, 100, 3), 30, dtype=np.uint8)
        result = apply_clahe(dark, clip_limit=3.0)
        assert result.mean() >= dark.mean()  # should brighten

    def test_custom_params(self):
        img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        result = apply_clahe(img, clip_limit=4.0, tile_size=4)
        assert result.shape == img.shape

    def test_rejects_non_bgr(self):
        gray = np.zeros((100, 100), dtype=np.uint8)
        with pytest.raises(ValueError, match="HxWx3"):
            apply_clahe(gray)

    def test_rejects_invalid_clip_limit(self):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        with pytest.raises(ValueError, match="clip_limit"):
            apply_clahe(img, clip_limit=0)

    def test_rejects_invalid_tile_size(self):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        with pytest.raises(ValueError, match="tile_size"):
            apply_clahe(img, tile_size=-1)


class TestToGrayscaleBGR:
    def test_output_same_shape(self):
        img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        result = to_grayscale_bgr(img)
        assert result.shape == img.shape
        assert result.dtype == np.uint8

    def test_channels_are_identical(self):
        """All 3 channels should be the same grayscale value."""
        img = np.random.randint(0, 255, (50, 50, 3), dtype=np.uint8)
        result = to_grayscale_bgr(img)
        assert np.array_equal(result[:, :, 0], result[:, :, 1])
        assert np.array_equal(result[:, :, 1], result[:, :, 2])

    def test_already_gray_is_idempotent(self):
        """Applying twice should produce the same result."""
        img = np.random.randint(0, 255, (50, 50, 3), dtype=np.uint8)
        once = to_grayscale_bgr(img)
        twice = to_grayscale_bgr(once)
        assert np.array_equal(once, twice)

    def test_rejects_non_bgr(self):
        gray = np.zeros((50, 50), dtype=np.uint8)
        with pytest.raises(ValueError, match="HxWx3"):
            to_grayscale_bgr(gray)


class TestValidateImageDimensions:
    def test_valid_image(self):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        w, h = validate_image_dimensions(img)
        assert w == 100
        assert h == 100

    def test_too_small_both_sides(self):
        img = np.zeros((30, 30, 3), dtype=np.uint8)
        with pytest.raises(ValueError, match="too small"):
            validate_image_dimensions(img)

    def test_one_side_too_small(self):
        img = np.zeros((100, 40, 3), dtype=np.uint8)
        with pytest.raises(ValueError, match="too small"):
            validate_image_dimensions(img)

    def test_custom_min_size(self):
        img = np.zeros((150, 150, 3), dtype=np.uint8)
        with pytest.raises(ValueError, match="too small"):
            validate_image_dimensions(img, min_size=200)


class TestMatchHistogram:
    """v3: match_histogram remaps tonal distribution from source toward reference."""

    def _mean_per_channel(self, img):
        return img.reshape(-1, 3).mean(axis=0)

    def test_identical_source_reference_returns_equivalent(self):
        rng = np.random.default_rng(42)
        img = rng.integers(0, 255, (64, 64, 3), dtype=np.uint8)
        out = match_histogram(img, img)
        assert out.shape == img.shape
        assert out.dtype == np.uint8
        # Matching to itself should round-trip near-identity (CDF maps bin→same bin).
        assert np.abs(out.astype(int) - img.astype(int)).mean() < 1.0

    def test_mean_shifts_toward_reference(self):
        rng = np.random.default_rng(0)
        # Source is dark-ish (mean ~80), reference is bright (mean ~200)
        dark = (rng.integers(0, 255, (80, 80, 3)) * 0.4).astype(np.uint8) + 40
        bright = np.clip(
            (rng.integers(0, 255, (80, 80, 3)) * 0.4).astype(np.int32) + 170, 0, 255,
        ).astype(np.uint8)
        matched = match_histogram(dark, bright)

        src_mean = self._mean_per_channel(dark)
        ref_mean = self._mean_per_channel(bright)
        out_mean = self._mean_per_channel(matched)

        # Each channel's mean should have moved from source toward reference
        assert np.all(out_mean > src_mean + 10)
        assert np.all(np.abs(out_mean - ref_mean) < np.abs(src_mean - ref_mean))

    def test_output_is_uint8(self):
        src = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
        ref = np.random.randint(0, 255, (48, 48, 3), dtype=np.uint8)
        out = match_histogram(src, ref)
        assert out.dtype == np.uint8
        assert out.min() >= 0 and out.max() <= 255

    def test_rejects_non_bgr_source(self):
        ref = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
        with pytest.raises(ValueError, match="source"):
            match_histogram(np.zeros((32, 32), dtype=np.uint8), ref)

    def test_rejects_non_bgr_reference(self):
        src = np.random.randint(0, 255, (32, 32, 3), dtype=np.uint8)
        with pytest.raises(ValueError, match="reference"):
            match_histogram(src, np.zeros((32, 32, 1), dtype=np.uint8))
