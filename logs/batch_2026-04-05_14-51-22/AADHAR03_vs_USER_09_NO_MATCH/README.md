# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:57:48  
**Aadhaar:** FILES\AADHAR\AADHAR03.jpg  
**Selfie:** FILES\SELFIE\USER_09.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1237 |
| **Confidence** | 12.4% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.40 |
| **L2 Distance** | 1.3239 (score: 0.1373) |
| **SSIM** | 0.3182 |
| **Landmark Score** | 0.4759 |
| **Pose Diff** | 11.0 deg |
| **Fused Score** | 0.2326 |
| **Aadhaar** | F, age 36 |
| **Selfie** | M, age 79 |
| **Age Gap** | 43 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.40, threshold=0.4)
  2. Cosine similarity: 0.1237 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 43yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 12.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1301ms total)
| Stage | Time |
|-------|------|
| load_ms | 135ms |
| enhancement_ms | 120ms |
| clahe_ms | 52ms |
| face_processing_ms | 0ms |
| dual_path_ms | 496ms |
| similarity_ms | 497ms |
| **TOTAL** | **1301ms** |
