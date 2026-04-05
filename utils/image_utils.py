"""Image I/O utilities: EXIF correction, format conversion, base64 encoding."""

import base64
import io

import cv2
import numpy as np
from PIL import Image, ImageOps


def bytes_to_bgr(raw_bytes: bytes) -> np.ndarray:
    """Load raw image bytes into a BGR numpy array with EXIF orientation correction.

    Args:
        raw_bytes: JPEG/PNG file content.

    Returns:
        BGR uint8 numpy array (H, W, 3).

    Raises:
        ValueError: If the input is not bytes or cannot be decoded as an image.
    """
    if not isinstance(raw_bytes, bytes):
        raise ValueError(f"Expected bytes, got {type(raw_bytes).__name__}")
    if len(raw_bytes) == 0:
        raise ValueError("Image bytes are empty")

    pil_img = Image.open(io.BytesIO(raw_bytes))
    pil_img = ImageOps.exif_transpose(pil_img)
    pil_img = pil_img.convert("RGB")
    rgb_array = np.array(pil_img, dtype=np.uint8)
    return cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)


def bgr_to_base64_jpeg(image: np.ndarray, quality: int = 90) -> str:
    """Encode a BGR numpy array to a base64 JPEG string (no data URI prefix).

    Args:
        image: BGR uint8 numpy array (H, W, 3).
        quality: JPEG compression quality (1-100).

    Returns:
        Base64-encoded JPEG string.

    Raises:
        ValueError: If image is not a 3-channel numpy array or quality is out of range.
    """
    if not isinstance(image, np.ndarray):
        raise ValueError(f"Expected numpy array, got {type(image).__name__}")
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError(f"Expected HxWx3 array, got shape {image.shape}")
    if not (1 <= quality <= 100):
        raise ValueError(f"JPEG quality must be in [1, 100], got {quality}")

    ok, buf = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ok:
        raise ValueError("Failed to encode image as JPEG")
    return base64.b64encode(buf.tobytes()).decode("ascii")


def validate_image_dimensions(image: np.ndarray, min_size: int = 50) -> tuple[int, int]:
    """Validate image dimensions meet minimum requirements.

    Args:
        image: BGR uint8 numpy array (H, W, 3).
        min_size: Minimum width and height in pixels.

    Returns:
        (width, height) tuple.

    Raises:
        ValueError: If image is below minimum size.
    """
    h, w = image.shape[:2]
    if w < min_size or h < min_size:
        raise ValueError(f"Image too small ({w}x{h}), minimum is {min_size}x{min_size}")
    return w, h
