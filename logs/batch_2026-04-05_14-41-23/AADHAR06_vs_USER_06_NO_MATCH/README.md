# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:49:38  
**Aadhaar:** FILES\AADHAR\AADHAR06.pdf  
**Selfie:** FILES\SELFIE\USER_06.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1824 |
| **Confidence** | 18.2% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2787 (score: 0.1469) |
| **SSIM** | 0.2076 |
| **Landmark Score** | 0.4227 |
| **Pose Diff** | 14.6 deg |
| **Fused Score** | 0.2415 |
| **Aadhaar** | M, age 39 |
| **Selfie** | M, age 45 |
| **Age Gap** | 6 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1824 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 6yr gap → threshold relaxed by 0.010 (effective: match=0.590, uncertain=0.390)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 18.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1060ms total)
| Stage | Time |
|-------|------|
| load_ms | 42ms |
| enhancement_ms | 33ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 488ms |
| similarity_ms | 489ms |
| **TOTAL** | **1060ms** |
