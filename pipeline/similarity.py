"""Cosine similarity scoring, multi-signal metrics, and threshold-based decision logic.

Pure numpy + cv2 — no GPU or model dependencies. This module is fully unit-testable
without any ML framework installed.

Similarity signals:
    1. Cosine similarity  — ArcFace embedding dot product (primary)
    2. L2 distance        — Euclidean distance between embeddings (secondary)
    3. SSIM               — Structural Similarity Index on aligned 112x112 crops
    4. Landmark geometry   — Facial ratio comparison from 68-point 3D landmarks
    5. Fused score        — Weighted combination of all signals
"""

import logging
from dataclasses import dataclass, field
from typing import Literal

import cv2
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class SimilarityDecision:
    """Result of the threshold decision tree."""

    verdict: Literal["match", "no_match", "uncertain"]
    score: float       # raw cosine similarity
    needs_vlm: bool    # whether VLM guard should be invoked
    quality_low: bool  # whether image quality flag was raised


@dataclass
class MultiMetricResult:
    """All similarity metrics computed between two faces."""

    cosine: float               # ArcFace cosine similarity [0, 1]
    l2_distance: float          # Euclidean distance (lower = more similar)
    l2_score: float             # L2 mapped to [0, 1] similarity score
    ssim: float                 # Structural similarity index [-1, 1]
    landmark_score: float       # Facial geometry ratio similarity [0, 1] or -1 if unavailable
    pose_diff: float            # Face pose angle difference in degrees, or -1
    fused_score: float          # Weighted combination of all signals [0, 1]
    details: dict = field(default_factory=dict)  # per-ratio breakdown


# 68-point landmark indices (standard face landmark mapping)
# Jawline: 0-16, Right eyebrow: 17-21, Left eyebrow: 22-26
# Nose bridge: 27-30, Nose tip: 31-35, Right eye: 36-41, Left eye: 42-47
# Outer lip: 48-59, Inner lip: 60-67
_LMK = {
    "right_eye_outer": 36, "right_eye_inner": 39,
    "left_eye_inner": 42, "left_eye_outer": 45,
    "nose_bridge_top": 27, "nose_tip": 30,
    "nose_left": 31, "nose_right": 35,
    "mouth_left": 48, "mouth_right": 54,
    "mouth_top": 51, "mouth_bottom": 57,
    "jaw_left": 0, "jaw_right": 16, "jaw_bottom": 8,
    "right_brow_inner": 21, "left_brow_inner": 22,
    "right_brow_outer": 17, "left_brow_outer": 26,
}


def _dist(p1: np.ndarray, p2: np.ndarray) -> float:
    """Euclidean distance between two 2D/3D points."""
    return float(np.linalg.norm(p1 - p2))


def compute_landmark_ratios(lmk: np.ndarray) -> dict[str, float]:
    """Compute age-invariant facial ratios from 68-point landmarks.

    These ratios capture bone-structure geometry that doesn't change
    with aging, weight changes, or cosmetic differences.

    Args:
        lmk: (68, 3) or (68, 2) landmark array.

    Returns:
        Dict of named ratios (all dimensionless, scale-invariant).
    """
    if lmk is None or lmk.shape[0] < 68:
        return {}

    pts = lmk[:, :2]  # use 2D (x, y) only for ratio computation

    # Key distances
    ipd = _dist(pts[36], pts[45])  # inter-pupillary distance (normalizer)
    if ipd < 1e-6:
        return {}

    # Right eye center and left eye center
    r_eye = pts[36:42].mean(axis=0)
    l_eye = pts[42:48].mean(axis=0)

    ratios = {
        # Eye geometry
        "eye_width_ratio": _dist(pts[36], pts[39]) / ipd,          # right eye width / IPD
        "eye_spacing_ratio": _dist(pts[39], pts[42]) / ipd,        # inner eye spacing / IPD
        # Nose geometry
        "nose_bridge_len": _dist(pts[27], pts[30]) / ipd,          # nose bridge length / IPD
        "nose_width": _dist(pts[31], pts[35]) / ipd,               # nose width / IPD
        "nose_to_eye": _dist(pts[27], (r_eye + l_eye) / 2) / ipd,  # nose top to eye midpoint / IPD
        # Mouth geometry
        "mouth_width": _dist(pts[48], pts[54]) / ipd,              # mouth width / IPD
        "mouth_height": _dist(pts[51], pts[57]) / ipd,             # mouth height / IPD
        "nose_to_mouth": _dist(pts[30], pts[51]) / ipd,            # nose tip to upper lip / IPD
        # Face proportions
        "jaw_width": _dist(pts[0], pts[16]) / ipd,                 # jaw width / IPD
        "face_height": _dist((pts[17] + pts[26]) / 2, pts[8]) / ipd,  # brow midpoint to chin / IPD
        # Brow geometry
        "brow_spacing": _dist(pts[21], pts[22]) / ipd,             # inner brow spacing / IPD
        "brow_to_eye": _dist(pts[21], pts[39]) / ipd,              # right brow to right eye inner / IPD
    }
    return ratios


