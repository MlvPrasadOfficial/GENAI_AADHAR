# Aadhaar KYC Face Matching — Compact Reference

## Purpose
Local face matching for KYC: Aadhaar card face vs user selfie. Pure local Python CLI, no cloud, no UI.

## Environment
- Conda env `aadhar` (Python 3.11) — `conda activate aadhar`
- RTX 4080 Laptop 12GB VRAM, Windows 11, Git Bash
- SageMaker: `ml.g5.xlarge` (A10G 24GB), Python 3.10 venv

## Run
```bash
python main.py --aadhaar card.jpg --selfie user.jpg --verbose
python main.py --batch pairs.csv --verbose
```

## Pipeline (in order)
1. Load + EXIF + PDF → BGR numpy (`utils/image_utils.py`)
2. Real-ESRGAN upscale if quality < 0.4 (`pipeline/enhancement.py`)
3. CLAHE on Aadhaar + optional grayscale normalize
4. InsightFace buffalo_l: detect → align → 512-d ArcFace embed, flip TTA (`pipeline/face_processor.py`)
5. Similarity: Cosine 55% + Landmark 25% + L2 10% + SSIM 10% fused (`pipeline/similarity.py`)
6. Dual-path (original vs preprocessed), keep best cosine
7. S-norm impostor cohort calibration (`pipeline/score_norm.py`)
8. Qwen2.5-VL-7B-Instruct guard (HF transformers, local FP16) (`pipeline/vlm_guard.py`)
9. Platt scaling confidence calibration (`pipeline/confidence_calibrator.py`)
10. Per-run log folder with crops + README.md (`utils/result_logger.py`)

## Thresholds
- `>= 0.60` → MATCH
- `0.40–0.60` → UNCERTAIN → VLM guard decides
- `< 0.40` → NO MATCH
- Age gap > 3yr relaxes threshold by 0.015/yr (cap 0.12)   *(v3: earlier + stronger relaxation)*
- VLM soft-override: cosine ≥ 0.50 + VLM=false → soft `-5` penalty, keep match (printed-card landmarks unreliable)

## Key Files
- `main.py` — CLI entry
- `config.yaml` — all tunable params
- `pipeline/orchestrator.py` — wires stages, caching, calibration
- `pipeline/vlm_guard.py` — Qwen2.5-VL age-conditioned prompt
- `utils/result_logger.py` — log folders with decision trace
- `pairs.csv` — 90 test pairs (9 Aadhaar × 10 selfies, verified 9/90)

## Install (one-time)
```bash
pip install torch==2.3.1+cu121 torchvision==0.18.1+cu121 --extra-index-url https://download.pytorch.org/whl/cu121
pip install numpy==1.26.4 onnxruntime-gpu==1.19.2 basicsr==1.4.2 realesrgan==0.3.0 insightface==0.7.3
pip install opencv-python==4.10.0.84 Pillow==10.4.0 PyYAML==6.0.2 requests==2.32.3 tqdm==4.66.4 pytest==8.3.2 PyMuPDF==1.24.5
pip install transformers accelerate qwen-vl-utils "jinja2>=3.1.0"
python scripts/download_models.py
```

## Tests
```bash
pytest tests/ -v -m "not integration"   # 259 unit tests, no GPU
pytest tests/test_pipeline.py -v -m integration   # needs models + GPU
```

## Confidence Adjustments (config.yaml, v3)
```yaml
vlm_confirmation_bonus: 10.0              # v3: 8→10
vlm_rejection_above_threshold: -12.0      # v3: -20→-12
vlm_rejection_uncertain: -5.0             # v3: -10→-5
vlm_soft_override_cosine: 0.50            # v3 new: below this, use soft path
vlm_soft_override_penalty: -5.0           # v3 new
quality_penalty: -5.0
age_gap_vlm_bonus: 5.0
```

## v3 Ensemble & Preprocessing (config.yaml)
```yaml
face:
  enable_ensemble: true
  secondary_model: antelopev2      # glintr100 ArcFace, Glint360K
  ensemble_strategy: max            # max | mean | weighted (FN-leaning = max)
  secondary_weight: 0.5             # used only when strategy=weighted
enhancement:
  force_enhance_aadhaar: true       # always run Real-ESRGAN on Aadhaar crop
preprocessing:
  histogram_matching: true          # match Aadhaar histogram to selfie
similarity:
  quality_weighted_fusion: true     # at quality<0.3: cosine=0.80, landmark=0.10
```

## Pitfalls
- Remove CPU `onnxruntime` if `onnxruntime-gpu` is installed
- VLM needs 20GB+ VRAM (Qwen2.5-VL-7B-Instruct ~16.6GB FP16)
- `jinja2>=3.1.0` required for VLM chat template
- basicsr 1.4.2 needs patch for `torchvision.transforms.functional_tensor` (newer torchvision)
- InsightFace matplotlib crash in Jupyter → `os.environ['MPLBACKEND']='Agg'` before import
- PDF Aadhaar auto-detected via `%PDF-` magic bytes (needs PyMuPDF)
- buffalo_l = non-commercial research license only

## SageMaker Deployment
- Use `sagemaker/sagemaker_notebook.ipynb`
- Python venv (not conda) → always use `{sys.executable}` in `!` commands
- Set `MPLBACKEND=Agg` in all cells + shell commands
- Step 1 must be re-run after every kernel restart (`%cd` doesn't persist)
- Qwen2.5-VL model path configured in Step 4 (`LOCAL_MODEL_PATH`)
