# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:30:20  
**Aadhaar:** FILES\AADHAR\AADHAR03.jpg  
**Selfie:** FILES\SELFIE\USER_07.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1483 |
| **Confidence** | 14.8% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.3052 (score: 0.1412) |
| **SSIM** | 0.4785 |
| **Landmark Score** | 0.5360 |
| **Pose Diff** | 9.6 deg |
| **Fused Score** | 0.2775 |
| **Aadhaar** | F, age 36 |
| **Selfie** | M, age 38 |
| **Age Gap** | 2 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.1483 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 14.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (7534ms total)
| Stage | Time |
|-------|------|
| load_ms | 136ms |
| enhancement_ms | 6349ms |
| clahe_ms | 48ms |
| face_processing_ms | 0ms |
| dual_path_ms | 499ms |
| similarity_ms | 502ms |
| **TOTAL** | **7534ms** |
