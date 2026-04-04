# Aadhaar KYC Face Matching — Project Architecture

## End-to-End Pipeline Flow

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        AADHAAR KYC FACE MATCHING PIPELINE                       │
└─────────────────────────────────────────────────────────────────────────────────┘

  INPUT A                                                    INPUT B
  Aadhaar Card Image                                         User Selfie
  ~300-400 KB, low quality                                   ~80 KB, low quality
        │                                                          │
        ▼                                                          ▼
  ┌─────────────┐                                         ┌─────────────┐
  │ EXIF        │  utils/image_utils.py                   │ EXIF        │
  │ Correction  │  PIL.ImageOps.exif_transpose()          │ Correction  │
  │ + Load BGR  │  → bytes → BGR numpy array              │ + Load BGR  │
  └──────┬──────┘                                         └──────┬──────┘
         │                                                        │
         ▼                                                        ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                     STAGE 1: QUALITY ASSESSMENT                         │
  │                     pipeline/enhancement.py                              │
  │                     Laplacian variance → quality score [0.0 – 1.0]      │
  │                     quality < 0.4 → run Real-ESRGAN                     │
  │                     quality ≥ 0.4 → skip enhancement                    │
  └─────────────────────────────────────────────────────────────────────────┘
         │                                                        │
         ▼  (if quality < 0.4)                                   ▼  (if quality < 0.4)
  ┌─────────────┐                                         ┌─────────────┐
  │ Real-ESRGAN │  pipeline/enhancement.py                │ Real-ESRGAN │
  │ 2x upscale  │  RealESRGANer (FP16, GPU)               │ 2x upscale  │
  │ face restore│  model: RealESRGAN_x4plus.pth           │ face restore│
  └──────┬──────┘                                         └──────┬──────┘
         │                                                        │
         └──────────────────────┬─────────────────────────────────┘
                                │
                                ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                     STAGE 2: FACE DETECTION                              │
  │                     pipeline/face_processor.py                           │
  │                     InsightFace buffalo_l → RetinaFace-10GF              │
  │                     det_thresh=0.7 (fallback: 0.5)                      │
  │                     det_size=[640,640]  │  ctx_id=0 (GPU)               │
  │                                                                          │
  │   Aadhaar: pick face with highest det_score (ignore QR/logo faces)      │
  │   Selfie: pick largest/most-confident face                               │
  │                                                                          │
  │   → bbox (x1,y1,x2,y2) + det_score                                      │
  └─────────────────────────────────────────────────────────────────────────┘
         │ NO FACE → raise NoFaceDetectedError("aadhaar"/"selfie")
         │
         ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                     STAGE 3: FACE ALIGNMENT                              │
  │                     pipeline/face_processor.py  (same InsightFace call) │
  │                     5-point landmark detection → affine warp             │
  │                     insightface.utils.face_align.norm_crop()             │
  │                     → aligned face crop  112×112 BGR                    │
  └─────────────────────────────────────────────────────────────────────────┘
         │
         ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                     STAGE 4: FACE EMBEDDING                              │
  │                     pipeline/face_processor.py  (same InsightFace call) │
  │                     ArcFace R50 @ WebFace600K                           │
  │                     face.normed_embedding → 512-d float32 L2-normalized │
  │                                                                          │
  │   Aadhaar embedding: emb_A  [512]                                        │
  │   Selfie  embedding: emb_B  [512]                                        │
  └─────────────────────────────────────────────────────────────────────────┘
         │
         ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                     STAGE 5: COSINE SIMILARITY                           │
  │                     pipeline/similarity.py                               │
  │                     score = np.dot(emb_A, emb_B)   # already L2-norm'd │
  │                     range: [0.0, 1.0]                                    │
  └─────────────────────────────────────────────────────────────────────────┘
         │
         ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                     STAGE 6: THRESHOLD DECISION TREE                     │
  │                     pipeline/similarity.py                               │
  │                                                                          │
  │   score < 0.40  ────────────────────────────────────────► NO MATCH      │
  │                                                                          │
  │   0.40 ≤ score < 0.60  ──────────────────────► [VLM GUARD]             │
  │                                                                          │
  │   score ≥ 0.60                                                           │
  │     AND quality OK  ────────────────────────────────────► MATCH         │
  │     AND quality LOW ────────────────────────► [VLM GUARD]              │
  └─────────────────────────────────────────────────────────────────────────┘
         │ (when VLM needed)
         ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                     STAGE 7: VISION LLM GUARD (optional)                │
  │                     pipeline/vlm_guard.py                                │
  │                     Ollama HTTP API → http://localhost:11434/api/chat    │
  │                     Model: llava:13b  (llava:7b for speed)              │
  │                     Input: both 112×112 aligned crops as base64 JPEG    │
  │                     Prompt: structural face comparison (bone/jaw/eyes)  │
  │                     Output: {same_person, confidence, reasoning}        │
  │                                                                          │
  │   same_person=true + confidence=high/medium  ──────────► MATCH          │
  │   same_person=false OR confidence=low         ──────────► NO MATCH      │
  │   Ollama unavailable (None)                   ──────────► conservative  │
  │     score ≥ 0.60 → MATCH                                                │
  │     score < 0.60 → NO MATCH                                             │
  └─────────────────────────────────────────────────────────────────────────┘
         │
         ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                     OUTPUT: PipelineResult                               │
  │                     pipeline/orchestrator.py                             │
  │                                                                          │
  │   match:            bool                                                 │
  │   confidence_pct:   float  (0.0 – 99.0)                                 │
  │   cosine_score:     float  (raw ArcFace similarity)                     │
  │   vlm_same_person:  bool | None                                          │
  │   vlm_reasoning:    str | None                                           │
  │   aadhaar_quality:  float  (0.0 – 1.0)                                  │
  │   selfie_quality:   float                                                │
  │   stage_timings:    dict   (ms per stage)                               │
  │   error:            str | None                                           │
  └─────────────────────────────────────────────────────────────────────────┘
         │
         ▼
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                     CLI OUTPUT: main.py                                  │
  │                                                                          │
  │   ========================================                               │
  │     Result: MATCH                                                        │
  │     Confidence: 84.2%                                                    │
  │     Cosine score: 0.6821                                                 │
  │     VLM: Matching eye socket depth and nose bridge width...             │
  │   ========================================                               │
  └─────────────────────────────────────────────────────────────────────────┘
