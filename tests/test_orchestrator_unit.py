"""Unit tests for KYCPipelineOrchestrator._fuse_decision() — no GPU, no models."""

import pytest

from pipeline.orchestrator import KYCPipelineOrchestrator
from pipeline.similarity import SimilarityDecision


@pytest.fixture
def pipeline(sample_config):
    """Create orchestrator without loading models (only need _fuse_decision)."""
    return KYCPipelineOrchestrator(sample_config)


def _decision(verdict="match", score=0.7, needs_vlm=False, quality_low=False):
    return SimilarityDecision(verdict=verdict, score=score,
                              needs_vlm=needs_vlm, quality_low=quality_low)


class TestFuseDecisionHighScore:
    """score >= match_threshold (0.60)"""

    def test_high_score_no_vlm_is_match(self, pipeline):
        match, conf = pipeline._fuse_decision(0.75, _decision(score=0.75), vlm_same_person=None)
        assert match is True
        assert abs(conf - 75.0) < 0.2

    def test_high_score_vlm_confirms_adds_bonus(self, pipeline):
        match, conf = pipeline._fuse_decision(0.65, _decision(score=0.65), vlm_same_person=True)
        assert match is True
        assert abs(conf - 73.0) < 0.2  # 65 + 8

    def test_high_score_vlm_rejects_is_no_match(self, pipeline):
        match, conf = pipeline._fuse_decision(0.70, _decision(score=0.70), vlm_same_person=False)
        assert match is False
        assert abs(conf - 50.0) < 0.2  # 70 - 20

    def test_high_score_low_quality_penalty(self, pipeline):
        d = _decision(score=0.65, quality_low=True)
        match, conf = pipeline._fuse_decision(0.65, d, vlm_same_person=None)
        assert match is True
        assert abs(conf - 60.0) < 0.2  # 65 - 5

    def test_high_score_vlm_confirm_plus_quality_penalty(self, pipeline):
        d = _decision(score=0.65, quality_low=True)
        match, conf = pipeline._fuse_decision(0.65, d, vlm_same_person=True)
        assert match is True
        assert abs(conf - 68.0) < 0.2  # 65 + 8 - 5


class TestFuseDecisionUncertainZone:
    """uncertain_low (0.40) <= score < match_threshold (0.60)"""

    def test_uncertain_vlm_confirms_is_match(self, pipeline):
        match, conf = pipeline._fuse_decision(0.50, _decision("uncertain", 0.50), vlm_same_person=True)
        assert match is True
        assert abs(conf - 58.0) < 0.2  # 50 + 8

    def test_uncertain_vlm_rejects_is_no_match(self, pipeline):
        match, conf = pipeline._fuse_decision(0.50, _decision("uncertain", 0.50), vlm_same_person=False)
        assert match is False
        assert abs(conf - 40.0) < 0.2  # 50 - 10

    def test_uncertain_no_vlm_is_no_match(self, pipeline):
        """Conservative: no VLM response in uncertain zone → reject."""
        match, conf = pipeline._fuse_decision(0.50, _decision("uncertain", 0.50), vlm_same_person=None)
        assert match is False


class TestFuseDecisionLowScore:
    """score < uncertain_low (0.40)"""

    def test_low_score_is_no_match(self, pipeline):
        match, conf = pipeline._fuse_decision(0.20, _decision("no_match", 0.20), vlm_same_person=None)
        assert match is False
        assert abs(conf - 20.0) < 0.2

    def test_zero_score(self, pipeline):
        match, conf = pipeline._fuse_decision(0.0, _decision("no_match", 0.0), vlm_same_person=None)
        assert match is False
        assert conf == 0.0


class TestFuseDecisionClamping:
    def test_clamps_to_99(self, pipeline):
        match, conf = pipeline._fuse_decision(0.95, _decision(score=0.95), vlm_same_person=True)
        assert conf <= 99.0

    def test_clamps_to_0(self, pipeline):
        """Edge case: high penalty on low score should not go negative."""
        match, conf = pipeline._fuse_decision(0.05, _decision("no_match", 0.05), vlm_same_person=None)
        assert conf >= 0.0


