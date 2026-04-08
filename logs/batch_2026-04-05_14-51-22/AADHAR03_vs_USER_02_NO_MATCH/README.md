# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:57:29  
**Aadhaar:** FILES\AADHAR\AADHAR03.jpg  
**Selfie:** FILES\SELFIE\USER_02.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2570 |
| **Confidence** | 25.7% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.2191 (score: 0.1606) |
| **SSIM** | 0.3217 |
| **Landmark Score** | 0.5561 |
| **Pose Diff** | 8.7 deg |
| **Fused Score** | 0.3286 |
| **Aadhaar** | F, age 36 |
| **Selfie** | M, age 31 |
| **Age Gap** | 5 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.92, threshold=0.4)
  2. Cosine similarity: 0.2570 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 25.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1456ms total)
| Stage | Time |
|-------|------|
| load_ms | 140ms |
| enhancement_ms | 113ms |
| clahe_ms | 49ms |
| face_processing_ms | 0ms |
| dual_path_ms | 576ms |
| similarity_ms | 577ms |
| **TOTAL** | **1456ms** |