```

---

## Module Dependency Map

```
main.py
  └── pipeline/orchestrator.py
        ├── pipeline/enhancement.py
        │     └── (realesrgan, basicsr, torch)
        ├── pipeline/face_processor.py
        │     └── (insightface, onnxruntime-gpu)
        ├── pipeline/similarity.py
        │     └── (numpy)
        ├── pipeline/vlm_guard.py
        │     └── (requests → Ollama HTTP API)
        └── utils/
              ├── config_loader.py  ← (PyYAML)
              ├── image_utils.py    ← (PIL, opencv-python)
              └── exceptions.py
```

---

## Technology Stack

```
┌──────────────────────────────────────────────────────────────────┐
│  Layer          │  Technology                │  Version          │
├──────────────────────────────────────────────────────────────────┤
│  Enhancement    │  Real-ESRGAN               │  0.3.0            │
│                 │  basicsr (backbone)         │  1.4.2            │
│                 │  PyTorch (GPU inference)    │  2.3.1+cu121      │
├──────────────────────────────────────────────────────────────────┤
│  Face Pipeline  │  InsightFace buffalo_l      │  0.7.3            │
│  (detect+align  │  ├─ RetinaFace-10GF (det)  │  ONNX             │
│  +embed)        │  ├─ 2D106 landmarks (align) │  ONNX             │
│                 │  └─ ArcFace R50 (embed)     │  ONNX             │
│                 │  ONNX Runtime GPU           │  1.19.2           │
├──────────────────────────────────────────────────────────────────┤
│  Similarity     │  NumPy cosine dot product   │  1.26.4           │
├──────────────────────────────────────────────────────────────────┤
│  Vision LLM     │  Ollama (Windows native)    │  0.20.0           │
│  Guard          │  LLaVA-v1.6                 │  13b              │
│  (optional)     │  HTTP API: localhost:11434  │                   │
├──────────────────────────────────────────────────────────────────┤
│  Image I/O      │  OpenCV                     │  4.10.0.84        │
│                 │  Pillow                     │  10.4.0           │
├──────────────────────────────────────────────────────────────────┤
│  Config         │  PyYAML                     │  6.0.2            │
│  CLI            │  argparse (stdlib)          │                   │
│  Testing        │  pytest                     │  8.3.2            │
└──────────────────────────────────────────────────────────────────┘
```

---

## Decision Flow (simplified)

```
score = ArcFace cosine similarity(aadhaar_embedding, selfie_embedding)

if score < 0.40:
    return NO_MATCH  (no VLM needed — clear rejection)

elif score >= 0.60 and not quality_low:
    return MATCH     (no VLM needed — clear acceptance)

else:  # uncertain zone (0.40–0.60) OR high score but low quality
    vlm = ollama_llava_verify(aadhaar_crop, selfie_crop, score)
    
    if vlm.same_person and vlm.confidence in ("high", "medium"):
        return MATCH
    elif vlm is None:  # Ollama not running
        return MATCH if score >= 0.60 else NO_MATCH  # fallback to score
    else:
        return NO_MATCH
```

---

## Performance Expectations (RTX 4080 Laptop 12GB)

| Stage | Typical Time |
|---|---|
| Real-ESRGAN (2x, FP16) | 200–400 ms |
| Face detection (RetinaFace) | 50–100 ms |
| ArcFace embedding | 20–50 ms |
| Cosine similarity | < 1 ms |
| LLaVA-13b via Ollama | 3–8 sec |
| **Total (no VLM)** | **~0.3–0.6 sec** |
| **Total (with VLM)** | **~4–9 sec** |
