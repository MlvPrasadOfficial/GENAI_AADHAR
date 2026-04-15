# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:49:23  
**Aadhaar:** FILES\AADHAR\AADHAR02.jpg  
**Selfie:** FILES\SELFIE\USER_09.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0822 |
| **Confidence** | 8.2% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 0.40 |
| **L2 Distance** | 1.3548 (score: 0.1310) |
| **SSIM** | 0.2411 |
| **Landmark Score** | 0.5983 |
| **Pose Diff** | 7.3 deg |
| **Fused Score** | 0.2320 |
| **Aadhaar** | M, age 35 |
| **Selfie** | M, age 79 |
| **Age Gap** | 44 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4)
  2. Cosine similarity: 0.0822 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 44yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 8.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (11184ms total)
| Stage | Time |
|-------|------|
| load_ms | 114ms |
| enhancement_ms | 9895ms |
| clahe_ms | 47ms |
| face_processing_ms | 0ms |
| dual_path_ms | 562ms |
| similarity_ms | 565ms |
| **TOTAL** | **11184ms** |
