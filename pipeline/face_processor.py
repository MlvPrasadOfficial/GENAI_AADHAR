"""Face detection, alignment, and embedding using InsightFace buffalo_l.

A single FaceAnalysis instance handles all three stages:
  1. RetinaFace-10GF detection → bounding box + confidence
  2. 5-point landmark alignment → 112x112 normalized crop
  3. ArcFace R50 embedding → 512-d L2-normalized vector

The Cython mesh extension is NOT required (patched during installation).
"""

import logging
import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from utils.exceptions import NoFaceDetectedError

logger = logging.getLogger(__name__)


@dataclass
class FaceResult:
    """Output of face detection + alignment + embedding for one image."""

    aligned_crop: np.ndarray   # 112x112 BGR uint8
    embedding: np.ndarray      # (512,) float32, L2-normalized
    bbox: tuple[int, int, int, int]  # (x1, y1, x2, y2)
    det_score: float           # detection confidence [0, 1]


class FaceProcessor:
    """InsightFace buffalo_l wrapper for face detection, alignment, and embedding.

    Usage:
        processor = FaceProcessor(config)
        processor.load()
        result = processor.process(bgr_image, source="aadhaar")
    """

    def __init__(self, config: dict):
        cfg = config["face"]
        self.model_pack: str = cfg["model_pack"]
        self.insightface_root: str = cfg["insightface_root"]
        self.det_size: tuple[int, int] = tuple(cfg["det_size"])
        self.det_thresh: float = cfg["det_thresh"]
        self.det_thresh_fallback: float = cfg.get("det_thresh_fallback", 0.5)
        self.ctx_id: int = cfg["ctx_id"]
        self._app = None

    def load(self) -> None:
        """Initialize InsightFace FaceAnalysis with buffalo_l model pack.

        Sets INSIGHTFACE_ROOT env var so InsightFace looks for models
        in our local models/ directory.
        """
        root = Path(self.insightface_root)
        root.mkdir(parents=True, exist_ok=True)
        os.environ["INSIGHTFACE_ROOT"] = str(root.resolve())

        import insightface

        self._app = insightface.app.FaceAnalysis(
            name=self.model_pack,
            root=str(root.resolve()),
            providers=["CUDAExecutionProvider", "CPUExecutionProvider"],
        )
        self._app.prepare(ctx_id=self.ctx_id, det_size=self.det_size)
        logger.info(
            "InsightFace %s loaded (det_size=%s, ctx_id=%d)",
            self.model_pack, self.det_size, self.ctx_id,
        )

    def process(self, image: np.ndarray, source: str = "image") -> FaceResult:
        """Run full face pipeline: detect → align → embed.

        Args:
            image: BGR uint8 numpy array.
            source: Label for error messages ("aadhaar" or "selfie").

        Returns:
            FaceResult with aligned crop, embedding, bbox, and detection score.

        Raises:
            NoFaceDetectedError: If no face is found after fallback retry.
        """
        if self._app is None:
            raise RuntimeError("FaceProcessor not loaded. Call load() first.")

        # Primary detection at configured threshold
        faces = self._app.get(image)
        faces = [f for f in faces if f.det_score >= self.det_thresh]

        # Fallback: lower threshold if no face found
        if not faces:
            logger.info(
                "No face at det_thresh=%.2f for %s, retrying at %.2f",
                self.det_thresh, source, self.det_thresh_fallback,
            )
            faces = self._app.get(image)
            faces = [f for f in faces if f.det_score >= self.det_thresh_fallback]

        if not faces:
            raise NoFaceDetectedError(
                source,
                f"RetinaFace found no faces above threshold {self.det_thresh_fallback}",
            )

        # Pick the face with the highest detection confidence
        best = max(faces, key=lambda f: f.det_score)
        bbox = tuple(int(x) for x in best.bbox[:4])
        embedding = best.normed_embedding  # already L2-normalized, shape (512,)

        # Get aligned crop from the face's internal representation
        # InsightFace stores the aligned 112x112 in face.normed_embedding's source
        # We reconstruct it from the kps (keypoints) for a clean aligned crop
        from insightface.utils.face_align import norm_crop

        aligned = norm_crop(image, best.kps, image_size=112)

        logger.info(
            "%s: face detected (score=%.3f, bbox=%s)", source, best.det_score, bbox
        )

        return FaceResult(
            aligned_crop=aligned,
            embedding=embedding.astype(np.float32),
            bbox=bbox,
            det_score=float(best.det_score),
        )
