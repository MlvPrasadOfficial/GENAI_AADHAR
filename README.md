# Aadhaar KYC Face Matching Pipeline v2

Local face verification system for KYC (Know Your Customer) workflows. Compares a face from an Aadhaar identity card against a live user selfie using deep learning embeddings, image preprocessing, and an optional Vision LLM guard.

## Key Features

- **ArcFace Embeddings** (InsightFace buffalo_l) -- 512-d cosine similarity matching
- **Cross-Age Handling** -- Age-gated threshold relaxation, age-conditioned VLM prompting
- **Image Preprocessing** -- Real-ESRGAN upscale, CLAHE contrast normalization, flip-augmented TTA
- **Dual-Path Embedding** -- Compares original vs preprocessed Aadhaar, keeps higher score
- **Vision LLM Guard** -- Ollama + Qwen2.5-VL-7B for uncertain-zone verification (bone-structure focused)
- **Batch Mode** -- Process multiple pairs from CSV
- **174 Unit Tests** -- Comprehensive coverage across all modules
- **Fully Configurable** -- All thresholds, bonuses, and penalties tunable via `config.yaml`

## Architecture

```
Image Loading (EXIF correction)
    |
Real-ESRGAN Enhancement (if quality < 0.4)
    |
CLAHE Contrast Normalization (Aadhaar only)
    |
Grayscale Normalization (optional, removes color domain gap)
    |
InsightFace Detection + Alignment + ArcFace Embedding
    |  + Flip-augmented TTA (horizontal flip + average)
    |  + Dual-path (original vs preprocessed, keep best)
    |
Cosine Similarity + Threshold Decision
    |
    +-- score >= 0.60 --> MATCH (skip VLM unless low quality)
    +-- 0.40 - 0.60  --> UNCERTAIN --> Ollama VLM Guard
    +-- score < 0.40  --> NO MATCH
    |
Age-Gap Threshold Relaxation (dynamic, up to -0.10)
    |
Decision Fusion (configurable confidence adjustments)
    |
Result Logging (per-run folders, decision trace, batch summary)
```

## Quick Start

```bash
# Activate environment
conda activate aadhar

# Single pair
python main.py --aadhaar FILES/AADHAR/AADHAR001.jpg --selfie FILES/SELFIE/USER_01.jpg --verbose

# Batch mode (CSV with aadhaar,selfie columns)
python main.py --batch pairs.csv --verbose

# JSON output
python main.py --aadhaar card.jpg --selfie selfie.jpg --json-output
```

### Exit Codes
| Code | Meaning |
|------|---------|
| 0 | MATCH (all match in batch) |
| 1 | NO MATCH (any no-match in batch) |
| 2 | ERROR |

## Configuration

All parameters are tunable in `config.yaml`:

```yaml
preprocessing:
  aadhaar_clahe: true          # CLAHE contrast normalization
  clahe_clip_limit: 2.0
  clahe_tile_size: 8
  dual_path: true              # Original vs preprocessed, keep best
  grayscale_normalize: false   # Experimental: removes color domain gap

similarity:
  match_threshold: 0.60
  uncertain_low: 0.40
  age_gap_threshold: 5         # Start relaxing after 5yr gap
  age_gap_relaxation_per_year: 0.01
  max_age_gap_relaxation: 0.10 # Cap: threshold never below 0.50

vlm_guard:
  enabled: true
  model: "qwen2.5vl:7b"
  timeout_s: 300

confidence_adjustments:
  vlm_confirmation_bonus: 8.0
  vlm_rejection_above_threshold: -20.0
  vlm_rejection_uncertain: -10.0
  quality_penalty: -5.0
  age_gap_vlm_bonus: 5.0
  gender_mismatch_penalty: 0.0
```

## Cross-Age Face Matching

The core challenge: Aadhaar photos are 5-15+ years old, printed on cards, and low quality. ArcFace wasn't designed for this age gap.

### How v2 Handles It

