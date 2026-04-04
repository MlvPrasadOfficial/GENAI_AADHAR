"""Cosine similarity scoring and threshold-based decision logic.

Pure numpy — no GPU or model dependencies. This module is fully unit-testable
without any ML framework installed.
"""

from dataclasses import dataclass

import numpy as np


@dataclass
class SimilarityDecision:
    """Result of the threshold decision tree."""

    verdict: str       # "match" | "no_match" | "uncertain"
    score: float       # raw cosine similarity
    needs_vlm: bool    # whether VLM guard should be invoked
    quality_low: bool  # whether image quality flag was raised


class SimilarityScorer:
    """Computes cosine similarity between two ArcFace embeddings and applies
    threshold logic to produce a match/no-match/uncertain verdict.

    Thresholds (from config):
        match_threshold (0.60): score >= this = definite match
        uncertain_low   (0.40): score < this = definite no-match
        Between these two = uncertain zone -> invoke VLM guard
    """

    def __init__(self, config: dict):
        sim_cfg = config["similarity"]
        self.match_threshold: float = sim_cfg["match_threshold"]
        self.uncertain_low: float = sim_cfg["uncertain_low"]

    def cosine_similarity(self, e1: np.ndarray, e2: np.ndarray) -> float:
        """Compute cosine similarity between two L2-normalized embeddings.

        Since InsightFace's normed_embedding is already L2-normalized,
        the dot product equals cosine similarity.

        Args:
            e1: First embedding, shape (512,), L2-normalized float32.
            e2: Second embedding, shape (512,), L2-normalized float32.

        Returns:
            Cosine similarity clamped to [0.0, 1.0].
        """
        return float(np.clip(np.dot(e1, e2), 0.0, 1.0))

    def decide(self, score: float, quality_low: bool = False) -> SimilarityDecision:
        """Apply threshold decision tree.

        Args:
            score: Cosine similarity from cosine_similarity().
            quality_low: True if either input image had low quality score.

        Returns:
            SimilarityDecision with verdict, whether VLM is needed, etc.
        """
        if score >= self.match_threshold:
            if quality_low:
                # High score but bad image quality — verify with VLM
                return SimilarityDecision("match", score, needs_vlm=True, quality_low=True)
            return SimilarityDecision("match", score, needs_vlm=False, quality_low=False)

        if score >= self.uncertain_low:
            # Uncertain zone — must invoke VLM
            return SimilarityDecision("uncertain", score, needs_vlm=True, quality_low=quality_low)

        # Below uncertain_low — definite no-match
        return SimilarityDecision("no_match", score, needs_vlm=False, quality_low=quality_low)