def compare_landmark_ratios(
    ratios1: dict[str, float],
    ratios2: dict[str, float],
) -> tuple[float, dict[str, float]]:
    """Compare two sets of facial ratios and return a similarity score.

    Args:
        ratios1: Facial ratios from face 1.
        ratios2: Facial ratios from face 2.

    Returns:
        (score, per_ratio_diff) where score is in [0, 1] (1 = identical geometry)
        and per_ratio_diff maps ratio names to absolute differences.
    """
    if not ratios1 or not ratios2:
        return -1.0, {}

    common_keys = set(ratios1.keys()) & set(ratios2.keys())
    if not common_keys:
        return -1.0, {}

    diffs = {}
    for key in sorted(common_keys):
        diffs[key] = abs(ratios1[key] - ratios2[key])

    # Average ratio difference — convert to similarity score
    # Typical same-person diff is < 0.05, different person > 0.10
    avg_diff = sum(diffs.values()) / len(diffs)
    # Map: 0 diff → 1.0 score, 0.15+ diff → ~0.0 score (sigmoid-like)
    score = float(np.exp(-avg_diff * 20.0))  # e^(-20*diff)
    return min(max(score, 0.0), 1.0), diffs


def compute_ssim(crop1: np.ndarray, crop2: np.ndarray) -> float:
    """Compute Structural Similarity Index between two aligned face crops.

    Converts to grayscale and uses OpenCV's matchTemplate-based approach
    for a simplified but effective SSIM.

    Args:
        crop1: 112x112 BGR uint8 aligned face.
        crop2: 112x112 BGR uint8 aligned face.

    Returns:
        SSIM value in [-1, 1] (higher = more similar).
    """
    if crop1 is None or crop2 is None:
        return 0.0
    if crop1.shape != crop2.shape:
        return 0.0

    gray1 = cv2.cvtColor(crop1, cv2.COLOR_BGR2GRAY).astype(np.float64)
    gray2 = cv2.cvtColor(crop2, cv2.COLOR_BGR2GRAY).astype(np.float64)

    c1 = (0.01 * 255) ** 2  # stabilizer constants
    c2 = (0.03 * 255) ** 2

    mu1 = cv2.GaussianBlur(gray1, (11, 11), 1.5)
    mu2 = cv2.GaussianBlur(gray2, (11, 11), 1.5)

    mu1_sq = mu1 ** 2
    mu2_sq = mu2 ** 2
    mu1_mu2 = mu1 * mu2

    sigma1_sq = cv2.GaussianBlur(gray1 ** 2, (11, 11), 1.5) - mu1_sq
    sigma2_sq = cv2.GaussianBlur(gray2 ** 2, (11, 11), 1.5) - mu2_sq
    sigma12 = cv2.GaussianBlur(gray1 * gray2, (11, 11), 1.5) - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + c1) * (2 * sigma12 + c2)) / \
               ((mu1_sq + mu2_sq + c1) * (sigma1_sq + sigma2_sq + c2))

    return float(ssim_map.mean())


