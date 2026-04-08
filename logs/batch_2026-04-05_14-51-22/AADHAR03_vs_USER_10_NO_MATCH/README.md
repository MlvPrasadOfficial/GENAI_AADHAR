# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:57:56  
**Aadhaar:** FILES\AADHAR\AADHAR03.jpg  
**Selfie:** FILES\SELFIE\USER_10.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0930 |
| **Confidence** | 9.3% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.3469 (score: 0.1326) |
| **SSIM** | 0.3902 |
| **Landmark Score** | 0.3464 |
| **Pose Diff** | 6.2 deg |
| **Fused Score** | 0.1900 |
| **Aadhaar** | F, age 33 |
| **Selfie** | M, age 21 |
| **Age Gap** | 12 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.0930 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 12yr gap → threshold relaxed by 0.070 (effective: match=0.530, uncertain=0.330)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 9.3% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (7689ms total)
| Stage | Time |
|-------|------|
| load_ms | 134ms |
| enhancement_ms | 6470ms |
| clahe_ms | 48ms |
| face_processing_ms | 0ms |
| dual_path_ms | 518ms |
| similarity_ms | 519ms |
| **TOTAL** | **7689ms** |
