# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:49:40  
**Aadhaar:** FILES\AADHAR\AADHAR02.jpg  
**Selfie:** FILES\SELFIE\USER_10.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1247 |
| **Confidence** | 12.5% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.3231 (score: 0.1374) |
| **SSIM** | 0.3695 |
| **Landmark Score** | 0.2855 |
| **Pose Diff** | 9.3 deg |
| **Fused Score** | 0.1907 |
| **Aadhaar** | M, age 33 |
| **Selfie** | M, age 21 |
| **Age Gap** | 12 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4), Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.1247 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 12yr gap → threshold relaxed by 0.070 (effective: match=0.530, uncertain=0.330)
  3. Quality flag: LOW (Aadhaar, Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 12.5% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (17127ms total)
| Stage | Time |
|-------|------|
| load_ms | 123ms |
| enhancement_ms | 15882ms |
| clahe_ms | 49ms |
| face_processing_ms | 0ms |
| dual_path_ms | 536ms |
| similarity_ms | 538ms |
| **TOTAL** | **17127ms** |
