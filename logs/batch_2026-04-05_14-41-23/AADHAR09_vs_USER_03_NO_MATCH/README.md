# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:55:51  
**Aadhaar:** FILES\AADHAR\AADHAR09.pdf  
**Selfie:** FILES\SELFIE\USER_03.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1099 |
| **Confidence** | 11.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 1.3342 (score: 0.1352) |
| **SSIM** | 0.2105 |
| **Landmark Score** | 0.6601 |
| **Pose Diff** | 8.9 deg |
| **Fused Score** | 0.2600 |
| **Aadhaar** | M, age 31 |
| **Selfie** | F, age 28 |
| **Age Gap** | 3 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.67, threshold=0.4)
  2. Cosine similarity: 0.1099 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 11.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1258ms total)
| Stage | Time |
|-------|------|
| load_ms | 40ms |
| enhancement_ms | 31ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 588ms |
| similarity_ms | 590ms |
| **TOTAL** | **1258ms** |
