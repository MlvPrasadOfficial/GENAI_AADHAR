"""Confidence calibration using Platt scaling (sigmoid mapping).

Maps raw pipeline confidence into a calibrated probability where
"70% confidence" actually means 70% of such predictions are correct.

Without calibration, the raw score * 100 + bonuses/penalties is an
arbitrary number. Platt scaling fits a sigmoid: P(match) = 1 / (1 + exp(A*s + B))
where A and B are learned from labeled data.

Since we don't have a large labeled dataset, we use hand-tuned parameters
based on the known threshold structure:
  - score 0.60 → ~80% probability (match threshold)
  - score 0.50 → ~50% probability (uncertain midpoint)
  - score 0.40 → ~20% probability (uncertain low)
  - score 0.30 → ~5% probability (definite no-match)

These can be refined later with actual labeled pairs via fit().
"""

import logging
import math

import numpy as np

logger = logging.getLogger(__name__)


class ConfidenceCalibrator:
    """Platt scaling confidence calibrator.

    Usage:
        calibrator = ConfidenceCalibrator(config)
        calibrated = calibrator.calibrate(raw_cosine, quality_factor)
    """

    def __init__(self, config: dict):
        cal_cfg = config.get("calibration", {})
        self.enabled: bool = cal_cfg.get("enabled", False)
        # Platt scaling parameters: P = 1 / (1 + exp(-(A*score + B)))
        # Default: maps 0.60 → ~0.80, 0.50 → ~0.50, 0.40 → ~0.20
        self.platt_a: float = cal_cfg.get("platt_a", 15.0)  # steepness
        self.platt_b: float = cal_cfg.get("platt_b", -7.5)  # offset

    def calibrate(self, score: float, quality_factor: float = 1.0) -> float:
        """Map a raw cosine score to a calibrated probability.

        Args:
            score: Raw cosine similarity in [0, 1].
            quality_factor: Multiplier from image quality (1.0 = good, <1 = poor).

        Returns:
            Calibrated confidence in [0.0, 99.0] (percentage).
        """
        if not self.enabled:
            return score * 100.0

        # Apply quality scaling before calibration
        adjusted = score * quality_factor

        # Platt sigmoid
        logit = self.platt_a * adjusted + self.platt_b
        prob = 1.0 / (1.0 + math.exp(-logit))

        # Scale to percentage, cap at 99%
        calibrated = max(0.0, min(prob * 100.0, 99.0))

        logger.debug(
            "Calibration: raw=%.4f q_adj=%.4f → logit=%.2f → prob=%.4f → %.1f%%",
            score, adjusted, logit, prob, calibrated,
        )

        return calibrated

    def fit(self, scores: list[float], labels: list[bool]) -> tuple[float, float]:
        """Fit Platt parameters from labeled data (cosine scores + ground truth).

        Uses simple logistic regression via Newton's method.

        Args:
            scores: List of raw cosine similarity scores.
            labels: List of ground truth match labels (True = same person).

        Returns:
            Tuple of (A, B) Platt parameters.
        """
        if len(scores) < 10:
            logger.warning("Need at least 10 labeled pairs for calibration fitting")
            return self.platt_a, self.platt_b

        x = np.array(scores, dtype=np.float64)
        y = np.array(labels, dtype=np.float64)

        # Simple iterative Platt scaling (Newton-Raphson)
        a, b = -1.0, 0.0
        lr = 0.01
        for _ in range(1000):
            logits = a * x + b
            probs = 1.0 / (1.0 + np.exp(-logits))
            probs = np.clip(probs, 1e-7, 1 - 1e-7)

            # Gradients
            diff = probs - y
            grad_a = float(np.dot(diff, x))
            grad_b = float(np.sum(diff))

            a -= lr * grad_a
            b -= lr * grad_b

        self.platt_a = float(a)
        self.platt_b = float(b)
        logger.info("Platt calibration fit: A=%.4f, B=%.4f", self.platt_a, self.platt_b)
        return self.platt_a, self.platt_b
