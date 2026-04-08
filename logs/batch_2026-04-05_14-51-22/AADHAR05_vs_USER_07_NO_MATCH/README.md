# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 15:00:26  
**Aadhaar:** FILES\AADHAR\AADHAR05.pdf  
**Selfie:** FILES\SELFIE\USER_07.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0895 |
| **Confidence** | 9.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.3494 (score: 0.1321) |
| **SSIM** | 0.3544 |
| **Landmark Score** | 0.3814 |
| **Pose Diff** | 13.8 deg |
| **Fused Score** | 0.1932 |
| **Aadhaar** | F, age 33 |
| **Selfie** | M, age 38 |
| **Age Gap** | 5 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.0895 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 9.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (7633ms total)
| Stage | Time |
|-------|------|
| load_ms | 44ms |
| enhancement_ms | 6579ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 499ms |
| similarity_ms | 502ms |
| **TOTAL** | **7633ms** |
