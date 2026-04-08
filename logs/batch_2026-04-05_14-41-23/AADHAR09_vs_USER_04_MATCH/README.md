# KYC Face Match — MATCH

**Timestamp:** 2026-04-05 14:56:29  
**Aadhaar:** FILES\AADHAR\AADHAR09.pdf  
**Selfie:** FILES\SELFIE\USER_04.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | MATCH |
| **Cosine Score** | 0.6337 |
| **Confidence** | 66.4% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 0.8560 (score: 0.2769) |
| **SSIM** | 0.2814 |
| **Landmark Score** | 0.4999 |
| **Pose Diff** | 9.0 deg |
| **Fused Score** | 0.5293 |
| **Aadhaar** | M, age 39 |
| **Selfie** | F, age 42 |
| **Age Gap** | 3 years |
| **VLM Verdict** | Same person |
| **VLM Reasoning** | The eye socket shape, inter-pupillary distance, and nose bridge width and profile are consistent, indicating the same bone structure. |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.6337 → MATCH zone (>= 0.6 match threshold)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Invoked — high cosine score but low image quality → double-checking
     VLM verdict: SAME PERSON
  5. Final decision: MATCH at 66.4% confidence
     Confidence breakdown: base 63.4% → +8 VLM confirmation → -5 quality penalty
     Reason: Score above threshold, VLM confirmed despite low quality images
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (38739ms total)
| Stage | Time |
|-------|------|
| load_ms | 36ms |
| enhancement_ms | 15098ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 561ms |
| similarity_ms | 564ms |
| vlm_ms | 22472ms |
| **TOTAL** | **38739ms** |
