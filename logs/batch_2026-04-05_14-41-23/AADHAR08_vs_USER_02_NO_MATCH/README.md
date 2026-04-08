# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:54:04  
**Aadhaar:** FILES\AADHAR\AADHAR08.pdf  
**Selfie:** FILES\SELFIE\USER_02.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1939 |
| **Confidence** | 19.4% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.2697 (score: 0.1489) |
| **SSIM** | 0.3148 |
| **Landmark Score** | 0.3714 |
| **Pose Diff** | 13.8 deg |
| **Fused Score** | 0.2459 |
| **Aadhaar** | F, age 21 |
| **Selfie** | M, age 31 |
| **Age Gap** | 10 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.92, threshold=0.4)
  2. Cosine similarity: 0.1939 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 10yr gap → threshold relaxed by 0.050 (effective: match=0.550, uncertain=0.350)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 19.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1225ms total)
| Stage | Time |
|-------|------|
| load_ms | 41ms |
| enhancement_ms | 35ms |
| clahe_ms | 10ms |
| face_processing_ms | 0ms |
| dual_path_ms | 569ms |
| similarity_ms | 570ms |
| **TOTAL** | **1225ms** |
