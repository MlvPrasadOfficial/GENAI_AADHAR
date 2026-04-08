# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:53:05  
**Aadhaar:** FILES\AADHAR\AADHAR07.pdf  
**Selfie:** FILES\SELFIE\USER_01.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0551 |
| **Confidence** | 5.5% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3747 (score: 0.1272) |
| **SSIM** | 0.1951 |
| **Landmark Score** | 0.3235 |
| **Pose Diff** | 8.0 deg |
| **Fused Score** | 0.1434 |
| **Aadhaar** | M, age 24 |
| **Selfie** | M, age 30 |
| **Age Gap** | 6 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.0551 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 6yr gap → threshold relaxed by 0.010 (effective: match=0.590, uncertain=0.390)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 5.5% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (3775ms total)
| Stage | Time |
|-------|------|
| load_ms | 52ms |
| enhancement_ms | 26ms |
| clahe_ms | 15ms |
| face_processing_ms | 988ms |
| dual_path_ms | 1346ms |
| similarity_ms | 1349ms |
| **TOTAL** | **3775ms** |
