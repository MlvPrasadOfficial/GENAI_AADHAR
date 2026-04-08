# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:55:32  
**Aadhaar:** FILES\AADHAR\AADHAR08.pdf  
**Selfie:** FILES\SELFIE\USER_07.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1710 |
| **Confidence** | 17.1% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.2876 (score: 0.1449) |
| **SSIM** | 0.4699 |
| **Landmark Score** | 0.3018 |
| **Pose Diff** | 25.2 deg |
| **Fused Score** | 0.2310 |
| **Aadhaar** | F, age 22 |
| **Selfie** | M, age 38 |
| **Age Gap** | 16 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.1710 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 16yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 17.1% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (15845ms total)
| Stage | Time |
|-------|------|
| load_ms | 53ms |
| enhancement_ms | 14757ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 512ms |
| similarity_ms | 515ms |
| **TOTAL** | **15845ms** |
