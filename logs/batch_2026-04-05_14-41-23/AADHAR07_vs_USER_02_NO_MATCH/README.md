# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:53:07  
**Aadhaar:** FILES\AADHAR\AADHAR07.pdf  
**Selfie:** FILES\SELFIE\USER_02.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2092 |
| **Confidence** | 20.9% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.2576 (score: 0.1516) |
| **SSIM** | 0.2561 |
| **Landmark Score** | 0.4230 |
| **Pose Diff** | 2.9 deg |
| **Fused Score** | 0.2616 |
| **Aadhaar** | M, age 24 |
| **Selfie** | M, age 31 |
| **Age Gap** | 7 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.92, threshold=0.4)
  2. Cosine similarity: 0.2092 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 7yr gap → threshold relaxed by 0.020 (effective: match=0.580, uncertain=0.380)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 20.9% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (2120ms total)
| Stage | Time |
|-------|------|
| load_ms | 59ms |
| enhancement_ms | 43ms |
| clahe_ms | 15ms |
| face_processing_ms | 0ms |
| dual_path_ms | 1001ms |
| similarity_ms | 1002ms |
| **TOTAL** | **2120ms** |
