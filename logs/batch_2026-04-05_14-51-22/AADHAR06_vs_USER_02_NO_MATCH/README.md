# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 15:00:37  
**Aadhaar:** FILES\AADHAR\AADHAR06.pdf  
**Selfie:** FILES\SELFIE\USER_02.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.3732 |
| **Confidence** | 27.3% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.1197 (score: 0.1865) |
| **SSIM** | 0.2199 |
| **Landmark Score** | 0.4095 |
| **Pose Diff** | 12.5 deg |
| **Fused Score** | 0.3483 |
| **Aadhaar** | M, age 39 |
| **Selfie** | M, age 31 |
| **Age Gap** | 8 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.92, threshold=0.4)
  2. Cosine similarity: 0.3732 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 27.3% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1102ms total)
| Stage | Time |
|-------|------|
| load_ms | 39ms |
| enhancement_ms | 28ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 512ms |
| similarity_ms | 515ms |
| **TOTAL** | **1102ms** |
