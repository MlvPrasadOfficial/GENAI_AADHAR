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
python main.py --aadhaar path/to/aadhaar_card.jpg --selfie path/to/selfie.jpg
python main.py --aadhaar card.jpg --selfie selfie.jpg --verbose
python main.py --aadhaar card.jpg --selfie selfie.jpg --json-output
```

## Pipeline Stages (in order)
1. `utils/image_utils.py` — EXIF correction, load bytes → BGR numpy
2. `pipeline/enhancement.py` — Real-ESRGAN upscale (skipped if quality >= 0.4)
3. `pipeline/face_processor.py` — InsightFace buffalo_l: detect → align → 512-d ArcFace embed
4. `pipeline/similarity.py` — Cosine similarity + threshold decision
5. `pipeline/vlm_guard.py` — Ollama LLaVA-13b (only invoked when score is 0.40–0.60 OR quality low)
6. `pipeline/orchestrator.py` — Wires all stages, returns `PipelineResult`

## Key Design Decisions
| Aspect | Decision | Reason |
|---|---|---|
| Enhancement | Real-ESRGAN (NOT GFPGAN) | GFPGAN causes identity drift; Real-ESRGAN preserves structure |
| Face model | InsightFace buffalo_l | All-in-one: RetinaFace + ArcFace in one ONNX pack |
| Match threshold | ≥ 0.60 | Calibrated on 60k-face database (2024 research) |
| Uncertain zone | 0.40–0.60 | Escalate to VLM guard |
| Vision LLM | Ollama + LLaVA-13b | vLLM has NO native Windows support; Ollama is Windows-native |
| Python version | 3.11 | Best InsightFace + ONNX Runtime GPU compatibility |
| NumPy | < 2.0 (pinned 1.26.4) | InsightFace not numpy 2.x compatible |

## Similarity Thresholds
- `cosine_score >= 0.60` → **MATCH** (skip VLM unless quality is low)
- `0.40 <= cosine_score < 0.60` → **UNCERTAIN** → invoke Ollama VLM guard
- `cosine_score < 0.40` → **NO MATCH** (skip VLM)

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
pip install opencv-python==4.10.0.84 Pillow==10.4.0 PyYAML==6.0.2 requests==2.32.3 tqdm==4.66.4 pytest==8.3.2

# Ollama (already installed on this machine)
ollama pull llava:13b

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
pytest tests/test_similarity.py -v           # no GPU needed
pytest tests/ -v -m "not integration"        # mock tests only
pytest tests/test_pipeline.py -v -m integration  # needs models + GPU
```

## File Map
```
main.py                     CLI entry point
config.yaml                 All tunable parameters
pipeline/orchestrator.py    Main pipeline runner
pipeline/enhancement.py     Real-ESRGAN wrapper
pipeline/face_processor.py  InsightFace wrapper
pipeline/similarity.py      Cosine + threshold logic
pipeline/vlm_guard.py       Ollama LLaVA HTTP client
utils/image_utils.py        EXIF, BGR/RGB, base64 helpers
utils/config_loader.py      YAML config loader
utils/exceptions.py         Custom exceptions
scripts/download_models.py  Model weight downloader
models/                     Downloaded weights (gitignored)
```a

## Known Pitfalls
- If `onnxruntime` (CPU) is installed alongside `onnxruntime-gpu`, GPU won't be used. Fix: `pip uninstall onnxruntime`
- InsightFace uses `INSIGHTFACE_ROOT` env var to locate buffalo_l weights
- Aadhaar cards may be photographed sideways — EXIF correction handles this
- Ollama must be running: `ollama serve` (auto-starts on Windows after install)
- buffalo_l is non-commercial research license only
2