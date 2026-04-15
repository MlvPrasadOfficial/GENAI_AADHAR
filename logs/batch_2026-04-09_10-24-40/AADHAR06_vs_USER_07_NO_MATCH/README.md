# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:38:22  
**Aadhaar:** FILES\AADHAR\AADHAR06.pdf  
**Selfie:** FILES\SELFIE\USER_07.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.5986 |
| **Confidence** | 49.9% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 0.8960 (score: 0.2608) |
| **SSIM** | 0.3271 |
| **Landmark Score** | 0.3785 |
| **Pose Diff** | 15.6 deg |
| **Fused Score** | 0.4826 |
| **Aadhaar** | M, age 38 |
| **Selfie** | M, age 38 |
| **Age Gap** | 0 years |
| **VLM Reasoning** | Ollama request failed (timeout or HTTP error) |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.5986 → UNCERTAIN zone (between 0.4 and 0.6)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Invoked — cosine score in uncertain zone → VLM decides
     VLM verdict: UNAVAILABLE (Ollama timeout or error)
  5. Final decision: NO MATCH at 49.9% confidence
     Reason: Score in uncertain zone, VLM unavailable — conservative rejection
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (309265ms total)
| Stage | Time |
|-------|------|
| load_ms | 42ms |
| enhancement_ms | 6230ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 459ms |
| similarity_ms | 460ms |
| vlm_ms | 302066ms |
| **TOTAL** | **309265ms** |
