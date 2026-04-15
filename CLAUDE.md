# Aadhaar KYC Face Matching Pipeline

## Project Purpose
Local face matching system for KYC verification. Compares a face in an Aadhaar card image (~300-400KB, low quality) against a user selfie (~80KB, low quality). No cloud, no web UI — pure local Python CLI.

## Environment
- **Conda env**: `aadhar` (Python 3.11)
- **Activate**: `conda activate aadhar`
- **Hardware**: RTX 4080 Laptop 12GB VRAM, Windows 11, Git Bash

## Run the Pipeline
```bash
conda activate aadhar
# Single pair (supports JPG, PNG, PDF Aadhaar cards)
python main.py --aadhaar path/to/aadhaar_card.jpg --selfie path/to/selfie.jpg
python main.py --aadhaar aadhaar.pdf --selfie selfie.jpg --verbose
python main.py --aadhaar card.jpg --selfie selfie.jpg --json-output

# Batch mode (CSV with aadhaar,selfie columns)
python main.py --batch pairs.csv --verbose
```

## Pipeline Stages (in order)
1. `utils/image_utils.py` — EXIF correction, load bytes → BGR numpy (with input type/size validation, PDF support via PyMuPDF)
2. `pipeline/enhancement.py` — Real-ESRGAN upscale (skipped if quality >= 0.4; warns if unavailable)
2b. `utils/image_utils.py` — CLAHE contrast normalization for Aadhaar card images (configurable)
2c. `utils/image_utils.py` — Optional grayscale normalization (removes color domain gap between printed/live)
3. `pipeline/face_processor.py` — InsightFace buffalo_l: detect → align → 512-d ArcFace embed (multi-face warning, GPU check, flip/ensemble TTA)
3b. `pipeline/crop_restore.py` — Optional crop-level restoration (bilateral filter or GFPGAN)
4. `pipeline/similarity.py` — Cosine + L2 + SSIM + landmark geometry + fused score, adaptive thresholds
4b. `pipeline/orchestrator.py` — Dual-path: compare original vs preprocessed Aadhaar, keep higher cosine score
4c. `pipeline/adaface.py` — Optional AdaFace second model with score fusion
4d. `pipeline/score_norm.py` — S-norm score calibration against impostor cohort
5. `pipeline/vlm_guard.py` — HuggingFace Qwen2.5-VL-7B-Instruct guard (local inference, strict JSON parsing, age-conditioned prompting)
6. `pipeline/orchestrator.py` — Wires all stages, age-gated thresholds, configurable confidence adjustments
6b. `pipeline/confidence_calibrator.py` — Platt scaling for calibrated confidence probabilities
7. `utils/result_logger.py` — Per-run log folder with hash-based deduplication and decision trace
8. `utils/embedding_cache.py` — LRU embedding cache (skips reprocessing same images in batch)

## Key Design Decisions
| Aspect | Decision | Reason |
|---|---|---|
| Enhancement | Real-ESRGAN (NOT GFPGAN) | GFPGAN causes identity drift; Real-ESRGAN preserves structure |
| Face model | InsightFace buffalo_l | All-in-one: RetinaFace + ArcFace in one ONNX pack |
| Match threshold | >= 0.60 | Calibrated on 60k-face database (2024 research) |
| Uncertain zone | 0.40-0.60 | Escalate to VLM guard |
| Vision LLM | HuggingFace Qwen2.5-VL-7B-Instruct | Direct local inference via transformers, no Ollama dependency, FP16 on 20GB+ VRAM |
| Python version | 3.11 | Best InsightFace + ONNX Runtime GPU compatibility |
| NumPy | < 2.0 (pinned 1.26.4) | InsightFace not numpy 2.x compatible |
| Confidence tuning | config.yaml `confidence_adjustments` | All score adjustments (VLM bonus/penalty, quality penalty) are configurable without code changes |
| CLAHE preprocessing | Applied to Aadhaar only | Normalizes contrast of printed card photos before face detection |
| Flip augment (TTA) | Horizontal flip + average embedding | Reduces noise in ArcFace embeddings, improves cross-pose robustness |
| Dual-path embedding | Original vs preprocessed, keep best | Catches cases where enhancement/CLAHE hurts recognition |
| Grayscale normalize | Optional, removes color domain gap | Eliminates print color cast differences (experimental, off by default) |
| Multi-metric fusion | Cosine 55% + Landmark 25% + L2 10% + SSIM 10% | Multiple signals reduce single-metric noise |
| Adaptive thresholds | Quality-tier based (high/medium/low) | Stricter for good images, relaxed for poor |
| Quality-weighted fusion | Dynamic weights by quality score | Low quality → more weight on bone structure |
| S-norm calibration | Impostor cohort z-score normalization | Quality-independent calibrated scores |
| Confidence calibration | Platt scaling (sigmoid mapping) | Meaningful probability percentages |
| Crop restoration | Bilateral filter on 112x112 crops | Denoise without identity drift |
| Embedding cache | LRU by SHA-256 hash of image bytes | Avoids redundant processing in batch mode |
| Embedding ensemble | Multi-augmentation TTA (flip+brightness+blur) | More robust than single-augmentation |
| AdaFace second model | Quality-adaptive face recognition | Cross-validates with ArcFace (optional) |
| Parallel batch | ThreadPoolExecutor for concurrent pairs | Faster batch processing |
| PDF Aadhaar input | PyMuPDF embedded image extraction + pixmap fallback | Supports scanned PDF Aadhaar cards natively |

