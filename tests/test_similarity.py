"""Tests for pipeline/similarity.py — pure numpy, no GPU required."""

import numpy as np
import pytest

from pipeline.similarity import (
    MultiMetricResult,
    SimilarityDecision,
    SimilarityScorer,
    compare_landmark_ratios,
    compute_landmark_ratios,
    compute_ssim,
)


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


class TestL2Distance:
    """Test L2 distance and score conversion."""

    def test_identical_vectors_zero_distance(self, scorer):
        v = np.random.randn(512).astype(np.float32)
        v /= np.linalg.norm(v)
        assert scorer.l2_distance(v, v) < 1e-5

    def test_opposite_vectors_max_distance(self, scorer):
        v = np.random.randn(512).astype(np.float32)
        v /= np.linalg.norm(v)
        dist = scorer.l2_distance(v, -v)
        assert abs(dist - 2.0) < 0.01  # sqrt(2 - 2*(-1)) = 2

    def test_l2_to_score_zero_is_one(self, scorer):
        assert abs(scorer.l2_to_score(0.0) - 1.0) < 1e-5

    def test_l2_to_score_large_distance_near_zero(self, scorer):
        assert scorer.l2_to_score(5.0) < 0.01

    def test_l2_to_score_moderate(self, scorer):
        score = scorer.l2_to_score(0.5)
        assert 0.3 < score < 0.6

    def test_mismatched_shapes_raises(self, scorer):
        with pytest.raises(ValueError, match="shape mismatch"):
            scorer.l2_distance(np.zeros(512), np.zeros(256))


class TestComputeSSIM:
    """Test SSIM computation on aligned face crops."""

    def test_identical_crops_high_ssim(self, dummy_face_crop):
        ssim = compute_ssim(dummy_face_crop, dummy_face_crop.copy())
        assert ssim > 0.95

    def test_different_crops_lower_ssim(self, dummy_face_crop):
        other = np.random.randint(0, 255, (112, 112, 3), dtype=np.uint8)
        ssim = compute_ssim(dummy_face_crop, other)
        assert ssim < 0.5

    def test_none_crop_returns_zero(self):
        crop = np.zeros((112, 112, 3), dtype=np.uint8)
        assert compute_ssim(None, crop) == 0.0
        assert compute_ssim(crop, None) == 0.0

    def test_shape_mismatch_returns_zero(self):
        c1 = np.zeros((112, 112, 3), dtype=np.uint8)
        c2 = np.zeros((64, 64, 3), dtype=np.uint8)
        assert compute_ssim(c1, c2) == 0.0

    def test_ssim_returns_float(self, dummy_face_crop):
        ssim = compute_ssim(dummy_face_crop, dummy_face_crop)
        assert isinstance(ssim, float)


