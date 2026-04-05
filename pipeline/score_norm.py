"""S-norm (symmetric score normalization) for calibrating cosine similarity.

Raw cosine scores are not directly comparable across different image
qualities — a 0.55 between two sharp photos means something different
from 0.55 between a blurry Aadhaar card and a selfie.

S-norm normalizes scores against an impostor cohort, producing z-scores
that are quality-independent and statistically meaningful.

Algorithm:
    1. Maintain a cohort of N reference embeddings (from diverse faces)
    2. For probe p and gallery g:
       - Compute cosine(p, g) = raw score
       - Compute cosine(p, cohort_i) for all i → mean_p, std_p
       - Compute cosine(g, cohort_i) for all i → mean_g, std_g
       - z_p = (raw - mean_p) / std_p
       - z_g = (raw - mean_g) / std_g
       - s_norm = (z_p + z_g) / 2

Reference: Auckenthaler et al., "Score Normalization for Text-Independent
Speaker Verification Systems", Digital Signal Processing, 2000.
"""

import logging
from pathlib import Path

import numpy as np

logger = logging.getLogger(__name__)


class SNormCalibrator:
    """Symmetric score normalization using an impostor cohort.

    Usage:
        calibrator = SNormCalibrator(config)
        calibrator.load_cohort()  # or build_cohort_from_embeddings()
        normalized = calibrator.normalize(probe_emb, gallery_emb, raw_score)
    """

    def __init__(self, config: dict):
        snorm_cfg = config.get("score_norm", {})
        self.enabled: bool = snorm_cfg.get("enabled", False)
        self.cohort_path: str = snorm_cfg.get("cohort_path", "models/snorm_cohort.npy")
        self.cohort_size: int = snorm_cfg.get("cohort_size", 100)
        self._cohort: np.ndarray | None = None  # (N, 512)

    def load_cohort(self) -> bool:
        """Load pre-computed impostor cohort from disk.

        Returns:
            True if cohort loaded successfully.
        """
        if not self.enabled:
            return False

        path = Path(self.cohort_path)
        if not path.exists():
            logger.warning(
                "S-norm cohort not found at %s. "
                "Run pipeline in batch mode first to auto-generate, "
                "or disable score_norm in config.",
                path,
            )
            return False

        try:
            self._cohort = np.load(str(path))
            if self._cohort.ndim != 2 or self._cohort.shape[1] != 512:
                logger.error("Invalid cohort shape: %s (expected (N, 512))", self._cohort.shape)
                self._cohort = None
                return False
            logger.info("S-norm cohort loaded: %d embeddings", len(self._cohort))
            return True
        except Exception as e:
            logger.error("Failed to load S-norm cohort: %s", e)
            self._cohort = None
            return False

    def build_cohort_from_embeddings(self, embeddings: list[np.ndarray]) -> None:
        """Build impostor cohort from a list of embeddings.

        Selects up to cohort_size diverse embeddings. Saves to disk for reuse.

        Args:
            embeddings: List of L2-normalized 512-d embeddings.
        """
        if not embeddings:
            logger.warning("No embeddings provided for cohort building")
            return

        # Stack and deduplicate (skip near-identical embeddings)
        all_embs = np.array(embeddings, dtype=np.float32)

        if len(all_embs) <= self.cohort_size:
            self._cohort = all_embs
        else:
            # Greedy diverse selection: pick embeddings that maximize minimum distance
            indices = [0]
            for _ in range(min(self.cohort_size - 1, len(all_embs) - 1)):
                selected = all_embs[indices]
                # Compute min distance from each candidate to selected set
                sims = all_embs @ selected.T  # (N, selected)
                max_sim = sims.max(axis=1)
                # Pick the candidate with lowest max similarity (most diverse)
                max_sim[indices] = 2.0  # exclude already selected
                next_idx = int(np.argmin(max_sim))
                indices.append(next_idx)
            self._cohort = all_embs[indices]

        # Save to disk
        path = Path(self.cohort_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        np.save(str(path), self._cohort)
        logger.info("S-norm cohort built: %d embeddings → %s", len(self._cohort), path)

    def normalize(
        self,
        probe: np.ndarray,
        gallery: np.ndarray,
        raw_score: float,
    ) -> float:
        """Apply S-norm to a raw cosine score.

        Args:
            probe: Probe embedding (512-d, L2-normalized).
            gallery: Gallery embedding (512-d, L2-normalized).
            raw_score: Raw cosine similarity between probe and gallery.

        Returns:
            S-normalized score. Higher = more confident match.
            Falls back to raw_score if cohort unavailable.
        """
        if not self.enabled or self._cohort is None:
            return raw_score

        # Compute probe-vs-cohort scores
        p_scores = self._cohort @ probe  # (N,)
        p_mean, p_std = float(p_scores.mean()), float(p_scores.std())

        # Compute gallery-vs-cohort scores
        g_scores = self._cohort @ gallery  # (N,)
        g_mean, g_std = float(g_scores.mean()), float(g_scores.std())

        # Z-normalize
        z_p = (raw_score - p_mean) / max(p_std, 1e-6)
        z_g = (raw_score - g_mean) / max(g_std, 1e-6)

        # Symmetric combination
        s_norm = (z_p + z_g) / 2.0

        logger.debug(
            "S-norm: raw=%.4f → z_p=%.3f (μ=%.3f σ=%.3f) z_g=%.3f (μ=%.3f σ=%.3f) → snorm=%.4f",
            raw_score, z_p, p_mean, p_std, z_g, g_mean, g_std, s_norm,
        )

        return float(s_norm)

    @property
    def available(self) -> bool:
        """Whether S-norm is enabled and cohort is loaded."""
        return self.enabled and self._cohort is not None
