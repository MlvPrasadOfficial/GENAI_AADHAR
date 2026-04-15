# SageMaker Setup — Exact Same Pipeline

Run the identical pipeline on SageMaker, including Ollama + Qwen2.5-VL.

## Requirements

- **Instance type:** `ml.g5.xlarge` (A10G 24GB) — runs all models including VLM
- **Volume size:** 100GB (models ~12GB + Ollama ~6GB)
- **Kernel:** `conda_python3`

## What Gets Installed

| Component | Size | Purpose |
|-----------|------|---------|
| PyTorch + CUDA | ~3GB | GPU compute |
| InsightFace buffalo_l | ~300MB | Face detection + ArcFace embedding |
| Real-ESRGAN | ~64MB | Image enhancement |
| Ollama | ~1GB | LLM runtime |
| Qwen2.5-VL:7B | ~5GB | Vision LLM guard |

## Steps

1. Create SageMaker Notebook Instance (`ml.g5.xlarge`, 100GB volume)
2. Open `sagemaker_notebook.ipynb`
3. Run all cells top to bottom
4. Upload your test images to `FILES/AADHAR/` and `FILES/SELFIE/`
5. Run the pipeline

## If Models Are Already on S3/EFS

Skip the download steps and copy directly:

```bash
# From S3
aws s3 cp s3://your-bucket/models/ models/ --recursive

# From EFS
cp -r /efs/shared-models/insightface models/insightface
cp -r /efs/shared-models/realesrgan models/realesrgan

# Ollama models from HuggingFace local download
# Copy the GGUF file and create Ollama model from it:
ollama create qwen2.5vl:7b -f /path/to/Modelfile
```

## Everything Runs Exactly As Local

- VLM guard: enabled (Ollama installed on the instance)
- GPU: CUDA for Real-ESRGAN + ONNX Runtime + Ollama
- Same config.yaml, same thresholds, same results
- No code changes needed
