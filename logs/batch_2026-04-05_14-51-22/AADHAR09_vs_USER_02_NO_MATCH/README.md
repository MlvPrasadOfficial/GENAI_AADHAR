# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 15:03:43  
**Aadhaar:** FILES\AADHAR\AADHAR09.pdf  
**Selfie:** FILES\SELFIE\USER_02.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1469 |
| **Confidence** | 14.7% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.3062 (score: 0.1410) |
| **SSIM** | 0.2074 |
| **Landmark Score** | 0.7729 |
| **Pose Diff** | 8.1 deg |
| **Fused Score** | 0.3089 |
| **Aadhaar** | M, age 39 |
| **Selfie** | M, age 31 |
| **Age Gap** | 8 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.92, threshold=0.4)
  2. Cosine similarity: 0.1469 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 14.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1004ms total)
| Stage | Time |
|-------|------|
| load_ms | 41ms |
| enhancement_ms | 22ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 466ms |
| similarity_ms | 466ms |
| **TOTAL** | **1004ms** |
