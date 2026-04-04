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
        ValueError: If the bytes cannot be decoded as an image.
    """
    pil_img = Image.open(io.BytesIO(raw_bytes))
    pil_img = ImageOps.exif_transpose(pil_img)
    pil_img = pil_img.convert("RGB")
    rgb_array = np.array(pil_img, dtype=np.uint8)
    return cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)


def bgr_to_base64_jpeg(image: np.ndarray, quality: int = 90) -> str:
    """Encode a BGR numpy array to a base64 JPEG string (no data URI prefix).

    Args:
        image: BGR uint8 numpy array.
        quality: JPEG compression quality (0-100).

    Returns:
        Base64-encoded JPEG string.
    """
    ok, buf = cv2.imencode(".jpg", image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    if not ok:
        raise ValueError("Failed to encode image as JPEG")
    return base64.b64encode(buf.tobytes()).decode("ascii")