1. **Age-Gated Threshold Relaxation** -- When detected age gap > 5yr, match threshold is lowered proportionally (max -0.10, threshold never below 0.50)
2. **Age-Conditioned VLM Prompting** -- When age gap > 3yr, the VLM prompt focuses exclusively on bone-structure features (eye sockets, nose bridge, ear shape) and explicitly states that aging changes are EXPECTED
3. **CLAHE Preprocessing** -- Normalizes contrast of printed card photos before face detection
4. **Flip-Augmented TTA** -- Averages original and horizontally-flipped embeddings for noise reduction
5. **Dual-Path Embedding** -- Tries both original and preprocessed Aadhaar, keeps whichever gives higher cosine score
6. **Age-Gap VLM Bonus** -- Extra +5 confidence when VLM confirms match despite age gap

### Score Progression (AADHAR001 vs USER_01)
| Version | Cosine | Confidence | Result |
|---------|--------|------------|--------|
| v1 (base ArcFace) | 0.547 | 44.7% | NO MATCH |
| v1 + VLM prompt fix | 0.547 | 67.7% | MATCH |
| v2 (CLAHE + TTA + dual-path) | 0.574 | 70.4% | MATCH |

## Requirements

- Python 3.11 (conda env `aadhar`)
- NVIDIA GPU with CUDA 12.x (RTX 4080 tested)
- Ollama with `qwen2.5vl:7b` model pulled

### Installation

```bash
conda activate aadhar
pip install torch==2.3.1+cu121 torchvision==0.18.1+cu121 --extra-index-url https://download.pytorch.org/whl/cu121
pip install numpy==1.26.4
pip install onnxruntime-gpu==1.19.2
pip install basicsr==1.4.2
pip install realesrgan==0.3.0
pip install insightface==0.7.3
pip install opencv-python==4.10.0.84 Pillow==10.4.0 PyYAML==6.0.2 requests==2.32.3 tqdm==4.66.4 pytest==8.3.2

ollama pull qwen2.5vl:7b
python scripts/download_models.py
```

## Testing

```bash
# All unit tests (174 tests, no GPU needed)
pytest tests/ -v -m "not integration"

# Individual test suites
pytest tests/test_similarity.py -v           # 15 tests
pytest tests/test_config_loader.py -v        # 24 tests
pytest tests/test_vlm_guard.py -v            # 25 tests
pytest tests/test_image_utils.py -v          # 28 tests
pytest tests/test_enhancement.py -v          # 15 tests
pytest tests/test_face_processor.py -v       # 15 tests
pytest tests/test_orchestrator_unit.py -v    # 33 tests
pytest tests/test_result_logger.py -v        # 11 tests
pytest tests/test_batch_logging.py -v        # 8 tests

# Integration (requires models + GPU + Ollama)
pytest tests/test_pipeline.py -v -m integration
```

## Project Structure

```
main.py                     CLI entry point (single + batch mode)
config.yaml                 All tunable parameters
pipeline/
  orchestrator.py           Main pipeline runner (age-gated thresholds, dual-path, confidence fusion)
  enhancement.py            Real-ESRGAN wrapper
  face_processor.py         InsightFace wrapper (flip-augmented TTA)
  similarity.py             Cosine similarity + threshold logic
  vlm_guard.py              Ollama VLM HTTP client (age-conditioned prompting)
utils/
  image_utils.py            EXIF, BGR/RGB, base64, CLAHE, grayscale, dimensions
  config_loader.py          YAML config loader with comprehensive validation
  result_logger.py          Per-run log folders, decision trace, batch logging
  exceptions.py             Custom exceptions
scripts/
  download_models.py        Model weight downloader
models/                     Downloaded weights (gitignored)
tests/                      174 unit tests across 11 test files
pairs.csv                   Sample batch input
```

## Future Improvements

| Technique | Impact | Status |
|-----------|--------|--------|
| AdaFace as second model + score fusion | High | Planned |
| S-norm score calibration with impostor cohort | High | Planned |
| CR-FIQA quality-aware scoring | Medium | Planned |
| MTLFace age-invariant embeddings | Highest | Research |
| CodeFormer face restoration | Medium | Research |
| StyleGAN age normalization | High | Research |

## License

Research use only. InsightFace buffalo_l model is non-commercial license.
