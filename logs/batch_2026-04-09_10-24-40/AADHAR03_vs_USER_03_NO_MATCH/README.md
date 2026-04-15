# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:30:03  
**Aadhaar:** FILES\AADHAR\AADHAR03.jpg  
**Selfie:** FILES\SELFIE\USER_03.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1512 |
| **Confidence** | 15.1% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 1.3029 (score: 0.1417) |
| **SSIM** | 0.2462 |
| **Landmark Score** | 0.6365 |
| **Pose Diff** | 9.7 deg |
| **Fused Score** | 0.2811 |
| **Aadhaar** | F, age 36 |
| **Selfie** | F, age 28 |
| **Age Gap** | 8 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.67, threshold=0.4)
  2. Cosine similarity: 0.1512 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 15.1% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1367ms total)
| Stage | Time |
|-------|------|
| load_ms | 112ms |
| enhancement_ms | 109ms |
| clahe_ms | 49ms |
| face_processing_ms | 0ms |
| dual_path_ms | 547ms |
| similarity_ms | 550ms |
| **TOTAL** | **1367ms** |