class TestAgeGapRelaxation:
    """Age-gated threshold relaxation (Phase 1a)."""

    def test_no_relaxation_below_threshold(self, pipeline):
        """Age gap <= 5 → no relaxation, score 0.57 still uncertain."""
        match, conf = pipeline._fuse_decision(
            0.57, _decision("uncertain", 0.57, needs_vlm=True), vlm_same_person=None, age_gap=3
        )
        assert match is False  # 0.57 < 0.60, uncertain with no VLM → reject

    def test_relaxation_at_8yr_gap(self, pipeline):
        """8yr gap → relax by 0.03 → effective threshold 0.57. Score 0.58 now matches."""
        match, conf = pipeline._fuse_decision(
            0.58, _decision("uncertain", 0.58, needs_vlm=True), vlm_same_person=None, age_gap=8
        )
        assert match is True  # 0.58 >= 0.57 effective threshold

    def test_relaxation_at_12yr_gap(self, pipeline):
        """12yr gap → relax by 0.07 → effective threshold 0.53. Score 0.54 matches."""
        match, conf = pipeline._fuse_decision(
            0.54, _decision("uncertain", 0.54, needs_vlm=True), vlm_same_person=None, age_gap=12
        )
        assert match is True

    def test_relaxation_capped(self, pipeline):
        """25yr gap → capped at 0.10 → effective threshold 0.50."""
        match, conf = pipeline._fuse_decision(
            0.51, _decision("uncertain", 0.51, needs_vlm=True), vlm_same_person=None, age_gap=25
        )
        assert match is True  # 0.51 >= 0.50

    def test_relaxation_cap_not_exceeded(self, pipeline):
        """Score just below capped threshold still rejected."""
        match, conf = pipeline._fuse_decision(
            0.49, _decision("uncertain", 0.49, needs_vlm=True), vlm_same_person=None, age_gap=25
        )
        # 0.49 < 0.50 effective threshold, but >= 0.30 effective uncertain_low → uncertain zone
        assert match is False  # no VLM → conservative reject

    def test_relaxation_with_vlm_confirm(self, pipeline):
        """Age relaxation + VLM confirm → match with bonus + age bonus."""
        match, conf = pipeline._fuse_decision(
            0.55, _decision("uncertain", 0.55, needs_vlm=True), vlm_same_person=True, age_gap=10
        )
        # 10yr gap → relax 0.05 → effective threshold 0.55 → 0.55 >= 0.55 → match zone
        # vlm_bonus(8) + age_gap_vlm_bonus(5) = 13
        assert match is True
        assert abs(conf - 68.0) < 0.2  # 55 + 8 + 5

    def test_zero_age_gap_no_effect(self, pipeline):
        """age_gap=0 → no relaxation."""
        relaxation = pipeline._compute_age_relaxation(0)
        assert relaxation == 0.0

    def test_exact_threshold_age_gap(self, pipeline):
        """age_gap exactly at threshold → no relaxation."""
        relaxation = pipeline._compute_age_relaxation(5)
        assert relaxation == 0.0


