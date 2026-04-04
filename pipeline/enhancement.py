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

    def __init__(self, config: dict):
        cfg = config["enhancement"]
        self.enabled: bool = cfg["enabled"]
        self.model_path: str = cfg["model_path"]
        self.upscale: int = cfg["upscale"]
        self.quality_threshold: float = cfg["quality_threshold"]
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
        self._upsampler = RealESRGANer(
            scale=4,
            model_path=str(model_path),
            model=model,
            tile=0,
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

    def enhance(self, image: np.ndarray) -> np.ndarray:
        """Upscale and restore image using Real-ESRGAN.

        Args:
            image: BGR uint8 numpy array.

        Returns:
            Enhanced BGR uint8 numpy array.

        Raises:
            EnhancementError: If enhancement fails.
        """
        if not self.enabled or self._upsampler is None:
            return image

        try:
            output, _ = self._upsampler.enhance(image, outscale=self.upscale)
            return output
        except Exception as e:
            raise EnhancementError(f"Real-ESRGAN enhancement failed: {e}") from e

    def maybe_enhance(self, image: np.ndarray) -> tuple[np.ndarray, float]:
        """Assess quality and enhance only if needed.

        Args:
            image: BGR uint8 numpy array.

        Returns:
            Tuple of (possibly enhanced image, quality score before enhancement).
        """
        score = self.quality_score(image)
        if score < self.quality_threshold and self.enabled and self._upsampler is not None:
            logger.info("Quality %.2f < %.2f — enhancing", score, self.quality_threshold)
            image = self.enhance(image)
        else:
            logger.info("Quality %.2f — skipping enhancement", score)
        return image, score
