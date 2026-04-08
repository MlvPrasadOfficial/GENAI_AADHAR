# KYC Face Match — MATCH

**Timestamp:** 2026-04-05 14:54:42  
**Aadhaar:** FILES\AADHAR\AADHAR08.pdf  
**Selfie:** FILES\SELFIE\USER_05.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | MATCH |
| **Cosine Score** | 0.5615 |
| **Confidence** | 64.1% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 0.9365 (score: 0.2454) |
| **SSIM** | 0.4157 |
| **Landmark Score** | 0.3644 |
| **Pose Diff** | 33.3 deg |
| **Fused Score** | 0.4660 |
| **Aadhaar** | F, age 22 |
| **Selfie** | F, age 25 |
| **Age Gap** | 3 years |
| **VLM Verdict** | Same person |
| **VLM Reasoning** | The eye socket shape, inter-pupillary distance, and nose bridge width are consistent, indicating the same bone structure. |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.5615 → UNCERTAIN zone (between 0.4 and 0.6)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Invoked — cosine score in uncertain zone → VLM decides
     VLM verdict: SAME PERSON
  5. Final decision: MATCH at 64.1% confidence
     Confidence breakdown: base 56.1% → +8 VLM confirmation
     Reason: Score in uncertain zone, but VLM confirmed same person
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (24015ms total)
| Stage | Time |
|-------|------|
| load_ms | 39ms |
| enhancement_ms | 44ms |
| clahe_ms | 13ms |
| face_processing_ms | 0ms |
| dual_path_ms | 574ms |
| similarity_ms | 576ms |
| vlm_ms | 22769ms |
| **TOTAL** | **24015ms** |