## Similarity Thresholds
- `cosine_score >= match_threshold (0.60)` → **MATCH** (skip VLM unless quality is low)
- `uncertain_low (0.40) <= cosine_score < match_threshold` → **UNCERTAIN** → invoke VLM guard (Qwen2.5-VL)
- `cosine_score < uncertain_low (0.40)` → **NO MATCH** (skip VLM)

## Age-Gap Threshold Relaxation
When detected age gap > 5yr, thresholds are dynamically relaxed:
- `age_gap_relaxation_per_year: 0.01` — lower threshold per year beyond 5yr gap
- `max_age_gap_relaxation: 0.10` — cap (threshold never drops below 0.50)
- VLM prompt dynamically injects age-stable structural feature guidance when gap > 3yr
- Extra `age_gap_vlm_bonus: 5.0` when VLM confirms match despite age gap

## Confidence Adjustments (configurable in config.yaml)
```yaml
confidence_adjustments:
  vlm_confirmation_bonus: 8.0        # VLM confirms match
  vlm_rejection_above_threshold: -20.0  # VLM rejects despite high cosine
  vlm_rejection_uncertain: -10.0     # VLM rejects in uncertain zone
  quality_penalty: -5.0              # Low image quality deduction
  age_gap_vlm_bonus: 5.0             # Extra bonus when VLM confirms AND age_gap > 5yr
  gender_mismatch_penalty: 0.0       # Disabled by default (InsightFace gender unreliable on printed cards)
```

## Config Validation
`config_loader.py` validates all fields at startup:
- Similarity thresholds in [0.0, 1.0], `uncertain_low < match_threshold`
- `det_size` must be 2-element list with positive integers
- `det_thresh_fallback` in [0.0, 1.0] and < `det_thresh`
- `upscale` must be positive
- `quality_threshold` in [0.0, 1.0]
- `max_new_tokens` must be positive integer
- `confidence_adjustments` values must be numeric
- `age_gap_threshold` non-negative, `age_gap_relaxation_per_year` non-negative
- `max_age_gap_relaxation` won't push threshold below `uncertain_low`
- `clahe_clip_limit` must be positive, `clahe_tile_size` must be positive integer

## Dependencies Setup (one-time)
```bash
conda activate aadhar
# Install order matters — do NOT rearrange
pip install torch==2.3.1+cu121 torchvision==0.18.1+cu121 --extra-index-url https://download.pytorch.org/whl/cu121
pip install numpy==1.26.4
pip install onnxruntime-gpu==1.19.2
pip install basicsr==1.4.2
pip install realesrgan==0.3.0
pip install insightface==0.7.3
pip install opencv-python==4.10.0.84 Pillow==10.4.0 PyYAML==6.0.2 requests==2.32.3 tqdm==4.66.4 pytest==8.3.2 PyMuPDF==1.24.5
pip install transformers accelerate qwen-vl-utils

# Download model weights
python scripts/download_models.py
```

