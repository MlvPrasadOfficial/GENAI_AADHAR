"""Crop-level face restoration using GFPGAN or CodeFormer.

Unlike full-image enhancement, this operates on the 112x112 aligned face
crop AFTER detection + alignment. This is safer for identity preservation
because:
  1. The face is already isolated and aligned
  2. The restoration only cleans up artifacts, noise, and compression
  3. It doesn't hallucinate or shift facial features on small crops

This module gracefully degrades — if no restoration model is available,
it returns the input crop unchanged.
"""

import logging
from pathlib import Path

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class CropRestorer:
    """Face crop restoration for 112x112 aligned face images.

    Supports two backends:
      - GFPGAN (preferred, better quality)
      - OpenCV bilateral filter (always available, lighter cleanup)

    Usage:
        restorer = CropRestorer(config)
        restorer.load()
        restored = restorer.restore(aligned_crop)
    """

    def __init__(self, config: dict):
        cr_cfg = config.get("crop_restore", {})
        self.enabled: bool = cr_cfg.get("enabled", False)
        self.backend: str = cr_cfg.get("backend", "bilateral")
        self.gfpgan_model_path: str = cr_cfg.get(
            "gfpgan_model_path", "models/gfpgan/GFPGANv1.4.pth"
        )
        self.bilateral_d: int = cr_cfg.get("bilateral_d", 5)
        self.bilateral_sigma_color: float = cr_cfg.get("bilateral_sigma_color", 50.0)
        self.bilateral_sigma_space: float = cr_cfg.get("bilateral_sigma_space", 50.0)
        self._gfpgan_restorer = None

    def load(self) -> None:
        """Load the restoration model if GFPGAN backend is configured."""
        if not self.enabled:
            logger.debug("Crop restoration disabled")
            return

        if self.backend == "gfpgan":
            self._load_gfpgan()
        elif self.backend == "bilateral":
            logger.info("Crop restoration: bilateral filter (d=%d, σ_c=%.0f, σ_s=%.0f)",
                        self.bilateral_d, self.bilateral_sigma_color, self.bilateral_sigma_space)
        else:
            logger.warning("Unknown crop_restore backend '%s', falling back to bilateral", self.backend)
            self.backend = "bilateral"

    def _load_gfpgan(self) -> None:
        """Attempt to load GFPGAN for crop restoration."""
        model_path = Path(self.gfpgan_model_path)
        if not model_path.exists():
            logger.warning(
                "GFPGAN model not found at %s — falling back to bilateral filter",
                model_path,
            )
            self.backend = "bilateral"
            return

        try:
            from gfpgan import GFPGANer

            self._gfpgan_restorer = GFPGANer(
                model_path=str(model_path),
                upscale=1,  # no upscale — keep 112x112
                arch="clean",
                channel_multiplier=2,
            )
            logger.info("GFPGAN loaded for crop restoration")
        except ImportError:
            logger.warning("gfpgan package not installed — falling back to bilateral filter")
            self.backend = "bilateral"
        except Exception as e:
            logger.warning("GFPGAN load failed (%s) — falling back to bilateral filter", e)
            self.backend = "bilateral"

    def restore(self, crop: np.ndarray) -> np.ndarray:
        """Restore a 112x112 aligned face crop.

        Args:
            crop: 112x112 BGR uint8 aligned face image.

        Returns:
            Restored crop (same shape), or original if restoration fails.
        """
        if not self.enabled or crop is None:
            return crop

        if self.backend == "gfpgan" and self._gfpgan_restorer is not None:
            return self._restore_gfpgan(crop)
        return self._restore_bilateral(crop)

    def _restore_gfpgan(self, crop: np.ndarray) -> np.ndarray:
        """Restore using GFPGAN (identity-preserving face restoration)."""
        try:
            # GFPGAN expects larger images; upscale → restore → downscale
            upscaled = cv2.resize(crop, (512, 512), interpolation=cv2.INTER_CUBIC)
            _, _, restored = self._gfpgan_restorer.enhance(
                upscaled, has_aligned=True, only_center_face=True, paste_back=False,
            )
            if restored is not None and len(restored) > 0:
                result = cv2.resize(restored[0], (112, 112), interpolation=cv2.INTER_AREA)
                return result
        except Exception as e:
            logger.warning("GFPGAN restoration failed: %s", e)
        return crop

    def _restore_bilateral(self, crop: np.ndarray) -> np.ndarray:
        """Restore using bilateral filter (denoise while preserving edges).

        Bilateral filtering smooths noise and compression artifacts while
        keeping sharp edges (eye contours, nose bridge, jawline) intact.
        """
        return cv2.bilateralFilter(
            crop,
            d=self.bilateral_d,
            sigmaColor=self.bilateral_sigma_color,
            sigmaSpace=self.bilateral_sigma_space,
        )
