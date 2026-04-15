# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:52:22  
**Aadhaar:** FILES\AADHAR\AADHAR05.pdf  
**Selfie:** FILES\SELFIE\USER_02.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0925 |
| **Confidence** | 9.3% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.3472 (score: 0.1325) |
| **SSIM** | 0.2575 |
| **Landmark Score** | 0.3962 |
| **Pose Diff** | 10.2 deg |
| **Fused Score** | 0.1889 |
| **Aadhaar** | F, age 28 |
| **Selfie** | M, age 31 |
| **Age Gap** | 3 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.92, threshold=0.4)
  2. Cosine similarity: 0.0925 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 9.3% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (906ms total)
| Stage | Time |
|-------|------|
| load_ms | 43ms |
| enhancement_ms | 33ms |
| clahe_ms | 12ms |
| face_processing_ms | 0ms |
| dual_path_ms | 409ms |
| similarity_ms | 410ms |
| **TOTAL** | **906ms** |
