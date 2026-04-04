"""Tests for utils/image_utils.py — bytes_to_bgr and bgr_to_base64_jpeg."""

import base64

import cv2
import numpy as np
import pytest

from utils.image_utils import bgr_to_base64_jpeg, bytes_to_bgr


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
