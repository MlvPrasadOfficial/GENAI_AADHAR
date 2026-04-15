# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:28:46  
**Aadhaar:** FILES\AADHAR\AADHAR02.jpg  
**Selfie:** FILES\SELFIE\USER_04.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0388 |
| **Confidence** | 3.9% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.3865 (score: 0.1250) |
| **SSIM** | 0.3511 |
| **Landmark Score** | 0.3974 |
| **Pose Diff** | 10.3 deg |
| **Fused Score** | 0.1683 |
| **Aadhaar** | M, age 33 |
| **Selfie** | F, age 42 |
| **Age Gap** | 9 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4), Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.0388 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 9yr gap → threshold relaxed by 0.040 (effective: match=0.560, uncertain=0.360)
  3. Quality flag: LOW (Aadhaar, Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 3.9% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (15600ms total)
| Stage | Time |
|-------|------|
| load_ms | 117ms |
| enhancement_ms | 14526ms |
| clahe_ms | 45ms |
| face_processing_ms | 0ms |
| dual_path_ms | 454ms |
| similarity_ms | 457ms |
| **TOTAL** | **15600ms** |
