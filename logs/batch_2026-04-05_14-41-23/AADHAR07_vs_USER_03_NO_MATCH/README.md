# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:53:08  
**Aadhaar:** FILES\AADHAR\AADHAR07.pdf  
**Selfie:** FILES\SELFIE\USER_03.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1662 |
| **Confidence** | 16.6% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 1.2913 (score: 0.1441) |
| **SSIM** | 0.2482 |
| **Landmark Score** | 0.6098 |
| **Pose Diff** | 2.0 deg |
| **Fused Score** | 0.2831 |
| **Aadhaar** | F, age 25 |
| **Selfie** | F, age 28 |
| **Age Gap** | 3 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.67, threshold=0.4)
  2. Cosine similarity: 0.1662 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 16.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (2421ms total)
| Stage | Time |
|-------|------|
| load_ms | 72ms |
| enhancement_ms | 45ms |
| clahe_ms | 12ms |
| face_processing_ms | 0ms |
| dual_path_ms | 1144ms |
| similarity_ms | 1147ms |
| **TOTAL** | **2421ms** |
