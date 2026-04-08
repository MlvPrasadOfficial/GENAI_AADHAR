# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:56:29  
**Aadhaar:** FILES\AADHAR\AADHAR09.pdf  
**Selfie:** FILES\SELFIE\USER_05.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0000 |
| **Confidence** | 0.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.4423 (score: 0.1149) |
| **SSIM** | 0.2708 |
| **Landmark Score** | 0.7751 |
| **Pose Diff** | 19.0 deg |
| **Fused Score** | 0.2323 |
| **Aadhaar** | M, age 31 |
| **Selfie** | F, age 25 |
| **Age Gap** | 6 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.0000 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 6yr gap → threshold relaxed by 0.010 (effective: match=0.590, uncertain=0.390)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 0.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1165ms total)
| Stage | Time |
|-------|------|
| load_ms | 32ms |
| enhancement_ms | 36ms |
| clahe_ms | 12ms |
| face_processing_ms | 0ms |
| dual_path_ms | 542ms |
| similarity_ms | 543ms |
| **TOTAL** | **1165ms** |
