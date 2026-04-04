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

            quality_low = aadhaar_quality < self.enhancer.quality_threshold or \
                          selfie_quality < self.enhancer.quality_threshold

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
                )
                timings["vlm_ms"] = _elapsed_ms(t0)
                vlm_same_person = verdict.same_person
                vlm_reasoning = verdict.reasoning

                logger.info(
                    "VLM: same_person=%s confidence=%s reasoning=%s",
                    verdict.same_person, verdict.confidence, verdict.reasoning,
                )

            # --- Stage 6: Final decision fusion ---
            match, confidence_pct = self._fuse_decision(
                score, decision, vlm_same_person
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

    def _fuse_decision(
        self,
        score: float,
        decision,
        vlm_same_person: bool | None,
    ) -> tuple[bool, float]:
        """Combine cosine score and VLM verdict into final match + confidence.

        Decision logic:
            score >= 0.60 + quality OK (no VLM) → MATCH
            score >= 0.60 + quality LOW + VLM:
                VLM says no → NO MATCH
                VLM unavailable → MATCH (trust the high score)
                VLM says yes → MATCH
            0.40–0.60 + VLM says yes (high/medium) → MATCH
            0.40–0.60 + VLM unavailable → NO MATCH (conservative)
            0.40–0.60 + VLM says no → NO MATCH
            < 0.40 → NO MATCH (no VLM)

        Returns:
            (match: bool, confidence_pct: float)
        """
        match_thresh = self.scorer.match_threshold

        if score >= match_thresh:
            if vlm_same_person is False:
                # VLM explicitly says no despite high score — reject
                match = False
                confidence_pct = score * 100 * 0.5
            else:
                # VLM says yes, unavailable (None), or wasn't invoked — trust score
                match = True
                vlm_boost = 1.15 if vlm_same_person is True else 1.0
                confidence_pct = score * 100 * vlm_boost
        elif score >= self.scorer.uncertain_low:
            if vlm_same_person is True:
                match = True
                confidence_pct = score * 100 * 1.1
            else:
                # VLM says no, unavailable, or wasn't invoked — conservative reject
                match = False
                confidence_pct = score * 100 * 0.7
        else:
            match = False
            confidence_pct = score * 100

        confidence_pct = min(confidence_pct, 99.0)
        return match, round(confidence_pct, 1)


def _elapsed_ms(start: float) -> float:
    """Return elapsed time in milliseconds since start."""
    return round((time.perf_counter() - start) * 1000, 1)
