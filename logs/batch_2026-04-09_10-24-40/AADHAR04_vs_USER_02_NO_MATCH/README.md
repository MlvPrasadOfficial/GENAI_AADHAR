# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:30:51  
**Aadhaar:** FILES\AADHAR\AADHAR04.jpg  
**Selfie:** FILES\SELFIE\USER_02.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0307 |
| **Confidence** | 3.1% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.3923 (score: 0.1239) |
| **SSIM** | 0.3366 |
| **Landmark Score** | 0.5661 |
| **Pose Diff** | 6.9 deg |
| **Fused Score** | 0.2045 |
| **Aadhaar** | F, age 29 |
| **Selfie** | M, age 31 |
| **Age Gap** | 2 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4)
  2. Cosine similarity: 0.0307 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 3.1% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (11459ms total)
| Stage | Time |
|-------|------|
| load_ms | 103ms |
| enhancement_ms | 10158ms |
| clahe_ms | 46ms |
| face_processing_ms | 0ms |
| dual_path_ms | 574ms |
| similarity_ms | 577ms |
| **TOTAL** | **11459ms** |
