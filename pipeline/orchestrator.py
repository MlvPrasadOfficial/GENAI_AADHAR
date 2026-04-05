"""Pipeline orchestrator — wires all stages together into a single run() call.

Pipeline flow:
    bytes_to_bgr → quality assessment → maybe_enhance → face detect+align+embed
    → cosine similarity → threshold decision → (optional VLM guard) → PipelineResult
"""

import logging
import time
from dataclasses import dataclass, field

import numpy as np

from pipeline.enhancement import ImageEnhancer
from pipeline.face_processor import FaceProcessor
from pipeline.similarity import SimilarityScorer
from pipeline.vlm_guard import VLMGuard
from utils.exceptions import NoFaceDetectedError, PipelineError
from utils.image_utils import bytes_to_bgr

logger = logging.getLogger(__name__)


@dataclass
class PipelineResult:
    """Final output of the face matching pipeline."""

    match: bool
    confidence_pct: float           # 0.0 – 99.0
    cosine_score: float             # raw ArcFace cosine similarity
    vlm_same_person: bool | None    # None = VLM not invoked or unavailable
    vlm_reasoning: str | None
    stage_timings: dict[str, float] = field(default_factory=dict)  # ms per stage
    aadhaar_quality: float = 0.0
    selfie_quality: float = 0.0
    aadhaar_crop: np.ndarray | None = None  # 112x112 BGR aligned face crop
    selfie_crop: np.ndarray | None = None   # 112x112 BGR aligned face crop
    aadhaar_gender: str = "unknown"
    aadhaar_age: int = 0
    selfie_gender: str = "unknown"
    selfie_age: int = 0
    aadhaar_num_faces: int = 1
    selfie_num_faces: int = 1
    error: str | None = None        # non-None if pipeline failed


