"""Image I/O utilities: EXIF correction, format conversion, base64 encoding, PDF support."""

import base64
import io
import logging

import cv2
import numpy as np
from PIL import Image, ImageOps

logger = logging.getLogger(__name__)


def bytes_to_bgr(raw_bytes: bytes) -> np.ndarray:
    """Load raw image bytes into a BGR numpy array with EXIF orientation correction.

    Supports JPEG, PNG, and PDF (extracts largest embedded image from first page).

    Args:
        raw_bytes: JPEG/PNG/PDF file content.

    Returns:
        BGR uint8 numpy array (H, W, 3).

    Raises:
        ValueError: If the input is not bytes or cannot be decoded as an image.
    """
    if not isinstance(raw_bytes, bytes):
        raise ValueError(f"Expected bytes, got {type(raw_bytes).__name__}")
    if len(raw_bytes) == 0:
        raise ValueError("Image bytes are empty")

    # Detect PDF by magic bytes (%PDF)
    if raw_bytes[:5] == b"%PDF-":
        return _pdf_to_bgr(raw_bytes)

    pil_img = Image.open(io.BytesIO(raw_bytes))
    pil_img = ImageOps.exif_transpose(pil_img)
    pil_img = pil_img.convert("RGB")
    rgb_array = np.array(pil_img, dtype=np.uint8)
    return cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)


def _pdf_to_bgr(raw_bytes: bytes) -> np.ndarray:
    """Extract the largest image from the first page of a PDF.

    Falls back to rendering the page as a pixmap if no embedded images found.

    Args:
        raw_bytes: PDF file content.

    Returns:
        BGR uint8 numpy array (H, W, 3).

    Raises:
        ValueError: If no image can be extracted from the PDF.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        raise ValueError(
            "PDF support requires PyMuPDF. Install with: pip install PyMuPDF"
        )

    doc = fitz.open(stream=raw_bytes, filetype="pdf")
    if len(doc) == 0:
        doc.close()
        raise ValueError("PDF has no pages")

    page = doc[0]

    # Strategy 1: Extract embedded images (preferred — lossless)
    images = page.get_images()
    if images:
        # Pick the largest embedded image
        best_img = None
        best_pixels = 0
        for img_info in images:
            xref = img_info[0]
            extracted = doc.extract_image(xref)
            pixels = extracted["width"] * extracted["height"]
            if pixels > best_pixels:
                best_pixels = pixels
                best_img = extracted

        if best_img is not None:
            img_bytes = best_img["image"]
            doc.close()
            logger.info(
                "PDF: extracted %dx%d %s image from embedded content",
                best_img["width"], best_img["height"], best_img["ext"],
            )
            # Decode extracted image bytes via PIL
            pil_img = Image.open(io.BytesIO(img_bytes))
            pil_img = pil_img.convert("RGB")
            rgb_array = np.array(pil_img, dtype=np.uint8)
            return cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)

    # Strategy 2: Render page to pixmap (fallback for vector PDFs)
    logger.info("PDF: no embedded images, rendering page as pixmap")
    zoom = 2.0  # 2x zoom for better quality
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    doc.close()

    # Convert pixmap to numpy array
    img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
        pix.height, pix.width, pix.n
    )
    if pix.n == 4:  # RGBA
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2BGR)
    elif pix.n == 3:  # RGB
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    else:
        raise ValueError(f"Unexpected pixmap channels: {pix.n}")

    return img_array


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


def apply_clahe(image: np.ndarray, clip_limit: float = 2.0, tile_size: int = 8) -> np.ndarray:
    """Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to a BGR image.

    Normalizes contrast locally — especially useful for printed ID card photos
    where lighting is uneven and contrast is low compared to live selfies.
    Operates on the L channel in LAB color space to preserve color.

    Args:
        image: BGR uint8 numpy array (H, W, 3).
        clip_limit: CLAHE contrast clip limit (higher = more contrast).
        tile_size: Grid size for local histogram equalization.

    Returns:
        Contrast-normalized BGR uint8 numpy array.
    """
    if not isinstance(image, np.ndarray) or image.ndim != 3 or image.shape[2] != 3:
        raise ValueError(f"Expected HxWx3 BGR array, got shape {getattr(image, 'shape', '?')}")
    if clip_limit <= 0:
        raise ValueError(f"clip_limit must be positive, got {clip_limit}")
    if tile_size <= 0:
        raise ValueError(f"tile_size must be positive, got {tile_size}")

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l_chan, a_chan, b_chan = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))
    l_chan = clahe.apply(l_chan)
    lab = cv2.merge([l_chan, a_chan, b_chan])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)


def match_histogram(source: np.ndarray, reference: np.ndarray) -> np.ndarray:
    """Match a source image's color histogram to a reference image.

    Each BGR channel is independently remapped via CDF matching so the output
    has the same tonal distribution as the reference. Useful for shrinking the
    color/lighting domain gap between printed Aadhaar photos and live selfies
    before embedding extraction.

    Args:
        source: BGR uint8 array to be transformed (typically the Aadhaar crop).
        reference: BGR uint8 array whose histogram is the target (typically selfie).

    Returns:
        BGR uint8 array with the same shape as ``source``.
    """
    if source.ndim != 3 or source.shape[2] != 3:
        raise ValueError(f"source must be HxWx3 BGR, got {source.shape}")
    if reference.ndim != 3 or reference.shape[2] != 3:
        raise ValueError(f"reference must be HxWx3 BGR, got {reference.shape}")

    matched = np.empty_like(source)
    for ch in range(3):
        src_vals, src_inv, src_counts = np.unique(
            source[..., ch].ravel(), return_inverse=True, return_counts=True,
        )
        ref_vals, ref_counts = np.unique(reference[..., ch].ravel(), return_counts=True)

        src_cdf = np.cumsum(src_counts).astype(np.float64)
        src_cdf /= src_cdf[-1]
        ref_cdf = np.cumsum(ref_counts).astype(np.float64)
        ref_cdf /= ref_cdf[-1]

        # For each source value, find the reference value whose CDF first exceeds it
        interp = np.interp(src_cdf, ref_cdf, ref_vals)
        matched[..., ch] = np.clip(interp[src_inv].reshape(source.shape[:2]), 0, 255).astype(np.uint8)

    return matched


def to_grayscale_bgr(image: np.ndarray) -> np.ndarray:
    """Convert a BGR image to 3-channel grayscale (removes color information).

    Useful for cross-domain face matching: eliminates color cast differences
    between printed ID card photos and live selfies, forcing the model to
    rely purely on structural/texture features.

    Args:
        image: BGR uint8 numpy array (H, W, 3).

    Returns:
        3-channel grayscale BGR uint8 numpy array (same shape as input).
    """
    if not isinstance(image, np.ndarray) or image.ndim != 3 or image.shape[2] != 3:
        raise ValueError(f"Expected HxWx3 BGR array, got shape {getattr(image, 'shape', '?')}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


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
