# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:30:10  
**Aadhaar:** FILES\AADHAR\AADHAR03.jpg  
**Selfie:** FILES\SELFIE\USER_04.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0712 |
| **Confidence** | 7.1% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.3630 (score: 0.1295) |
| **SSIM** | 0.4178 |
| **Landmark Score** | 0.4067 |
| **Pose Diff** | 5.0 deg |
| **Fused Score** | 0.1956 |
| **Aadhaar** | F, age 33 |
| **Selfie** | F, age 42 |
| **Age Gap** | 9 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.0712 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 9yr gap → threshold relaxed by 0.040 (effective: match=0.560, uncertain=0.360)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 7.1% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (7436ms total)
| Stage | Time |
|-------|------|
| load_ms | 121ms |
| enhancement_ms | 6253ms |
| clahe_ms | 48ms |
| face_processing_ms | 0ms |
| dual_path_ms | 505ms |
| similarity_ms | 508ms |
| **TOTAL** | **7436ms** |
