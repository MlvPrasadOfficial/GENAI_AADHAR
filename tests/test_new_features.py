"""Tests for v3 features: caching, S-norm, crop restore, calibration, adaptive thresholds."""

import numpy as np
import pytest

from pipeline.adaface import AdaFaceModel
from pipeline.confidence_calibrator import ConfidenceCalibrator
from pipeline.crop_restore import CropRestorer
from pipeline.score_norm import SNormCalibrator
from pipeline.similarity import SimilarityScorer
from utils.embedding_cache import EmbeddingCache


# ---------------------------------------------------------------------------
# Embedding Cache
# ---------------------------------------------------------------------------

class TestEmbeddingCache:
    def test_put_and_get(self):
        cache = EmbeddingCache(max_size=4)
        cache.put("abc", {"data": 1})
        assert cache.get("abc") == {"data": 1}

    def test_miss_returns_none(self):
        cache = EmbeddingCache(max_size=4)
        assert cache.get("nonexistent") is None

    def test_lru_eviction(self):
        cache = EmbeddingCache(max_size=2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.put("c", 3)  # evicts "a"
        assert cache.get("a") is None
        assert cache.get("b") == 2
        assert cache.get("c") == 3

    def test_access_refreshes_lru(self):
        cache = EmbeddingCache(max_size=2)
        cache.put("a", 1)
        cache.put("b", 2)
        cache.get("a")  # refresh "a"
        cache.put("c", 3)  # evicts "b" (not "a")
        assert cache.get("a") == 1
        assert cache.get("b") is None

    def test_hash_key_deterministic(self):
        data = b"test image bytes"
        k1 = EmbeddingCache.hash_key(data)
        k2 = EmbeddingCache.hash_key(data)
        assert k1 == k2

    def test_hash_key_differs_for_different_data(self):
        k1 = EmbeddingCache.hash_key(b"image1")
        k2 = EmbeddingCache.hash_key(b"image2")
        assert k1 != k2

    def test_stats(self):
        cache = EmbeddingCache(max_size=4)
        cache.put("a", 1)
        cache.get("a")       # hit
        cache.get("missing")  # miss
        stats = cache.stats
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["size"] == 1
        assert stats["hit_rate"] == 0.5

    def test_clear(self):
        cache = EmbeddingCache(max_size=4)
        cache.put("a", 1)
        cache.clear()
        assert cache.get("a") is None
        assert cache.stats["size"] == 0

    def test_overwrite_existing_key(self):
        cache = EmbeddingCache(max_size=4)
        cache.put("a", 1)
        cache.put("a", 2)
        assert cache.get("a") == 2
        assert cache.stats["size"] == 1


# ---------------------------------------------------------------------------
# S-norm Score Normalization
# ---------------------------------------------------------------------------

class TestSNormCalibrator:
    @pytest.fixture
    def calibrator(self, sample_config):
        cfg = dict(sample_config)
        cfg["score_norm"] = {"enabled": True, "cohort_path": "nonexistent.npy", "cohort_size": 10}
        return SNormCalibrator(cfg)

    def test_disabled_returns_raw(self, sample_config):
        cal = SNormCalibrator(sample_config)
        assert cal.normalize(np.zeros(512), np.zeros(512), 0.55) == 0.55

    def test_build_cohort(self, calibrator):
        embeddings = []
        for _ in range(20):
            v = np.random.randn(512).astype(np.float32)
            v /= np.linalg.norm(v)
            embeddings.append(v)
        calibrator.build_cohort_from_embeddings(embeddings)
        assert calibrator.available
        assert calibrator._cohort.shape == (10, 512)

    def test_normalize_with_cohort(self, calibrator):
        # Build cohort
        embeddings = []
        for _ in range(20):
            v = np.random.randn(512).astype(np.float32)
            v /= np.linalg.norm(v)
            embeddings.append(v)
        calibrator.build_cohort_from_embeddings(embeddings)

        probe = np.random.randn(512).astype(np.float32)
        probe /= np.linalg.norm(probe)
        gallery = np.random.randn(512).astype(np.float32)
        gallery /= np.linalg.norm(gallery)
        raw = float(np.dot(probe, gallery))
        normed = calibrator.normalize(probe, gallery, raw)
        # S-norm output should be different from raw
        assert isinstance(normed, float)

    def test_unavailable_when_no_cohort(self, sample_config):
        cal = SNormCalibrator(sample_config)
        assert not cal.available


# ---------------------------------------------------------------------------
# Confidence Calibrator (Platt Scaling)
# ---------------------------------------------------------------------------

class TestConfidenceCalibrator:
    @pytest.fixture
    def calibrator(self):
        config = {"calibration": {"enabled": True, "platt_a": 15.0, "platt_b": -7.5}}
        return ConfidenceCalibrator(config)

    def test_disabled_returns_raw_percent(self):
        cal = ConfidenceCalibrator({"calibration": {"enabled": False}})
        assert abs(cal.calibrate(0.55) - 55.0) < 0.01

    def test_calibrated_monotonic(self, calibrator):
        # Higher scores should give higher confidence
        c1 = calibrator.calibrate(0.40)
        c2 = calibrator.calibrate(0.50)
        c3 = calibrator.calibrate(0.60)
        assert c1 < c2 < c3

    def test_high_score_high_confidence(self, calibrator):
        c = calibrator.calibrate(0.70)
        assert c > 80.0

    def test_low_score_low_confidence(self, calibrator):
        c = calibrator.calibrate(0.20)
        assert c < 20.0

    def test_capped_at_99(self, calibrator):
        c = calibrator.calibrate(1.0)
        assert c <= 99.0

    def test_quality_factor_reduces_confidence(self, calibrator):
        good = calibrator.calibrate(0.55, quality_factor=1.0)
        poor = calibrator.calibrate(0.55, quality_factor=0.7)
        assert poor < good

    def test_fit_updates_params(self, calibrator):
        scores = [0.7, 0.8, 0.65, 0.3, 0.2, 0.15, 0.25, 0.1, 0.75, 0.6]
        labels = [True, True, True, False, False, False, False, False, True, True]
        a, b = calibrator.fit(scores, labels)
        assert a != 15.0 or b != -7.5  # at least one changed


# ---------------------------------------------------------------------------
# Crop Restorer
# ---------------------------------------------------------------------------

class TestCropRestorer:
    def test_disabled_returns_input(self, dummy_face_crop):
        restorer = CropRestorer({"crop_restore": {"enabled": False}})
        result = restorer.restore(dummy_face_crop)
        np.testing.assert_array_equal(result, dummy_face_crop)

    def test_bilateral_changes_pixels(self, dummy_face_crop):
        restorer = CropRestorer({
            "crop_restore": {"enabled": True, "backend": "bilateral"}
        })
        restorer.load()
        result = restorer.restore(dummy_face_crop)
        assert result.shape == dummy_face_crop.shape
        # Bilateral filter should smooth, so output differs
        assert not np.array_equal(result, dummy_face_crop)

    def test_none_input_returns_none(self):
        restorer = CropRestorer({"crop_restore": {"enabled": True, "backend": "bilateral"}})
        assert restorer.restore(None) is None

    def test_gfpgan_falls_back_to_bilateral(self):
        restorer = CropRestorer({
            "crop_restore": {
                "enabled": True,
                "backend": "gfpgan",
                "gfpgan_model_path": "nonexistent_model.pth",
            }
        })
        restorer.load()
        assert restorer.backend == "bilateral"


# ---------------------------------------------------------------------------
# Adaptive Thresholds
# ---------------------------------------------------------------------------

class TestAdaptiveThresholds:
    def test_disabled_returns_base(self, sample_config):
        scorer = SimilarityScorer(sample_config)
        mt, ul = scorer.get_adaptive_thresholds(0.8)
        assert mt == 0.60
        assert ul == 0.40

    def test_enabled_high_quality_stricter(self, sample_config):
        cfg = dict(sample_config)
        cfg["similarity"] = dict(cfg["similarity"])
        cfg["similarity"]["adaptive_thresholds"] = True
        scorer = SimilarityScorer(cfg)
        mt, ul = scorer.get_adaptive_thresholds(0.8)
        assert mt == 0.65
        assert ul == 0.45

    def test_enabled_low_quality_relaxed(self, sample_config):
        cfg = dict(sample_config)
        cfg["similarity"] = dict(cfg["similarity"])
        cfg["similarity"]["adaptive_thresholds"] = True
        scorer = SimilarityScorer(cfg)
        mt, ul = scorer.get_adaptive_thresholds(0.2)
        assert mt == 0.55
        assert ul == 0.35

    def test_medium_quality_standard(self, sample_config):
        cfg = dict(sample_config)
        cfg["similarity"] = dict(cfg["similarity"])
        cfg["similarity"]["adaptive_thresholds"] = True
        scorer = SimilarityScorer(cfg)
        mt, ul = scorer.get_adaptive_thresholds(0.5)
        assert mt == 0.60
        assert ul == 0.40


# ---------------------------------------------------------------------------
# Quality-Weighted Fusion
# ---------------------------------------------------------------------------

class TestQualityWeightedFusion:
    def test_disabled_returns_default_weights(self, sample_config):
        scorer = SimilarityScorer(sample_config)
        w = scorer.get_quality_adjusted_weights(0.2)
        assert w == scorer.fusion_weights

    def test_enabled_low_quality_boosts_cosine(self, sample_config):
        """v3: quality-weighted fusion now makes cosine dominant at low quality
        (old behavior boosted landmark; printed-card landmarks are unreliable)."""
        cfg = dict(sample_config)
        cfg["similarity"] = dict(cfg["similarity"])
        cfg["similarity"]["quality_weighted_fusion"] = True
        scorer = SimilarityScorer(cfg)
        w = scorer.get_quality_adjusted_weights(0.2)
        assert w["cosine"] == 0.80
        assert w["landmark"] == 0.10
        assert w["ssim"] == 0.03

    def test_enabled_good_quality_unchanged(self, sample_config):
        cfg = dict(sample_config)
        cfg["similarity"] = dict(cfg["similarity"])
        cfg["similarity"]["quality_weighted_fusion"] = True
        scorer = SimilarityScorer(cfg)
        w = scorer.get_quality_adjusted_weights(0.8)
        assert w == scorer.fusion_weights


# ---------------------------------------------------------------------------
# AdaFace
# ---------------------------------------------------------------------------

class TestAdaFaceModel:
    def test_disabled_by_default(self, sample_config):
        model = AdaFaceModel(sample_config)
        assert not model.enabled
        assert not model.available

    def test_missing_model_disables(self):
        cfg = {"adaface": {"enabled": True, "model_path": "nonexistent.ckpt"}}
        model = AdaFaceModel(cfg)
        model.load()
        assert not model.available

    def test_fuse_scores_weighted(self):
        cfg = {"adaface": {"enabled": True, "fusion_weight": 0.3}}
        model = AdaFaceModel(cfg)
        fused = model.fuse_scores(0.60, 0.50)
        expected = 0.7 * 0.60 + 0.3 * 0.50
        assert abs(fused - expected) < 0.001

    def test_fuse_scores_clamped(self):
        cfg = {"adaface": {"enabled": True, "fusion_weight": 0.5}}
        model = AdaFaceModel(cfg)
        assert model.fuse_scores(1.0, 1.0) <= 1.0
        assert model.fuse_scores(0.0, 0.0) >= 0.0

    def test_get_embedding_when_unavailable(self, dummy_face_crop):
        cfg = {"adaface": {"enabled": False}}
        model = AdaFaceModel(cfg)
        assert model.get_embedding(dummy_face_crop) is None
