"""AdaFace integration — quality-adaptive face recognition as second model.

AdaFace adapts its feature extraction based on image quality, producing
better embeddings for low-quality inputs. When paired with ArcFace (primary),
the two-model ensemble provides:
  1. Cross-validation: two models agreeing = high confidence
  2. Quality robustness: AdaFace excels on degraded Aadhaar card images
  3. Score fusion: weighted average or min-of-two for final similarity

This module loads a pretrained AdaFace IR-101 model (if available) and
provides the same embedding interface as the primary ArcFace pipeline.
Gracefully degrades if model weights are missing.

Model download: https://github.com/mk-minchul/AdaFace
Expected path: models/adaface/adaface_ir101_webface12m.ckpt
"""

import logging
from pathlib import Path

import cv2
import numpy as np

logger = logging.getLogger(__name__)


class AdaFaceModel:
    """AdaFace quality-adaptive face recognition model.

    Usage:
        model = AdaFaceModel(config)
        model.load()
        if model.available:
            embedding = model.get_embedding(aligned_112x112_crop)
    """

    def __init__(self, config: dict):
        ada_cfg = config.get("adaface", {})
        self.enabled: bool = ada_cfg.get("enabled", False)
        self.model_path: str = ada_cfg.get(
            "model_path", "models/adaface/adaface_ir101_webface12m.ckpt"
        )
        self.fusion_weight: float = ada_cfg.get("fusion_weight", 0.3)
        self._model = None
        self._transform = None

    def load(self) -> None:
        """Load AdaFace model weights."""
        if not self.enabled:
            logger.debug("AdaFace disabled in config")
            return

        model_path = Path(self.model_path)
        if not model_path.exists():
            logger.warning(
                "AdaFace model not found at %s — feature disabled. "
                "Download from https://github.com/mk-minchul/AdaFace",
                model_path,
            )
            self.enabled = False
            return

        try:
            import torch
            # Try to import AdaFace model architecture
            self._load_model(model_path)
            logger.info("AdaFace loaded from %s", model_path)
        except ImportError:
            logger.warning("PyTorch not available for AdaFace — feature disabled")
            self.enabled = False
        except Exception as e:
            logger.warning("AdaFace load failed: %s — feature disabled", e)
            self.enabled = False

    def _load_model(self, model_path: Path) -> None:
        """Load the AdaFace checkpoint."""
        import torch

        # AdaFace uses a standard IResNet architecture
        # We load just the state dict and run inference
        checkpoint = torch.load(str(model_path), map_location="cpu", weights_only=False)
        if "state_dict" in checkpoint:
            state_dict = checkpoint["state_dict"]
        else:
            state_dict = checkpoint

        # Try to load as a standard IR network
        try:
            from pipeline._adaface_ir import IR_101
            model = IR_101((112, 112))
            # Remove 'model.' prefix from state dict keys if present
            cleaned = {}
            for k, v in state_dict.items():
                key = k.replace("model.", "") if k.startswith("model.") else k
                cleaned[key] = v
            model.load_state_dict(cleaned, strict=False)
            model.eval()
            if torch.cuda.is_available():
                model = model.cuda()
            self._model = model
        except (ImportError, RuntimeError) as e:
            logger.warning("AdaFace architecture not available: %s", e)
            self.enabled = False

    def get_embedding(self, aligned_crop: np.ndarray) -> np.ndarray | None:
        """Extract 512-d embedding from a 112x112 aligned face crop.

        Args:
            aligned_crop: 112x112 BGR uint8 image.

        Returns:
            L2-normalized 512-d float32 embedding, or None if unavailable.
        """
        if not self.available or aligned_crop is None:
            return None

        import torch

        # Preprocess: BGR→RGB, normalize to [-1, 1], CHW, batch
        rgb = cv2.cvtColor(aligned_crop, cv2.COLOR_BGR2RGB)
        img = rgb.astype(np.float32) / 255.0
        img = (img - 0.5) / 0.5  # normalize to [-1, 1]
        img = np.transpose(img, (2, 0, 1))  # HWC → CHW
        tensor = torch.from_numpy(img).unsqueeze(0)  # add batch dim

        if torch.cuda.is_available():
            tensor = tensor.cuda()

        with torch.no_grad():
            embedding = self._model(tensor)
            if isinstance(embedding, tuple):
                embedding = embedding[0]
            emb = embedding.cpu().numpy().flatten().astype(np.float32)

        norm = np.linalg.norm(emb)
        if norm < 1e-6:
            return None
        return emb / norm

    def fuse_scores(
        self,
        arcface_score: float,
        adaface_score: float,
    ) -> float:
        """Fuse ArcFace and AdaFace similarity scores.

        Uses weighted average with configurable weight.

        Args:
            arcface_score: Primary ArcFace cosine similarity.
            adaface_score: AdaFace cosine similarity.

        Returns:
            Fused similarity score in [0, 1].
        """
        w = self.fusion_weight
        fused = (1 - w) * arcface_score + w * adaface_score
        return float(np.clip(fused, 0.0, 1.0))

    @property
    def available(self) -> bool:
        """Whether AdaFace is enabled and model is loaded."""
        return self.enabled and self._model is not None
