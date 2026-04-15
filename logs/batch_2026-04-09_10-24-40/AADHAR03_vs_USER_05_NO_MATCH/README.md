# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:30:11  
**Aadhaar:** FILES\AADHAR\AADHAR03.jpg  
**Selfie:** FILES\SELFIE\USER_05.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1873 |
| **Confidence** | 18.7% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2749 (score: 0.1477) |
| **SSIM** | 0.3586 |
| **Landmark Score** | 0.5349 |
| **Pose Diff** | 13.5 deg |
| **Fused Score** | 0.2874 |
| **Aadhaar** | F, age 33 |
| **Selfie** | F, age 25 |
| **Age Gap** | 8 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1873 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 18.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1287ms total)
| Stage | Time |
|-------|------|
| load_ms | 122ms |
| enhancement_ms | 110ms |
| clahe_ms | 50ms |
| face_processing_ms | 0ms |
| dual_path_ms | 501ms |
| similarity_ms | 504ms |
| **TOTAL** | **1287ms** |
