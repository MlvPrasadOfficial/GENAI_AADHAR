# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:57:03  
**Aadhaar:** FILES\AADHAR\AADHAR09.pdf  
**Selfie:** FILES\SELFIE\USER_10.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0091 |
| **Confidence** | 0.9% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.4077 (score: 0.1210) |
| **SSIM** | 0.2653 |
| **Landmark Score** | 0.3443 |
| **Pose Diff** | 7.2 deg |
| **Fused Score** | 0.1297 |
| **Aadhaar** | M, age 39 |
| **Selfie** | M, age 21 |
| **Age Gap** | 18 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.0091 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 18yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 0.9% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (16107ms total)
| Stage | Time |
|-------|------|
| load_ms | 42ms |
| enhancement_ms | 14976ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 540ms |
| similarity_ms | 542ms |
| **TOTAL** | **16107ms** |