## Verify GPU Setup
```python
import onnxruntime
print(onnxruntime.get_available_providers())
# Expected: ['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']
```

## Windows CUDA PATH Requirements
Ensure these are in system PATH:
- `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.x\bin`
- `C:\Program Files\NVIDIA\CUDNN\v9.x\bin\12.x`

## Testing
```bash
pytest tests/ -v -m "not integration"        # all unit tests (241 tests, no GPU needed)
pytest tests/test_similarity.py -v           # similarity + L2 + SSIM + landmarks + fusion (43 tests)
pytest tests/test_new_features.py -v         # cache, S-norm, calibrator, crop restore, adaptive, AdaFace (36 tests)
pytest tests/test_config_loader.py -v        # config validation (24 tests)
pytest tests/test_vlm_guard.py -v            # VLM parsing + inference + age prompt (22 tests)
pytest tests/test_image_utils.py -v          # image I/O + input validation + CLAHE + grayscale + dimensions + PDF (31 tests)
pytest tests/test_result_logger.py -v        # audit log + age-gap trace (11 tests)
pytest tests/test_enhancement.py -v          # quality scoring + downscale (15 tests)
pytest tests/test_face_processor.py -v       # face detection + multi-face + flip/ensemble augment (15 tests)
pytest tests/test_orchestrator_unit.py -v    # decision fusion + age relaxation + VLM bonus + preprocessing (33 tests)
pytest tests/test_batch_logging.py -v        # batch logging (8 tests)
pytest tests/test_pipeline.py -v -m integration  # needs models + GPU
```

## File Map
```
main.py                           CLI entry point (single + batch + parallel mode)
config.yaml                       All tunable parameters (thresholds, features, adjustments)
pipeline/orchestrator.py          Main pipeline runner (caching, crop restore, S-norm, calibration)
pipeline/enhancement.py           Real-ESRGAN wrapper (GPU warning, warns when unavailable)
pipeline/face_processor.py        InsightFace wrapper (flip/ensemble TTA, multi-face warning)
pipeline/similarity.py            Cosine + L2 + SSIM + landmarks + fused score, adaptive thresholds
pipeline/vlm_guard.py             HuggingFace Qwen2.5-VL local inference (age-conditioned prompting)
pipeline/score_norm.py            S-norm score calibration (impostor cohort z-normalization)
pipeline/confidence_calibrator.py Platt scaling confidence calibration
pipeline/crop_restore.py          Crop-level face restoration (bilateral/GFPGAN)
pipeline/adaface.py               AdaFace second model integration (optional)
utils/image_utils.py              EXIF, BGR/RGB, base64, CLAHE, grayscale, dimensions, PDF extraction
utils/config_loader.py            YAML config loader with validation
utils/result_logger.py            Per-run log folders with decision trace, batch README
utils/embedding_cache.py          LRU embedding cache by image hash
utils/exceptions.py               Custom exceptions
scripts/download_models.py        Model weight downloader
models/                           Downloaded weights (gitignored)
pairs.csv                         90 test pairs (9 Aadhaar × 10 selfies, full matrix)
tests/                            241 unit tests across 11 test files
```

## Known Pitfalls
- If `onnxruntime` (CPU) is installed alongside `onnxruntime-gpu`, GPU won't be used. Fix: `pip uninstall onnxruntime`
- InsightFace uses `INSIGHTFACE_ROOT` env var to locate buffalo_l weights
- Aadhaar cards may be photographed sideways — EXIF correction handles this
- VLM guard requires 20GB+ VRAM for FP16 inference (Qwen2.5-VL-7B-Instruct is ~16.6GB)
- buffalo_l is non-commercial research license only
- Enhancement silently skips if model weights are missing — check logs for warnings
- VLM response parsing falls back to regex if model returns non-JSON — check `raw_response` in logs
- PDF Aadhaar cards require PyMuPDF (`fitz`) — auto-detected via `%PDF-` magic bytes in file header

## Test Data
- `FILES/AADHAR/` — 9 Aadhaar cards (4 JPG + 5 PDF)
- `FILES/SELFIE/` — 10 selfie photos (JPG)
- `pairs.csv` — Full 90-pair matrix (9 × 10), verified result: 9/90 matches
