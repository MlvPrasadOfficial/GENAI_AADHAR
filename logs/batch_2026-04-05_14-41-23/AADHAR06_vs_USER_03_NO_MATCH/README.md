# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:49:30  
**Aadhaar:** FILES\AADHAR\AADHAR06.pdf  
**Selfie:** FILES\SELFIE\USER_03.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0960 |
| **Confidence** | 9.6% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 1.3446 (score: 0.1331) |
| **SSIM** | 0.1713 |
| **Landmark Score** | 0.5934 |
| **Pose Diff** | 9.6 deg |
| **Fused Score** | 0.2316 |
| **Aadhaar** | M, age 38 |
| **Selfie** | F, age 28 |
| **Age Gap** | 10 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.67, threshold=0.4)
  2. Cosine similarity: 0.0960 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 10yr gap → threshold relaxed by 0.050 (effective: match=0.550, uncertain=0.350)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 9.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1042ms total)
| Stage | Time |
|-------|------|
| load_ms | 43ms |
| enhancement_ms | 34ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 477ms |
| similarity_ms | 479ms |
| **TOTAL** | **1042ms** |
