# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:30:12  
**Aadhaar:** FILES\AADHAR\AADHAR03.jpg  
**Selfie:** FILES\SELFIE\USER_06.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1859 |
| **Confidence** | 18.6% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2760 (score: 0.1475) |
| **SSIM** | 0.2687 |
| **Landmark Score** | 0.6214 |
| **Pose Diff** | 14.7 deg |
| **Fused Score** | 0.2992 |
| **Aadhaar** | F, age 36 |
| **Selfie** | M, age 45 |
| **Age Gap** | 9 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1859 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 9yr gap → threshold relaxed by 0.040 (effective: match=0.560, uncertain=0.360)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 18.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1337ms total)
| Stage | Time |
|-------|------|
| load_ms | 134ms |
| enhancement_ms | 110ms |
| clahe_ms | 51ms |
| face_processing_ms | 0ms |
| dual_path_ms | 520ms |
| similarity_ms | 522ms |
| **TOTAL** | **1337ms** |
