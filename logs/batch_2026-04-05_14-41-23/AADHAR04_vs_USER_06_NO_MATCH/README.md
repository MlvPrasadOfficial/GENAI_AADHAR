# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:48:02  
**Aadhaar:** FILES\AADHAR\AADHAR04.jpg  
**Selfie:** FILES\SELFIE\USER_06.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1176 |
| **Confidence** | 11.8% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3284 (score: 0.1363) |
| **SSIM** | 0.2167 |
| **Landmark Score** | 0.5838 |
| **Pose Diff** | 13.9 deg |
| **Fused Score** | 0.2460 |
| **Aadhaar** | F, age 31 |
| **Selfie** | M, age 45 |
| **Age Gap** | 14 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4)
  2. Cosine similarity: 0.1176 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 14yr gap → threshold relaxed by 0.090 (effective: match=0.510, uncertain=0.310)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 11.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (11979ms total)
| Stage | Time |
|-------|------|
| load_ms | 114ms |
| enhancement_ms | 10735ms |
| clahe_ms | 53ms |
| face_processing_ms | 0ms |
| dual_path_ms | 538ms |
| similarity_ms | 540ms |
| **TOTAL** | **11979ms** |
