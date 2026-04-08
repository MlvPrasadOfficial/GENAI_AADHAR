# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:56:30  
**Aadhaar:** FILES\AADHAR\AADHAR09.pdf  
**Selfie:** FILES\SELFIE\USER_06.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1303 |
| **Confidence** | 13.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3188 (score: 0.1383) |
| **SSIM** | 0.2312 |
| **Landmark Score** | 0.6166 |
| **Pose Diff** | 14.8 deg |
| **Fused Score** | 0.2628 |
| **Aadhaar** | M, age 31 |
| **Selfie** | M, age 45 |
| **Age Gap** | 14 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1303 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 14yr gap → threshold relaxed by 0.090 (effective: match=0.510, uncertain=0.310)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 13.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1172ms total)
| Stage | Time |
|-------|------|
| load_ms | 51ms |
| enhancement_ms | 29ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 540ms |
| similarity_ms | 543ms |
| **TOTAL** | **1172ms** |
