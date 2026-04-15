# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:58:52  
**Aadhaar:** FILES\AADHAR\AADHAR09.pdf  
**Selfie:** FILES\SELFIE\USER_07.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0052 |
| **Confidence** | 0.5% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.4105 (score: 0.1205) |
| **SSIM** | 0.3442 |
| **Landmark Score** | 0.6707 |
| **Pose Diff** | 15.3 deg |
| **Fused Score** | 0.2170 |
| **Aadhaar** | M, age 31 |
| **Selfie** | M, age 38 |
| **Age Gap** | 7 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.0052 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 7yr gap → threshold relaxed by 0.020 (effective: match=0.580, uncertain=0.380)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 0.5% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (6759ms total)
| Stage | Time |
|-------|------|
| load_ms | 50ms |
| enhancement_ms | 5666ms |
| clahe_ms | 13ms |
| face_processing_ms | 0ms |
| dual_path_ms | 514ms |
| similarity_ms | 517ms |
| **TOTAL** | **6759ms** |
