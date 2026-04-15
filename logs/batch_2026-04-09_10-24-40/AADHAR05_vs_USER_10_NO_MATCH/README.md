# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:33:03  
**Aadhaar:** FILES\AADHAR\AADHAR05.pdf  
**Selfie:** FILES\SELFIE\USER_10.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0566 |
| **Confidence** | 5.7% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.3736 (score: 0.1274) |
| **SSIM** | 0.3415 |
| **Landmark Score** | 0.2060 |
| **Pose Diff** | 10.3 deg |
| **Fused Score** | 0.1295 |
| **Aadhaar** | F, age 33 |
| **Selfie** | M, age 21 |
| **Age Gap** | 12 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.0566 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 12yr gap → threshold relaxed by 0.070 (effective: match=0.530, uncertain=0.330)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 5.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (7438ms total)
| Stage | Time |
|-------|------|
| load_ms | 33ms |
| enhancement_ms | 6401ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 497ms |
| similarity_ms | 499ms |
| **TOTAL** | **7438ms** |
