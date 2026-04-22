"""Image enhancement using Real-ESRGAN with quality-gated processing.

Only enhances images whose quality score (Laplacian variance) falls below
the configured threshold. This avoids unnecessary processing on already-clear
images and prevents introducing artifacts.
"""

import logging
from pathlib import Path

import cv2
import numpy as np
import torch

from utils.exceptions import EnhancementError

logger = logging.getLogger(__name__)


class ImageEnhancer:
    """Real-ESRGAN wrapper with quality assessment.

    Usage:
        enhancer = ImageEnhancer(config)
        enhancer.load()
        score = enhancer.quality_score(image)
        if score < threshold:
            image = enhancer.enhance(image)
    """

    # Max pixels before downscaling prior to enhancement (prevents GPU OOM).
    # 1536x2048 = ~3.1 MP — safe for 12 GB VRAM with 2x upscale.
    MAX_ENHANCE_PIXELS = 1536 * 2048

    def __init__(self, config: dict):
        cfg = config["enhancement"]
        self.enabled: bool = cfg["enabled"]
        self.model_path: str = cfg["model_path"]
        self.upscale: int = cfg["upscale"]
        self.quality_threshold: float = cfg["quality_threshold"]
        self.force_enhance_aadhaar: bool = cfg.get("force_enhance_aadhaar", False)
        self._upsampler = None

    def load(self) -> None:
        """Load Real-ESRGAN model weights. Call once at startup."""
        if not self.enabled:
            logger.info("Enhancement disabled in config")
            return

        model_path = Path(self.model_path)
        if not model_path.exists():
            logger.warning(
                "Real-ESRGAN weights not found at %s. "
                "Run: python scripts/download_models.py",
                model_path,
            )
            self.enabled = False
            return

        from basicsr.archs.rrdbnet_arch import RRDBNet
        from realesrgan import RealESRGANer

        model = RRDBNet(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_block=23,
            num_grow_ch=32,
            scale=4,
        )
        half = torch.cuda.is_available()
        if not half:
            logger.warning("*** GPU NOT AVAILABLE *** — Real-ESRGAN using CPU (FP32). Enhancement will be slow.")
        self._upsampler = RealESRGANer(
            scale=4,
            model_path=str(model_path),
            model=model,
            tile=256,       # small tiles to survive VRAM pressure from VLM (~17GB for Qwen2.5-VL-7B)
            tile_pad=10,
            pre_pad=0,
            half=half,
        )
        device = "GPU (FP16)" if half else "CPU (FP32)"
        logger.info("Real-ESRGAN loaded [%s], upscale=%dx", device, self.upscale)

    def quality_score(self, image: np.ndarray) -> float:
        """Estimate image quality using Laplacian variance (sharpness proxy).

        Args:
            image: BGR uint8 numpy array.

        Returns:
            Normalized quality score in [0.0, 1.0].
            Lower values = more blurry. Typical threshold: 0.4.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        # Normalize: 0-100 Laplacian variance maps to 0.0-1.0
        # Based on empirical testing: lap_var < 40 = very blurry,
        # 40-100 = moderate, >100 = sharp
        return float(np.clip(lap_var / 100.0, 0.0, 1.0))

    def _downscale_if_needed(self, image: np.ndarray) -> np.ndarray:
        """Downscale image if it exceeds MAX_ENHANCE_PIXELS to prevent GPU OOM."""
        h, w = image.shape[:2]
        pixels = h * w
        if pixels <= self.MAX_ENHANCE_PIXELS:
            return image

        scale = (self.MAX_ENHANCE_PIXELS / pixels) ** 0.5
        new_w, new_h = int(w * scale), int(h * scale)
        logger.info(
            "Downscaling %dx%d (%.1f MP) → %dx%d before enhancement",
            w, h, pixels / 1e6, new_w, new_h,
        )
        return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    def enhance(self, image: np.ndarray) -> np.ndarray:
        """Upscale and restore image using Real-ESRGAN.

        Large images are downscaled first to prevent GPU OOM, then
        enhanced with tiled processing.

        Args:
            image: BGR uint8 numpy array.

        Returns:
            Enhanced BGR uint8 numpy array.

        Raises:
            EnhancementError: If enhancement fails.
        """
        if not self.enabled or self._upsampler is None:
            return image

        image = self._downscale_if_needed(image)

        try:
            import torch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            output, _ = self._upsampler.enhance(image, outscale=self.upscale)
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            return output
        except Exception as e:
            # On OOM, return original image instead of crashing the pipeline.
            # The pipeline downstream still has the original + preprocessed paths.
            import torch
            if "out of memory" in str(e).lower() or "output_tile" in str(e):
                logger.warning(
                    "Real-ESRGAN OOM — skipping enhancement for this image. "
                    "Consider reducing VLM precision or tile size further. (%s)", e,
                )
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                return image
            raise EnhancementError(f"Real-ESRGAN enhancement failed: {e}") from e

    def maybe_enhance(
        self, image: np.ndarray, source: str = "image",
    ) -> tuple[np.ndarray, float]:
        """Assess quality and enhance only if needed.

        Args:
            image: BGR uint8 numpy array.
            source: "aadhaar" | "selfie" | "image". When "aadhaar" and
                force_enhance_aadhaar is set, enhancement runs unconditionally
                (printed cards are categorically low-quality even when Laplacian
                variance passes the gate).

        Returns:
            Tuple of (possibly enhanced image, quality score before enhancement).
        """
        score = self.quality_score(image)
        force = self.force_enhance_aadhaar and source == "aadhaar"
        if force or score < self.quality_threshold:
            if self.enabled and self._upsampler is not None:
                reason = "forced (aadhaar)" if force else f"quality {score:.2f} < {self.quality_threshold:.2f}"
                logger.info("Enhancing — %s", reason)
                image = self.enhance(image)
            else:
                logger.warning(
                    "Enhancement requested (force=%s, score=%.2f) but unavailable "
                    "(enabled=%s, model_loaded=%s)",
                    force, score, self.enabled, self._upsampler is not None,
                )
        else:
            logger.debug("Quality %.2f — skipping enhancement", score)
        return image, score
