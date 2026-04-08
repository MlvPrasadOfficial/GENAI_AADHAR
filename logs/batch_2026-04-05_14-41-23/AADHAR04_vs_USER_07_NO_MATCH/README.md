# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:48:20  
**Aadhaar:** FILES\AADHAR\AADHAR04.jpg  
**Selfie:** FILES\SELFIE\USER_07.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0477 |
| **Confidence** | 4.8% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.3801 (score: 0.1262) |
| **SSIM** | 0.4445 |
| **Landmark Score** | 0.5496 |
| **Pose Diff** | 13.4 deg |
| **Fused Score** | 0.2207 |
| **Aadhaar** | F, age 29 |
| **Selfie** | M, age 38 |
| **Age Gap** | 9 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4), Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.0477 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 9yr gap → threshold relaxed by 0.040 (effective: match=0.560, uncertain=0.360)
  3. Quality flag: LOW (Aadhaar, Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 4.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (18104ms total)
| Stage | Time |
|-------|------|
| load_ms | 135ms |
| enhancement_ms | 16787ms |
| clahe_ms | 50ms |
| face_processing_ms | 0ms |
| dual_path_ms | 565ms |
| similarity_ms | 567ms |
| **TOTAL** | **18104ms** |
