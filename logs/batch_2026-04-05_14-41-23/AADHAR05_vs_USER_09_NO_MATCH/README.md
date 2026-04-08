# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:49:20  
**Aadhaar:** FILES\AADHAR\AADHAR05.pdf  
**Selfie:** FILES\SELFIE\USER_09.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0780 |
| **Confidence** | 7.8% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.40 |
| **L2 Distance** | 1.3579 (score: 0.1304) |
| **SSIM** | 0.2672 |
| **Landmark Score** | 0.3195 |
| **Pose Diff** | 8.2 deg |
| **Fused Score** | 0.1625 |
| **Aadhaar** | F, age 28 |
| **Selfie** | M, age 79 |
| **Age Gap** | 51 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.40, threshold=0.4)
  2. Cosine similarity: 0.0780 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 51yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 7.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1099ms total)
| Stage | Time |
|-------|------|
| load_ms | 39ms |
| enhancement_ms | 51ms |
| clahe_ms | 13ms |
| face_processing_ms | 0ms |
| dual_path_ms | 496ms |
| similarity_ms | 499ms |
| **TOTAL** | **1099ms** |
