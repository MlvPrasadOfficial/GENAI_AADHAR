# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:56:47  
**Aadhaar:** FILES\AADHAR\AADHAR09.pdf  
**Selfie:** FILES\SELFIE\USER_08.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1670 |
| **Confidence** | 16.7% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2907 (score: 0.1443) |
| **SSIM** | 0.1909 |
| **Landmark Score** | 0.5128 |
| **Pose Diff** | 25.2 deg |
| **Fused Score** | 0.2536 |
| **Aadhaar** | M, age 31 |
| **Selfie** | M, age 54 |
| **Age Gap** | 23 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1670 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 23yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 16.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1366ms total)
| Stage | Time |
|-------|------|
| load_ms | 42ms |
| enhancement_ms | 38ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 638ms |
| similarity_ms | 640ms |
| **TOTAL** | **1366ms** |
