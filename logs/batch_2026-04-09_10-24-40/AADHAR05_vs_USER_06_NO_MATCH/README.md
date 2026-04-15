# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:32:48  
**Aadhaar:** FILES\AADHAR\AADHAR05.pdf  
**Selfie:** FILES\SELFIE\USER_06.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0799 |
| **Confidence** | 8.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3566 (score: 0.1307) |
| **SSIM** | 0.2293 |
| **Landmark Score** | 0.4225 |
| **Pose Diff** | 13.7 deg |
| **Fused Score** | 0.1855 |
| **Aadhaar** | F, age 33 |
| **Selfie** | M, age 45 |
| **Age Gap** | 12 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.0799 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 12yr gap → threshold relaxed by 0.070 (effective: match=0.530, uncertain=0.330)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 8.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1010ms total)
| Stage | Time |
|-------|------|
| load_ms | 59ms |
| enhancement_ms | 26ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 457ms |
| similarity_ms | 459ms |
| **TOTAL** | **1010ms** |
