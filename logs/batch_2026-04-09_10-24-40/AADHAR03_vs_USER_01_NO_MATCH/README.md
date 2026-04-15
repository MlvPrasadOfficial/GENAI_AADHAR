# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:30:01  
**Aadhaar:** FILES\AADHAR\AADHAR03.jpg  
**Selfie:** FILES\SELFIE\USER_01.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1454 |
| **Confidence** | 14.5% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3073 (score: 0.1407) |
| **SSIM** | 0.1894 |
| **Landmark Score** | 0.4290 |
| **Pose Diff** | 18.0 deg |
| **Fused Score** | 0.2202 |
| **Aadhaar** | F, age 36 |
| **Selfie** | M, age 30 |
| **Age Gap** | 6 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1454 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 6yr gap → threshold relaxed by 0.010 (effective: match=0.590, uncertain=0.390)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 14.5% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1964ms total)
| Stage | Time |
|-------|------|
| load_ms | 100ms |
| enhancement_ms | 99ms |
| clahe_ms | 50ms |
| face_processing_ms | 560ms |
| dual_path_ms | 576ms |
| similarity_ms | 578ms |
| **TOTAL** | **1964ms** |
