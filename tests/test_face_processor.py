"""Tests for pipeline/face_processor.py — mocks InsightFace, no GPU needed."""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from pipeline.face_processor import FaceProcessor, FaceResult
from utils.exceptions import NoFaceDetectedError


def _make_fake_face(det_score=0.9, gender=1, age=30, norm=1.0):
    """Create a fake InsightFace face object with required attributes."""
    embedding = np.random.randn(512).astype(np.float32)
    if norm > 0:
        embedding = embedding / np.linalg.norm(embedding) * norm
    else:
        embedding = np.zeros(512, dtype=np.float32)

    return SimpleNamespace(
        det_score=det_score,
        bbox=np.array([100, 100, 200, 200], dtype=np.float32),
        normed_embedding=embedding,
        kps=np.array([[120, 130], [180, 130], [150, 160], [125, 185], [175, 185]], dtype=np.float32),
        gender=gender,
        age=age,
    )


@pytest.fixture
def processor(sample_config):
    """Create a FaceProcessor without loading models."""
    return FaceProcessor(sample_config)


@pytest.fixture
def loaded_processor(processor):
    """FaceProcessor with a mocked _app."""
    processor._app = MagicMock()
    return processor


class TestProcessNotLoaded:
    def test_raises_if_not_loaded(self, processor):
        img = np.zeros((200, 200, 3), dtype=np.uint8)
        with pytest.raises(RuntimeError, match="not loaded"):
            processor.process(img)


class TestProcessFaceSelection:
    @patch("insightface.utils.face_align.norm_crop", return_value=np.zeros((112, 112, 3), dtype=np.uint8))
    def test_picks_highest_det_score(self, mock_crop, loaded_processor):
        face_low = _make_fake_face(det_score=0.75)
        face_high = _make_fake_face(det_score=0.95)
        loaded_processor._app.get.return_value = [face_low, face_high]

        result = loaded_processor.process(np.zeros((200, 200, 3), dtype=np.uint8))
        assert abs(result.det_score - 0.95) < 0.01

    @patch("insightface.utils.face_align.norm_crop", return_value=np.zeros((112, 112, 3), dtype=np.uint8))
    def test_fallback_threshold(self, mock_crop, loaded_processor):
        """Face at 0.55 (below primary 0.7, above fallback 0.5) should be found."""
        face = _make_fake_face(det_score=0.55)
        loaded_processor._app.get.return_value = [face]

        result = loaded_processor.process(np.zeros((200, 200, 3), dtype=np.uint8))
        assert abs(result.det_score - 0.55) < 0.01

    def test_no_face_raises(self, loaded_processor):
        loaded_processor._app.get.return_value = []
        with pytest.raises(NoFaceDetectedError):
            loaded_processor.process(np.zeros((200, 200, 3), dtype=np.uint8))

    def test_all_below_fallback_raises(self, loaded_processor):
        """Face at 0.3 (below fallback 0.5) should raise."""
        face = _make_fake_face(det_score=0.3)
        loaded_processor._app.get.return_value = [face]
        with pytest.raises(NoFaceDetectedError):
            loaded_processor.process(np.zeros((200, 200, 3), dtype=np.uint8))


class TestEmbeddingNormalization:
    @patch("insightface.utils.face_align.norm_crop", return_value=np.zeros((112, 112, 3), dtype=np.uint8))
    def test_renormalizes_non_unit_embedding(self, mock_crop, loaded_processor):
        face = _make_fake_face(det_score=0.9, norm=1.05)
        loaded_processor._app.get.return_value = [face]

        result = loaded_processor.process(np.zeros((200, 200, 3), dtype=np.uint8))
        assert abs(np.linalg.norm(result.embedding) - 1.0) < 0.001

    def test_zero_norm_raises(self, loaded_processor):
        face = _make_fake_face(det_score=0.9, norm=0)
        loaded_processor._app.get.return_value = [face]
        with pytest.raises(NoFaceDetectedError, match="zero norm"):
            loaded_processor.process(np.zeros((200, 200, 3), dtype=np.uint8))


