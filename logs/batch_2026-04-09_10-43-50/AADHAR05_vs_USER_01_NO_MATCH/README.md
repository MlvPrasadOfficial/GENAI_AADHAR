# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:52:22  
**Aadhaar:** FILES\AADHAR\AADHAR05.pdf  
**Selfie:** FILES\SELFIE\USER_01.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0701 |
| **Confidence** | 7.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3638 (score: 0.1293) |
| **SSIM** | 0.1803 |
| **Landmark Score** | 0.3243 |
| **Pose Diff** | 14.6 deg |
| **Fused Score** | 0.1506 |
| **Aadhaar** | F, age 33 |
| **Selfie** | M, age 30 |
| **Age Gap** | 3 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.0701 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 7.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1846ms total)
| Stage | Time |
|-------|------|
| load_ms | 172ms |
| enhancement_ms | 12ms |
| clahe_ms | 8ms |
| face_processing_ms | 528ms |
| dual_path_ms | 562ms |
| similarity_ms | 564ms |
| **TOTAL** | **1846ms** |