class SimilarityScorer:
    """Computes cosine similarity between two ArcFace embeddings and applies
    threshold logic to produce a match/no-match/uncertain verdict.

    Also computes secondary metrics: L2 distance, SSIM, landmark geometry,
    and a fused score combining all signals.

    Thresholds (from config):
        match_threshold (0.60): score >= this = definite match
        uncertain_low   (0.40): score < this = definite no-match
        Between these two = uncertain zone -> invoke VLM guard
    """

    # Default fusion weights (configurable via config.yaml)
    DEFAULT_WEIGHTS = {
        "cosine": 0.55,
        "l2": 0.10,
        "ssim": 0.10,
        "landmark": 0.25,
    }

    # Adaptive threshold tiers: quality_min → (match_threshold, uncertain_low)
    DEFAULT_QUALITY_TIERS = [
        # (min_quality, match_thresh, uncertain_low)
        (0.7, 0.65, 0.45),   # high quality: stricter thresholds
        (0.4, 0.60, 0.40),   # medium quality: standard thresholds
        (0.0, 0.55, 0.35),   # low quality: relaxed thresholds
    ]

    def __init__(self, config: dict):
        sim_cfg = config["similarity"]
        self.match_threshold: float = sim_cfg["match_threshold"]
        self.uncertain_low: float = sim_cfg["uncertain_low"]
        self.fusion_weights: dict[str, float] = sim_cfg.get(
            "fusion_weights", self.DEFAULT_WEIGHTS
        )
        # Adaptive thresholds
        self.adaptive_thresholds: bool = sim_cfg.get("adaptive_thresholds", False)
        self.quality_tiers: list = sim_cfg.get("quality_tiers", self.DEFAULT_QUALITY_TIERS)
        # Quality-weighted fusion
        self.quality_weighted_fusion: bool = sim_cfg.get("quality_weighted_fusion", False)

    def cosine_similarity(self, e1: np.ndarray, e2: np.ndarray) -> float:
        """Compute cosine similarity between two L2-normalized embeddings.

        Since InsightFace's normed_embedding is already L2-normalized,
        the dot product equals cosine similarity.

        Args:
            e1: First embedding, shape (512,), L2-normalized float32.
            e2: Second embedding, shape (512,), L2-normalized float32.

        Returns:
            Cosine similarity clamped to [0.0, 1.0].

        Raises:
            ValueError: If embeddings have mismatched shapes.
        """
        if e1.shape != e2.shape:
            raise ValueError(f"Embedding shape mismatch: {e1.shape} vs {e2.shape}")
        return float(np.clip(np.dot(e1, e2), 0.0, 1.0))

    def get_adaptive_thresholds(self, quality: float) -> tuple[float, float]:
        """Return (match_threshold, uncertain_low) adapted to image quality.

        Higher quality images get stricter thresholds (fewer false positives),
        lower quality images get relaxed thresholds (fewer false negatives).

        Args:
            quality: Minimum quality score of the two images, in [0, 1].

        Returns:
            (match_threshold, uncertain_low) for this quality level.
        """
        if not self.adaptive_thresholds:
            return self.match_threshold, self.uncertain_low

        for min_q, mt, ul in self.quality_tiers:
            if quality >= min_q:
                return mt, ul
        return self.match_threshold, self.uncertain_low

    def get_quality_adjusted_weights(
        self, quality: float,
    ) -> dict[str, float]:
        """Return fusion weights adjusted for image quality.

        Low quality → increase landmark weight (bone structure is stable),
        decrease SSIM weight (noisy images produce unreliable SSIM).

        Args:
            quality: Minimum quality score of the two images, in [0, 1].

        Returns:
            Adjusted fusion weight dict.
        """
        if not self.quality_weighted_fusion:
            return self.fusion_weights

        w = dict(self.fusion_weights)

        if quality < 0.3:
            # Very low quality: rely heavily on cosine + landmarks
            w["cosine"] = 0.50
            w["landmark"] = 0.35
            w["l2"] = 0.10
            w["ssim"] = 0.05
        elif quality < 0.5:
            # Low-medium quality: boost landmarks slightly
            w["cosine"] = 0.50
            w["landmark"] = 0.30
            w["l2"] = 0.10
            w["ssim"] = 0.10

        return w

    def decide(self, score: float, quality_low: bool = False,
               quality_score: float = 1.0) -> SimilarityDecision:
        """Apply threshold decision tree.

        Args:
            score: Cosine similarity from cosine_similarity().
            quality_low: True if either input image had low quality score.
            quality_score: Min quality of the two images for adaptive thresholds.

        Returns:
            SimilarityDecision with verdict, whether VLM is needed, etc.
        """
        match_thresh, unc_low = self.get_adaptive_thresholds(quality_score)

        if score >= match_thresh:
            if quality_low:
                # High score but bad image quality — verify with VLM
                return SimilarityDecision("match", score, needs_vlm=True, quality_low=True)
            return SimilarityDecision("match", score, needs_vlm=False, quality_low=False)

        if score >= unc_low:
            # Uncertain zone — must invoke VLM
            return SimilarityDecision("uncertain", score, needs_vlm=True, quality_low=quality_low)

        # Below uncertain_low — definite no-match
        return SimilarityDecision("no_match", score, needs_vlm=False, quality_low=quality_low)

    def l2_distance(self, e1: np.ndarray, e2: np.ndarray) -> float:
        """Compute L2 (Euclidean) distance between two embeddings.

        For L2-normalized embeddings: L2 = sqrt(2 - 2*cosine).
        Range: [0, 2] where 0 = identical, 2 = opposite.
        """
        if e1.shape != e2.shape:
            raise ValueError(f"Embedding shape mismatch: {e1.shape} vs {e2.shape}")
        return float(np.linalg.norm(e1 - e2))

    def l2_to_score(self, l2_dist: float) -> float:
        """Convert L2 distance to a [0, 1] similarity score.

        Maps [0, 2] → [1, 0] using exponential decay.
        """
        return float(np.exp(-l2_dist * 1.5))

    def compute_all_metrics(
        self,
        face1,
        face2,
        quality: float = 1.0,
    ) -> MultiMetricResult:
        """Compute all similarity metrics between two FaceResults.

        Args:
            face1: FaceResult from Aadhaar processing.
            face2: FaceResult from selfie processing.

        Returns:
            MultiMetricResult with all signals and fused score.
        """
        # 1. Cosine similarity (primary)
        cosine = self.cosine_similarity(face1.embedding, face2.embedding)

        # 2. L2 distance
        l2_dist = self.l2_distance(face1.embedding, face2.embedding)
        l2_score = self.l2_to_score(l2_dist)

        # 3. SSIM on aligned crops
        ssim = compute_ssim(face1.aligned_crop, face2.aligned_crop)

        # 4. Landmark geometry ratios
        lmk1 = getattr(face1, "landmark_3d_68", None)
        lmk2 = getattr(face2, "landmark_3d_68", None)
        ratios1 = compute_landmark_ratios(lmk1)
        ratios2 = compute_landmark_ratios(lmk2)
        landmark_score, ratio_diffs = compare_landmark_ratios(ratios1, ratios2)

        # 5. Pose difference
        pose1 = getattr(face1, "pose", None)
        pose2 = getattr(face2, "pose", None)
        pose_diff = -1.0
        if pose1 is not None and pose2 is not None:
            pose_diff = float(np.linalg.norm(pose1 - pose2))

        # 6. Fused score (weighted combination, quality-adjusted)
        w = self.get_quality_adjusted_weights(quality)
        total_weight = 0.0
        fused = 0.0

        fused += w.get("cosine", 0.55) * cosine
        total_weight += w.get("cosine", 0.55)

        fused += w.get("l2", 0.10) * l2_score
        total_weight += w.get("l2", 0.10)

        fused += w.get("ssim", 0.10) * max(ssim, 0.0)  # clamp negative SSIM
        total_weight += w.get("ssim", 0.10)

        if landmark_score >= 0:
            fused += w.get("landmark", 0.25) * landmark_score
            total_weight += w.get("landmark", 0.25)

        fused_score = fused / total_weight if total_weight > 0 else cosine

        details = {
            "ratios_face1": ratios1,
            "ratios_face2": ratios2,
            "ratio_diffs": ratio_diffs,
        }

        logger.info(
            "Multi-metric: cosine=%.4f l2=%.4f(%.3f) ssim=%.4f landmark=%.4f pose_diff=%.1f fused=%.4f",
            cosine, l2_dist, l2_score, ssim, landmark_score, pose_diff, fused_score,
        )

        return MultiMetricResult(
            cosine=cosine,
            l2_distance=l2_dist,
            l2_score=l2_score,
            ssim=ssim,
            landmark_score=landmark_score,
            pose_diff=pose_diff,
            fused_score=fused_score,
            details=details,
        )