class KYCPipelineOrchestrator:
    """End-to-end Aadhaar KYC face matching pipeline.

    Usage:
        pipeline = KYCPipelineOrchestrator(config)
        pipeline.load()  # once at startup
        result = pipeline.run(aadhaar_bytes, selfie_bytes)
    """

    def __init__(self, config: dict):
        self.config = config
        self.enhancer = ImageEnhancer(config)
        self.processor = FaceProcessor(config)
        self.scorer = SimilarityScorer(config)
        self.vlm = VLMGuard(config)

        # Configurable confidence adjustments
        ca = config.get("confidence_adjustments", {})
        self._vlm_confirm_bonus: float = ca.get("vlm_confirmation_bonus", 8.0)
        self._vlm_reject_high: float = ca.get("vlm_rejection_above_threshold", -20.0)
        self._vlm_reject_uncertain: float = ca.get("vlm_rejection_uncertain", -10.0)
        self._quality_penalty: float = ca.get("quality_penalty", -5.0)
        self._age_gap_vlm_bonus: float = ca.get("age_gap_vlm_bonus", 5.0)
        self._gender_mismatch_penalty: float = ca.get("gender_mismatch_penalty", 0.0)

        # Age-gap threshold relaxation
        sim = config.get("similarity", {})
        self._age_gap_threshold: int = sim.get("age_gap_threshold", 5)
        self._age_relaxation_per_year: float = sim.get("age_gap_relaxation_per_year", 0.01)
        self._max_age_relaxation: float = sim.get("max_age_gap_relaxation", 0.10)

    def load(self) -> None:
        """Load all model weights. Call once at startup."""
        logger.info("Loading pipeline models...")
        self.enhancer.load()
        self.processor.load()
        logger.info("Pipeline ready")

    def run(self, aadhaar_bytes: bytes, selfie_bytes: bytes) -> PipelineResult:
        """Execute the full face matching pipeline.

        Args:
            aadhaar_bytes: Raw bytes of Aadhaar card image (JPEG/PNG).
            selfie_bytes: Raw bytes of user selfie (JPEG/PNG).

        Returns:
            PipelineResult with match decision, confidence, and metadata.
        """
        timings: dict[str, float] = {}
        vlm_same_person = None
        vlm_reasoning = None
        aadhaar_quality = 0.0
        selfie_quality = 0.0

        try:
            # --- Stage 1: Load and EXIF-correct images ---
            t0 = time.perf_counter()
            aadhaar_img = bytes_to_bgr(aadhaar_bytes)
            selfie_img = bytes_to_bgr(selfie_bytes)
            timings["load_ms"] = _elapsed_ms(t0)

            # --- Stage 2: Quality assessment + enhancement ---
            t0 = time.perf_counter()
            aadhaar_img, aadhaar_quality = self.enhancer.maybe_enhance(aadhaar_img)
            selfie_img, selfie_quality = self.enhancer.maybe_enhance(selfie_img)
            timings["enhancement_ms"] = _elapsed_ms(t0)

            # Re-assess quality AFTER enhancement to avoid false flags
            # (pre-enhancement score is stored for reporting, post for decision)
            aadhaar_post_q = self.enhancer.quality_score(aadhaar_img)
            selfie_post_q = self.enhancer.quality_score(selfie_img)
            quality_low = aadhaar_post_q < self.enhancer.quality_threshold or \
                          selfie_post_q < self.enhancer.quality_threshold

            # --- Stage 3: Face detection + alignment + embedding ---
            t0 = time.perf_counter()
            aadhaar_face = self.processor.process(aadhaar_img, source="aadhaar")
            selfie_face = self.processor.process(selfie_img, source="selfie")
            timings["face_processing_ms"] = _elapsed_ms(t0)

            # --- Stage 4: Cosine similarity ---
            t0 = time.perf_counter()
            score = self.scorer.cosine_similarity(
                aadhaar_face.embedding, selfie_face.embedding
            )
            decision = self.scorer.decide(score, quality_low=quality_low)
            timings["similarity_ms"] = _elapsed_ms(t0)

            logger.info(
                "Cosine=%.4f verdict=%s needs_vlm=%s",
                score, decision.verdict, decision.needs_vlm,
            )

            # --- Stage 5: VLM guard (conditional) ---
            if decision.needs_vlm and self.vlm.enabled:
                t0 = time.perf_counter()
                verdict = self.vlm.verify(
                    aadhaar_face.aligned_crop,
                    selfie_face.aligned_crop,
                    cosine_score=score,
                    aadhaar_age=aadhaar_face.age,
                    selfie_age=selfie_face.age,
                )
                timings["vlm_ms"] = _elapsed_ms(t0)
                vlm_same_person = verdict.same_person
                vlm_reasoning = verdict.reasoning

                logger.info(
                    "VLM: same_person=%s confidence=%s reasoning=%s",
                    verdict.same_person, verdict.confidence, verdict.reasoning,
                )

            # --- Stage 6: Final decision fusion ---
            age_gap = abs(aadhaar_face.age - selfie_face.age)
            gender_mismatch = (
                aadhaar_face.gender != selfie_face.gender
                and aadhaar_face.gender != "unknown"
                and selfie_face.gender != "unknown"
            )
            match, confidence_pct = self._fuse_decision(
                score, decision, vlm_same_person,
                age_gap=age_gap, gender_mismatch=gender_mismatch,
            )

            return PipelineResult(
                match=match,
                confidence_pct=confidence_pct,
                cosine_score=score,
                vlm_same_person=vlm_same_person,
                vlm_reasoning=vlm_reasoning,
                stage_timings=timings,
                aadhaar_quality=aadhaar_quality,
                selfie_quality=selfie_quality,
                aadhaar_crop=aadhaar_face.aligned_crop,
                selfie_crop=selfie_face.aligned_crop,
                aadhaar_gender=aadhaar_face.gender,
                aadhaar_age=aadhaar_face.age,
                selfie_gender=selfie_face.gender,
                selfie_age=selfie_face.age,
                aadhaar_num_faces=aadhaar_face.num_faces_detected,
                selfie_num_faces=selfie_face.num_faces_detected,
            )

        except NoFaceDetectedError as e:
            logger.error("Face detection failed: %s", e)
            return PipelineResult(
                match=False, confidence_pct=0.0, cosine_score=0.0,
                vlm_same_person=None, vlm_reasoning=None,
                stage_timings=timings,
                aadhaar_quality=aadhaar_quality,
                selfie_quality=selfie_quality,
                error=str(e),
            )
        except PipelineError as e:
            logger.error("Pipeline error: %s", e)
            return PipelineResult(
                match=False, confidence_pct=0.0, cosine_score=0.0,
                vlm_same_person=None, vlm_reasoning=None,
                stage_timings=timings,
                aadhaar_quality=aadhaar_quality,
                selfie_quality=selfie_quality,
                error=str(e),
            )
        except (ValueError, OSError) as e:
            logger.error("Image loading error: %s", e)
            return PipelineResult(
                match=False, confidence_pct=0.0, cosine_score=0.0,
                vlm_same_person=None, vlm_reasoning=None,
                stage_timings=timings,
                aadhaar_quality=aadhaar_quality,
                selfie_quality=selfie_quality,
                error=f"Invalid image: {e}",
            )
        except Exception as e:
            logger.error("Unexpected error: %s", e, exc_info=True)
            return PipelineResult(
                match=False, confidence_pct=0.0, cosine_score=0.0,
                vlm_same_person=None, vlm_reasoning=None,
                stage_timings=timings,
                aadhaar_quality=aadhaar_quality,
                selfie_quality=selfie_quality,
                error=f"Unexpected error: {type(e).__name__}",
            )

    def _compute_age_relaxation(self, age_gap: int) -> float:
        """Compute threshold relaxation amount based on age gap.

        Returns a non-negative float to subtract from match_threshold.
        """
        if age_gap <= self._age_gap_threshold:
            return 0.0
        excess = age_gap - self._age_gap_threshold
        return min(excess * self._age_relaxation_per_year, self._max_age_relaxation)

    def _fuse_decision(
        self,
        score: float,
        decision,
        vlm_same_person: bool | None,
        age_gap: int = 0,
        gender_mismatch: bool = False,
    ) -> tuple[bool, float]:
        """Combine cosine score and VLM verdict into final match + confidence.

        Decision logic (thresholds from config):
            score >= match_threshold + quality OK (no VLM) → MATCH
            score >= match_threshold + quality LOW + VLM:
                VLM says no → NO MATCH
                VLM unavailable → MATCH (trust the high score)
                VLM says yes → MATCH
            uncertain_low–match_threshold + VLM says yes → MATCH
            uncertain_low–match_threshold + VLM unavailable → NO MATCH (conservative)
            uncertain_low–match_threshold + VLM says no → NO MATCH
            < uncertain_low → NO MATCH (no VLM)

        When age_gap > age_gap_threshold, match_threshold and uncertain_low
        are relaxed proportionally (see _compute_age_relaxation).

        Confidence adjustments are configurable via config.yaml
        confidence_adjustments section. Final clamped to [0.0, 99.0].

        Returns:
            (match: bool, confidence_pct: float)
        """
        relaxation = self._compute_age_relaxation(age_gap)
        match_thresh = self.scorer.match_threshold - relaxation
        uncertain_low = self.scorer.uncertain_low - relaxation
        base_conf = score * 100.0

        if relaxation > 0:
            logger.info(
                "Age gap %dyr → threshold relaxed by %.3f (effective: match=%.3f, uncertain_low=%.3f)",
                age_gap, relaxation, match_thresh, uncertain_low,
            )

        if score >= match_thresh:
            if vlm_same_person is False:
                match = False
                confidence_pct = base_conf + self._vlm_reject_high
            else:
                match = True
                vlm_bonus = self._vlm_confirm_bonus if vlm_same_person is True else 0.0
                if vlm_same_person is True and age_gap > self._age_gap_threshold:
                    vlm_bonus += self._age_gap_vlm_bonus
                quality_pen = abs(self._quality_penalty) if decision.quality_low else 0.0
                confidence_pct = base_conf + vlm_bonus - quality_pen
        elif score >= uncertain_low:
            if vlm_same_person is True:
                match = True
                age_bonus = self._age_gap_vlm_bonus if age_gap > self._age_gap_threshold else 0.0
                confidence_pct = base_conf + self._vlm_confirm_bonus + age_bonus
            else:
                match = False
                confidence_pct = base_conf + self._vlm_reject_uncertain
        else:
            match = False
            confidence_pct = base_conf

        if gender_mismatch and self._gender_mismatch_penalty != 0.0:
            confidence_pct += self._gender_mismatch_penalty  # negative value

        confidence_pct = max(0.0, min(confidence_pct, 99.0))
        return match, round(confidence_pct, 1)


def _elapsed_ms(start: float) -> float:
    """Return elapsed time in milliseconds since start."""
    return round((time.perf_counter() - start) * 1000, 1)