class TestAgeGapVLMBonus:
    """Age-gap VLM confidence bonus (WI 2)."""

    def test_vlm_bonus_with_large_age_gap_match_zone(self, pipeline):
        """VLM confirms + age_gap=10 in match zone → base + vlm_bonus(8) + age_bonus(5)."""
        match, conf = pipeline._fuse_decision(
            0.65, _decision(score=0.65), vlm_same_person=True, age_gap=10
        )
        assert match is True
        # 65 + 8 + 5 = 78.0
        assert abs(conf - 78.0) < 0.2

    def test_no_vlm_bonus_when_gap_small(self, pipeline):
        """VLM confirms + age_gap=3 → normal bonus only, no age bonus."""
        match, conf = pipeline._fuse_decision(
            0.65, _decision(score=0.65), vlm_same_person=True, age_gap=3
        )
        assert match is True
        # 65 + 8 = 73.0 (no age bonus)
        assert abs(conf - 73.0) < 0.2

    def test_vlm_bonus_in_uncertain_zone(self, pipeline):
        """VLM confirms in uncertain zone + age_gap=8 → includes age bonus."""
        match, conf = pipeline._fuse_decision(
            0.55, _decision("uncertain", 0.55, needs_vlm=True), vlm_same_person=True, age_gap=8
        )
        # 8yr gap → relax 0.03 → effective threshold 0.57, 0.55 < 0.57 → still uncertain zone
        # uncertain zone + VLM confirm: 55 + 8 + 5 = 68.0
        assert match is True
        assert abs(conf - 68.0) < 0.2

    def test_vlm_bonus_disabled_when_zero(self, sample_config):
        """age_gap_vlm_bonus=0 → no extra bonus even with large gap."""
        sample_config["confidence_adjustments"]["age_gap_vlm_bonus"] = 0.0
        from pipeline.orchestrator import KYCPipelineOrchestrator
        p = KYCPipelineOrchestrator(sample_config)
        match, conf = p._fuse_decision(
            0.65, _decision(score=0.65), vlm_same_person=True, age_gap=10
        )
        assert match is True
        # 65 + 8 + 0 = 73.0
        assert abs(conf - 73.0) < 0.2


class TestGenderMismatchPenalty:
    """Gender mismatch penalty (WI 5b)."""

    def test_gender_mismatch_penalty_applied(self, sample_config):
        """With penalty configured, gender mismatch reduces confidence."""
        sample_config["confidence_adjustments"]["gender_mismatch_penalty"] = -15.0
        from pipeline.orchestrator import KYCPipelineOrchestrator
        p = KYCPipelineOrchestrator(sample_config)
        match, conf = p._fuse_decision(
            0.65, _decision(score=0.65), vlm_same_person=None, gender_mismatch=True
        )
        assert match is True
        # 65 + 0 (no vlm) - 15 (gender) = 50.0
        assert abs(conf - 50.0) < 0.2

    def test_gender_mismatch_penalty_zero_no_effect(self, pipeline):
        """Default 0.0 penalty means no change even with gender mismatch."""
        match1, conf1 = pipeline._fuse_decision(
            0.65, _decision(score=0.65), vlm_same_person=None, gender_mismatch=False
        )
        match2, conf2 = pipeline._fuse_decision(
            0.65, _decision(score=0.65), vlm_same_person=None, gender_mismatch=True
        )
        assert conf1 == conf2


class TestPreprocessingConfig:
    """CLAHE preprocessing wiring tests."""

    def test_clahe_disabled_by_default(self, pipeline):
        """Default sample_config has CLAHE disabled."""
        assert pipeline._aadhaar_clahe is False

    def test_clahe_enabled_from_config(self, sample_config):
        sample_config["preprocessing"]["aadhaar_clahe"] = True
        p = KYCPipelineOrchestrator(sample_config)
        assert p._aadhaar_clahe is True
        assert p._clahe_clip_limit == 2.0
        assert p._clahe_tile_size == 8

    def test_clahe_custom_params(self, sample_config):
        sample_config["preprocessing"] = {
            "aadhaar_clahe": True,
            "clahe_clip_limit": 3.5,
            "clahe_tile_size": 4,
        }
        p = KYCPipelineOrchestrator(sample_config)
        assert p._clahe_clip_limit == 3.5
        assert p._clahe_tile_size == 4

    def test_dual_path_disabled_by_default(self, pipeline):
        assert pipeline._dual_path is False

    def test_dual_path_enabled_from_config(self, sample_config):
        sample_config["preprocessing"]["dual_path"] = True
        p = KYCPipelineOrchestrator(sample_config)
        assert p._dual_path is True

    def test_grayscale_disabled_by_default(self, pipeline):
        assert pipeline._grayscale_normalize is False

    def test_grayscale_enabled_from_config(self, sample_config):
        sample_config["preprocessing"]["grayscale_normalize"] = True
        p = KYCPipelineOrchestrator(sample_config)
        assert p._grayscale_normalize is True
