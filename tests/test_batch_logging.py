"""Tests for batch logging functions in utils/result_logger.py."""

import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pytest

from utils.result_logger import create_batch_dir, log_batch_result, write_batch_summary


@dataclass
class _FakeResult:
    match: bool = False
    confidence_pct: float = 50.0
    cosine_score: float = 0.55
    vlm_same_person: bool | None = None
    vlm_reasoning: str | None = None
    stage_timings: dict = field(default_factory=lambda: {"load_ms": 10})
    aadhaar_quality: float = 0.8
    selfie_quality: float = 0.9
    aadhaar_crop: np.ndarray | None = None
    selfie_crop: np.ndarray | None = None
    aadhaar_gender: str = "M"
    aadhaar_age: int = 35
    selfie_gender: str = "M"
    selfie_age: int = 30
    error: str | None = None


class TestCreateBatchDir:
    def test_creates_folder(self, tmp_path):
        batch_dir = create_batch_dir(str(tmp_path))
        assert batch_dir.exists()
        assert batch_dir.is_dir()

    def test_folder_name_starts_with_batch(self, tmp_path):
        batch_dir = create_batch_dir(str(tmp_path))
        assert batch_dir.name.startswith("batch_")


class TestLogBatchResult:
    def test_creates_subfolder_with_result(self, tmp_path):
        batch_dir = create_batch_dir(str(tmp_path))
        result = _FakeResult()
        run_dir = log_batch_result(result, "card.jpg", "selfie.jpg", batch_dir)
        assert run_dir.exists()
        assert (run_dir / "result.txt").exists()

    def test_subfolder_name_contains_stems_and_status(self, tmp_path):
        batch_dir = create_batch_dir(str(tmp_path))
        result = _FakeResult(match=True)
        run_dir = log_batch_result(result, "files/AADHAR001.jpg", "files/USER_01.jpg", batch_dir)
        assert "AADHAR001" in run_dir.name
        assert "USER_01" in run_dir.name
        assert "MATCH" in run_dir.name

    def test_error_status_in_name(self, tmp_path):
        batch_dir = create_batch_dir(str(tmp_path))
        result = _FakeResult(error="something broke")
        run_dir = log_batch_result(result, "a.jpg", "b.jpg", batch_dir)
        assert "ERROR" in run_dir.name


class TestWriteBatchSummary:
    def test_creates_summary_file(self, tmp_path):
        batch_dir = create_batch_dir(str(tmp_path))
        results = [("a.jpg", "b.jpg", _FakeResult())]
        summary = write_batch_summary(batch_dir, results)
        assert summary.exists()
        assert summary.name == "summary.txt"

    def test_contains_all_pair_names(self, tmp_path):
        batch_dir = create_batch_dir(str(tmp_path))
        results = [
            ("AADHAR001.jpg", "USER_01.jpg", _FakeResult()),
            ("AADHAR02.jpg", "USER_01.jpg", _FakeResult(cosine_score=0.20)),
        ]
        summary = write_batch_summary(batch_dir, results)
        text = summary.read_text(encoding="utf-8")
        assert "AADHAR001.jpg" in text
        assert "AADHAR02.jpg" in text
        assert "USER_01.jpg" in text

    def test_counts_matches(self, tmp_path):
        batch_dir = create_batch_dir(str(tmp_path))
        results = [
            ("a.jpg", "b.jpg", _FakeResult(match=True)),
            ("c.jpg", "d.jpg", _FakeResult(match=False)),
            ("e.jpg", "f.jpg", _FakeResult(match=True)),
        ]
        summary = write_batch_summary(batch_dir, results)
        text = summary.read_text(encoding="utf-8")
        assert "Matches: 2/3" in text
