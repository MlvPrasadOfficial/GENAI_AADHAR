"""Tests for utils/image_utils.py — bytes_to_bgr and bgr_to_base64_jpeg."""

import base64

import cv2
import numpy as np
import pytest

from utils.image_utils import bgr_to_base64_jpeg, bytes_to_bgr, validate_image_dimensions


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