class TestLandmarkRatios:
    """Test facial landmark ratio computation."""

    @pytest.fixture
    def fake_landmarks(self):
        """Generate a plausible 68-point 3D landmark array."""
        np.random.seed(42)
        # Create a roughly face-shaped landmark set
        lmk = np.zeros((68, 3), dtype=np.float32)
        # Place key points roughly where they'd be on a face
        # Eyes at reasonable positions
        lmk[36] = [30, 40, 0]   # right eye outer
        lmk[39] = [40, 40, 0]   # right eye inner
        lmk[42] = [50, 40, 0]   # left eye inner
        lmk[45] = [60, 40, 0]   # left eye outer
        # Fill eye regions for center calculation
        for i in range(36, 42):
            lmk[i] = [30 + (i - 36) * 2, 40, 0]
        for i in range(42, 48):
            lmk[i] = [50 + (i - 42) * 2, 40, 0]
        # Nose
        lmk[27] = [45, 35, 0]   # nose bridge top
        lmk[30] = [45, 55, 0]   # nose tip
        lmk[31] = [40, 58, 0]   # nose left
        lmk[35] = [50, 58, 0]   # nose right
        # Mouth
        lmk[48] = [35, 65, 0]   # mouth left
        lmk[54] = [55, 65, 0]   # mouth right
        lmk[51] = [45, 62, 0]   # mouth top
        lmk[57] = [45, 70, 0]   # mouth bottom
        # Jaw
        lmk[0] = [20, 50, 0]    # jaw left
        lmk[16] = [70, 50, 0]   # jaw right
        lmk[8] = [45, 80, 0]    # jaw bottom
        # Brows
        lmk[17] = [25, 30, 0]   # right brow outer
        lmk[21] = [40, 30, 0]   # right brow inner
        lmk[22] = [50, 30, 0]   # left brow inner
        lmk[26] = [65, 30, 0]   # left brow outer
        return lmk

    def test_returns_12_ratios(self, fake_landmarks):
        ratios = compute_landmark_ratios(fake_landmarks)
        assert len(ratios) == 12

    def test_all_ratios_positive(self, fake_landmarks):
        ratios = compute_landmark_ratios(fake_landmarks)
        for name, val in ratios.items():
            assert val >= 0, f"{name} should be non-negative"

    def test_none_landmarks_empty(self):
        assert compute_landmark_ratios(None) == {}

    def test_too_few_landmarks_empty(self):
        lmk = np.zeros((10, 3), dtype=np.float32)
        assert compute_landmark_ratios(lmk) == {}

    def test_zero_ipd_empty(self):
        lmk = np.zeros((68, 3), dtype=np.float32)
        # All points at origin → IPD = 0
        assert compute_landmark_ratios(lmk) == {}

    def test_same_face_identical_ratios(self, fake_landmarks):
        r1 = compute_landmark_ratios(fake_landmarks)
        r2 = compute_landmark_ratios(fake_landmarks.copy())
        for key in r1:
            assert abs(r1[key] - r2[key]) < 1e-6

    def test_compare_identical_ratios_score_1(self, fake_landmarks):
        ratios = compute_landmark_ratios(fake_landmarks)
        score, diffs = compare_landmark_ratios(ratios, ratios)
        assert abs(score - 1.0) < 1e-5
        assert all(d < 1e-6 for d in diffs.values())

    def test_compare_empty_ratios_returns_neg1(self):
        score, diffs = compare_landmark_ratios({}, {"a": 1.0})
        assert score == -1.0
        assert diffs == {}

    def test_compare_different_faces_lower_score(self, fake_landmarks):
        r1 = compute_landmark_ratios(fake_landmarks)
        # Perturb landmarks to simulate different face
        lmk2 = fake_landmarks.copy()
        lmk2[48] += [10, 0, 0]  # wider mouth
        lmk2[54] += [-10, 0, 0]
        lmk2[0] += [-5, 0, 0]   # wider jaw
        lmk2[16] += [5, 0, 0]
        r2 = compute_landmark_ratios(lmk2)
        score, diffs = compare_landmark_ratios(r1, r2)
        assert 0.0 <= score < 1.0


class TestComputeAllMetrics:
    """Test the full multi-metric computation."""

    @pytest.fixture
    def mock_face(self, random_embedding, dummy_face_crop):
        """Create a minimal face-like object with required attributes."""
        class FakeFace:
            def __init__(self):
                self.embedding = random_embedding()
                self.aligned_crop = dummy_face_crop
                self.landmark_3d_68 = None
                self.pose = None
        return FakeFace

    def test_returns_multi_metric_result(self, scorer, mock_face):
        f1, f2 = mock_face(), mock_face()
        result = scorer.compute_all_metrics(f1, f2)
        assert isinstance(result, MultiMetricResult)

    def test_cosine_in_result(self, scorer, mock_face):
        f1 = mock_face()
        result = scorer.compute_all_metrics(f1, f1)
        assert result.cosine > 0.99  # same embedding

    def test_l2_in_result(self, scorer, mock_face):
        f1, f2 = mock_face(), mock_face()
        result = scorer.compute_all_metrics(f1, f2)
        assert result.l2_distance >= 0
        assert 0 <= result.l2_score <= 1

    def test_ssim_in_result(self, scorer, mock_face):
        f1 = mock_face()
        result = scorer.compute_all_metrics(f1, f1)
        assert result.ssim > 0.95  # same crop

    def test_no_landmarks_negative_score(self, scorer, mock_face):
        f1, f2 = mock_face(), mock_face()
        result = scorer.compute_all_metrics(f1, f2)
        assert result.landmark_score == -1.0

    def test_no_pose_negative_diff(self, scorer, mock_face):
        f1, f2 = mock_face(), mock_face()
        result = scorer.compute_all_metrics(f1, f2)
        assert result.pose_diff == -1.0

    def test_fused_score_reasonable(self, scorer, mock_face):
        f1, f2 = mock_face(), mock_face()
        result = scorer.compute_all_metrics(f1, f2)
        assert 0 <= result.fused_score <= 1

    def test_with_pose(self, scorer, mock_face):
        f1, f2 = mock_face(), mock_face()
        f1.pose = np.array([10.0, 5.0, 2.0], dtype=np.float32)
        f2.pose = np.array([12.0, 3.0, 1.0], dtype=np.float32)
        result = scorer.compute_all_metrics(f1, f2)
        assert result.pose_diff > 0