class TestGenderAgeMapping:
    @patch("insightface.utils.face_align.norm_crop", return_value=np.zeros((112, 112, 3), dtype=np.uint8))
    def test_male_mapping(self, mock_crop, loaded_processor):
        face = _make_fake_face(gender=1, age=35)
        loaded_processor._app.get.return_value = [face]
        result = loaded_processor.process(np.zeros((200, 200, 3), dtype=np.uint8))
        assert result.gender == "M"
        assert result.age == 35

    @patch("insightface.utils.face_align.norm_crop", return_value=np.zeros((112, 112, 3), dtype=np.uint8))
    def test_female_mapping(self, mock_crop, loaded_processor):
        face = _make_fake_face(gender=0, age=28)
        loaded_processor._app.get.return_value = [face]
        result = loaded_processor.process(np.zeros((200, 200, 3), dtype=np.uint8))
        assert result.gender == "F"
        assert result.age == 28

    @patch("insightface.utils.face_align.norm_crop", return_value=np.zeros((112, 112, 3), dtype=np.uint8))
    def test_unknown_gender(self, mock_crop, loaded_processor):
        face = _make_fake_face(gender=1)
        face.gender = None  # override
        loaded_processor._app.get.return_value = [face]
        result = loaded_processor.process(np.zeros((200, 200, 3), dtype=np.uint8))
        assert result.gender == "unknown"


class TestMultiFaceWarning:
    @patch("insightface.utils.face_align.norm_crop", return_value=np.zeros((112, 112, 3), dtype=np.uint8))
    def test_multi_face_warning_logged(self, mock_crop, loaded_processor, caplog):
        """Warning should be logged when multiple faces are detected."""
        import logging
        faces = [_make_fake_face(det_score=0.9), _make_fake_face(det_score=0.8), _make_fake_face(det_score=0.7)]
        loaded_processor._app.get.return_value = faces
        with caplog.at_level(logging.WARNING):
            loaded_processor.process(np.zeros((200, 200, 3), dtype=np.uint8))
        assert "3 faces detected" in caplog.text

    @patch("insightface.utils.face_align.norm_crop", return_value=np.zeros((112, 112, 3), dtype=np.uint8))
    def test_num_faces_in_result(self, mock_crop, loaded_processor):
        """num_faces_detected should reflect the total count."""
        faces = [_make_fake_face(det_score=0.9), _make_fake_face(det_score=0.8)]
        loaded_processor._app.get.return_value = faces
        result = loaded_processor.process(np.zeros((200, 200, 3), dtype=np.uint8))
        assert result.num_faces_detected == 2


class TestFlipAugment:
    """Flip-augmented embedding (TTA) tests."""

    @patch("insightface.utils.face_align.norm_crop", return_value=np.zeros((112, 112, 3), dtype=np.uint8))
    def test_flip_augment_averages_embeddings(self, mock_crop, sample_config):
        """With flip_augment=True, embedding should be averaged with flipped version."""
        sample_config["face"]["flip_augment"] = True
        proc = FaceProcessor(sample_config)
        proc._app = MagicMock()

        face = _make_fake_face(det_score=0.9)
        proc._app.get.return_value = [face]

        # Mock the rec model to return a known embedding for the flipped crop
        mock_rec = MagicMock()
        flipped_emb = np.random.randn(1, 512).astype(np.float32)
        flipped_emb /= np.linalg.norm(flipped_emb)
        mock_rec.get_feat.return_value = flipped_emb
        mock_rec.taskname = "recognition"
        proc._app.models = {"w600k_r50": mock_rec}

        result = proc.process(np.zeros((200, 200, 3), dtype=np.uint8))
        # Embedding should be L2-normalized
        assert abs(np.linalg.norm(result.embedding) - 1.0) < 0.001
        # It should NOT be identical to the original (it's averaged with flip)
        assert not np.allclose(result.embedding, face.normed_embedding, atol=1e-3)

    @patch("insightface.utils.face_align.norm_crop", return_value=np.zeros((112, 112, 3), dtype=np.uint8))
    def test_no_flip_augment_by_default(self, mock_crop, loaded_processor):
        """Default config should NOT apply flip augment."""
        face = _make_fake_face(det_score=0.9)
        loaded_processor._app.get.return_value = [face]

        result = loaded_processor.process(np.zeros((200, 200, 3), dtype=np.uint8))
        # Should match original embedding (no averaging)
        assert np.allclose(result.embedding, face.normed_embedding, atol=0.02)

    @patch("insightface.utils.face_align.norm_crop", return_value=np.zeros((112, 112, 3), dtype=np.uint8))
    def test_flip_augment_graceful_without_rec_model(self, mock_crop, sample_config):
        """If recognition model is not found, flip augment should be skipped gracefully."""
        sample_config["face"]["flip_augment"] = True
        proc = FaceProcessor(sample_config)
        proc._app = MagicMock()
        proc._app.models = {}  # no models

        face = _make_fake_face(det_score=0.9)
        proc._app.get.return_value = [face]

        result = proc.process(np.zeros((200, 200, 3), dtype=np.uint8))
        # Should still return a valid result (falls back to original embedding)
        assert result.embedding is not None
        assert abs(np.linalg.norm(result.embedding) - 1.0) < 0.001
