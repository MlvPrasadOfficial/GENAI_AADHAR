# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:53:41  
**Aadhaar:** FILES\AADHAR\AADHAR001.jpg  
**Selfie:** FILES\SELFIE\USER_04.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0469 |
| **Confidence** | 4.7% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.3806 (score: 0.1261) |
| **SSIM** | 0.3580 |
| **Landmark Score** | 0.5621 |
| **Pose Diff** | 20.5 deg |
| **Fused Score** | 0.2147 |
| **Aadhaar** | M, age 38 |
| **Selfie** | F, age 42 |
| **Age Gap** | 4 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.0469 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 4.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (10014ms total)
| Stage | Time |
|-------|------|
| load_ms | 138ms |
| enhancement_ms | 6524ms |
| clahe_ms | 95ms |
| face_processing_ms | 939ms |
| dual_path_ms | 1158ms |
| similarity_ms | 1161ms |
| **TOTAL** | **10014ms** |
