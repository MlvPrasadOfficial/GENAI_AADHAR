# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:49:02  
**Aadhaar:** FILES\AADHAR\AADHAR02.jpg  
**Selfie:** FILES\SELFIE\USER_07.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1027 |
| **Confidence** | 10.3% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.3397 (score: 0.1341) |
| **SSIM** | 0.3573 |
| **Landmark Score** | 0.4911 |
| **Pose Diff** | 12.7 deg |
| **Fused Score** | 0.2284 |
| **Aadhaar** | M, age 35 |
| **Selfie** | M, age 38 |
| **Age Gap** | 3 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4), Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.1027 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar, Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 10.3% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (16427ms total)
| Stage | Time |
|-------|------|
| load_ms | 111ms |
| enhancement_ms | 15320ms |
| clahe_ms | 46ms |
| face_processing_ms | 0ms |
| dual_path_ms | 474ms |
| similarity_ms | 476ms |
| **TOTAL** | **16427ms** |
