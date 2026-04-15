# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:32:37  
**Aadhaar:** FILES\AADHAR\AADHAR04.jpg  
**Selfie:** FILES\SELFIE\USER_10.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0237 |
| **Confidence** | 2.4% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.3974 (score: 0.1229) |
| **SSIM** | 0.4011 |
| **Landmark Score** | 0.3191 |
| **Pose Diff** | 4.1 deg |
| **Fused Score** | 0.1452 |
| **Aadhaar** | F, age 29 |
| **Selfie** | M, age 21 |
| **Age Gap** | 8 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4), Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.0237 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: LOW (Aadhaar, Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 2.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (17660ms total)
| Stage | Time |
|-------|------|
| load_ms | 132ms |
| enhancement_ms | 16434ms |
| clahe_ms | 48ms |
| face_processing_ms | 0ms |
| dual_path_ms | 522ms |
| similarity_ms | 524ms |
| **TOTAL** | **17660ms** |
