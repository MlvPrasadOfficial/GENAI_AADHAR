# SageMaker Deployment Guide

## Quick Start

1. Create a **SageMaker Notebook Instance** with GPU:
   - Instance type: `ml.g5.xlarge` (A10G 24GB) or `ml.g4dn.xlarge` (T4 16GB)
   - Volume: 50GB minimum
   - Platform: `conda_python3` kernel

2. Open `sagemaker_notebook.ipynb` and follow steps 1-7

## Model Setup

The pipeline needs these model files:

```
models/
  insightface/models/buffalo_l/
    1k3d68.onnx          # 68-point 3D landmarks
    2d106det.onnx         # 106-point 2D landmarks
    det_10g.onnx          # RetinaFace detector
    genderage.onnx        # Gender + age estimator
    w600k_r50.onnx        # ArcFace R50 embedding
  realesrgan/
    RealESRGAN_x4plus.pth # Super-resolution model
```

### If models are already downloaded from HuggingFace:

```bash
# From HuggingFace cache
cp -r ~/.cache/huggingface/hub/models--buffalo_l/ models/insightface/models/buffalo_l/

# Or from S3
aws s3 cp s3://your-bucket/models/ models/ --recursive

# Or symlink from shared EFS
ln -s /efs/shared-models/insightface models/insightface
```

### If models need downloading:

```bash
python scripts/download_models.py
```

## Key Differences from Local Setup

| Feature | Local (Windows) | SageMaker |
|---------|----------------|-----------|
| GPU | RTX 4080 (CUDA) | A10G/T4/V100 (CUDA) |
| VLM Guard | Ollama + Qwen2.5-VL | **Disabled** (no Ollama) |
| Models | `models/` directory | S3 or EFS mount |
| Results | `logs/` directory | `logs/` + S3 upload |
| Python | conda env `aadhar` | SageMaker kernel |

## VLM Guard Alternatives on SageMaker

Since Ollama is not available on SageMaker, options are:

1. **Disable VLM** (default in this setup) — pipeline uses cosine + multi-metric scoring only
2. **Amazon Bedrock** — swap `vlm_guard.py` to call Claude/Nova vision via Bedrock API
3. **SageMaker Endpoint** — deploy Qwen2.5-VL as a real-time endpoint, update `ollama_url` to point to it
4. **Self-hosted Ollama** — run Ollama on a separate EC2 GPU instance, set `ollama_url` to its IP

## Running Without VLM

Without VLM, the decision logic changes:
- Score >= 0.60 → **MATCH** (no VLM confirmation needed)
- 0.40 <= Score < 0.60 → **NO MATCH** (VLM would normally resolve these)
- Score < 0.40 → **NO MATCH**

This means some borderline matches (0.40-0.60 range) that VLM would confirm will be rejected. For higher recall, consider lowering `match_threshold` to 0.55 in `config.yaml`.

## Batch Processing on SageMaker

For large-scale batch processing, use SageMaker Processing Jobs:

```python
from sagemaker.processing import ScriptProcessor

processor = ScriptProcessor(
    image_uri='your-ecr-image',
    role='your-sagemaker-role',
    instance_count=1,
    instance_type='ml.g5.xlarge',
    command=['python3']
)

processor.run(
    code='main.py',
    arguments=['--batch', '/opt/ml/processing/input/pairs.csv', '--verbose'],
    inputs=[ProcessingInput(source='s3://bucket/data/', destination='/opt/ml/processing/input/')],
    outputs=[ProcessingOutput(source='/opt/ml/processing/output/', destination='s3://bucket/results/')]
)
```
