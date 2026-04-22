"""Secondary face recognition model for ensemble cosine fusion.

Loads a second InsightFace model pack (default: antelopev2 — SCRFD-10G detector
+ glintr100 ArcFace trained on Glint360K) and exposes just the recognition
head. We reuse the aligned crop produced by the primary buffalo_l pipeline
rather than re-running detection, which avoids duplicated compute and keeps
both embeddings tied to the same aligned face.

Degrades gracefully: if weights are missing or loading fails, the ensemble
falls back to primary-only scoring.
"""

import logging
import os
from pathlib import Path

import numpy as np

logger = logging.getLogger(__name__)


class SecondaryFaceEmbedder:
    """Loads a second InsightFace recognition model and embeds aligned crops.

    Usage:
        emb = SecondaryFaceEmbedder(config)
        emb.load()
        if emb.available:
            vec = emb.get_embedding(aligned_112x112_bgr)
    """

    def __init__(self, config: dict):
        face_cfg = config.get("face", {})
        self.enabled: bool = face_cfg.get("enable_ensemble", False)
        self.model_pack: str = face_cfg.get("secondary_model", "antelopev2")
        self.insightface_root: str = face_cfg.get("insightface_root", "models/insightface")
        self.ctx_id: int = face_cfg.get("ctx_id", 0)
        self._rec_model = None

    def load(self) -> None:
        """Load the secondary recognition model. Safe to call at startup."""
        if not self.enabled:
            logger.debug("Secondary face model disabled in config")
            return

        try:
            root = Path(self.insightface_root).resolve()
            root.mkdir(parents=True, exist_ok=True)
            os.environ["INSIGHTFACE_ROOT"] = str(root)

            import insightface

            app = insightface.app.FaceAnalysis(
                name=self.model_pack,
                root=str(root),
                providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
            )
            app.prepare(ctx_id=self.ctx_id, det_size=(320, 320))

            for model in app.models.values():
                if hasattr(model, "taskname") and model.taskname == "recognition":
                    self._rec_model = model
                    break

            if self._rec_model is None:
                logger.warning(
                    "Secondary model pack %s has no recognition head — disabled",
                    self.model_pack,
                )
                self.enabled = False
                return

            logger.info(
                "Secondary face model loaded: pack=%s recognition=%s",
                self.model_pack, type(self._rec_model).__name__,
            )

        except Exception as e:
            logger.warning(
                "Secondary face model load failed (%s) — ensemble disabled",
                e,
            )
            self.enabled = False

    def get_embedding(self, aligned_crop: np.ndarray) -> np.ndarray | None:
        """Extract an L2-normalized embedding from a 112x112 aligned BGR crop.

        Returns None if the model is unavailable or the embedding is degenerate.
        """
        if not self.available or aligned_crop is None:
            return None
        try:
            feat = self._rec_model.get_feat(aligned_crop)
            emb = feat.flatten().astype(np.float32)
            norm = np.linalg.norm(emb)
            if norm < 1e-6:
                return None
            return emb / norm
        except Exception as e:
            logger.warning("Secondary embedding extraction failed: %s", e)
            return None

    @property
    def available(self) -> bool:
        return self.enabled and self._rec_model is not None
