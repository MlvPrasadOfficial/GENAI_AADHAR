"""Tests for pipeline/similarity.py — pure numpy, no GPU required."""

import numpy as np
import pytest

from pipeline.similarity import SimilarityDecision, SimilarityScorer


@pytest.fixture
def scorer(sample_config):
    return SimilarityScorer(sample_config)


class TestCosineSimilarity:
    """Test cosine_similarity computation."""

    def test_identical_vectors_score_1(self, scorer):
        v = np.random.randn(512).astype(np.float32)
        v /= np.linalg.norm(v)
        assert abs(scorer.cosine_similarity(v, v) - 1.0) < 1e-5

    def test_orthogonal_vectors_score_0(self, scorer):
        v1 = np.zeros(512, dtype=np.float32)
        v1[0] = 1.0
        v2 = np.zeros(512, dtype=np.float32)
        v2[1] = 1.0
        assert abs(scorer.cosine_similarity(v1, v2)) < 1e-5

    def test_opposite_vectors_clamped_to_0(self, scorer):
        v = np.random.randn(512).astype(np.float32)
        v /= np.linalg.norm(v)
        # Opposite direction → dot product < 0, clamped to 0.0
        assert scorer.cosine_similarity(v, -v) == 0.0

    def test_similar_vectors_high_score(self, scorer):
        v1 = np.random.randn(512).astype(np.float32)
        v1 /= np.linalg.norm(v1)
        noise = np.random.randn(512).astype(np.float32) * 0.01
        v2 = v1 + noise
        v2 /= np.linalg.norm(v2)
        score = scorer.cosine_similarity(v1, v2)
        assert score > 0.95

    def test_result_is_python_float(self, scorer, random_embedding):
        score = scorer.cosine_similarity(random_embedding(), random_embedding())
        assert isinstance(score, float)

    def test_mismatched_shapes_raises(self, scorer):
        v1 = np.random.randn(512).astype(np.float32)
        v2 = np.random.randn(256).astype(np.float32)
        with pytest.raises(ValueError, match="shape mismatch"):
            scorer.cosine_similarity(v1, v2)


class TestDecision:
    """Test threshold decision tree."""

    def test_high_score_good_quality_is_match(self, scorer):
        result = scorer.decide(0.75, quality_low=False)
        assert result.verdict == "match"
        assert result.needs_vlm is False

    def test_high_score_low_quality_needs_vlm(self, scorer):
        result = scorer.decide(0.65, quality_low=True)
        assert result.verdict == "match"
        assert result.needs_vlm is True
        assert result.quality_low is True

    def test_uncertain_zone_needs_vlm(self, scorer):
        result = scorer.decide(0.50, quality_low=False)
        assert result.verdict == "uncertain"
        assert result.needs_vlm is True

    def test_low_score_is_no_match(self, scorer):
        result = scorer.decide(0.20, quality_low=False)
        assert result.verdict == "no_match"
        assert result.needs_vlm is False

    def test_boundary_at_match_threshold(self, scorer):
        # Exactly at threshold → match
        result = scorer.decide(0.60, quality_low=False)
        assert result.verdict == "match"

    def test_boundary_just_below_match(self, scorer):
        result = scorer.decide(0.599, quality_low=False)
        assert result.verdict == "uncertain"

    def test_boundary_at_uncertain_low(self, scorer):
        result = scorer.decide(0.40, quality_low=False)
        assert result.verdict == "uncertain"

    def test_boundary_just_below_uncertain(self, scorer):
        result = scorer.decide(0.399, quality_low=False)
        assert result.verdict == "no_match"

    def test_zero_score(self, scorer):
        result = scorer.decide(0.0)
        assert result.verdict == "no_match"
        assert result.needs_vlm is False
