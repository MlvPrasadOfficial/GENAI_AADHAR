# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:58:47  
**Aadhaar:** FILES\AADHAR\AADHAR04.jpg  
**Selfie:** FILES\SELFIE\USER_04.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0653 |
| **Confidence** | 6.5% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.3672 (score: 0.1286) |
| **SSIM** | 0.3953 |
| **Landmark Score** | 0.4497 |
| **Pose Diff** | 11.6 deg |
| **Fused Score** | 0.2008 |
| **Aadhaar** | F, age 29 |
| **Selfie** | F, age 42 |
| **Age Gap** | 13 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4), Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.0653 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 13yr gap → threshold relaxed by 0.080 (effective: match=0.520, uncertain=0.320)
  3. Quality flag: LOW (Aadhaar, Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 6.5% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (17855ms total)
| Stage | Time |
|-------|------|
| load_ms | 127ms |
| enhancement_ms | 16557ms |
| clahe_ms | 47ms |
| face_processing_ms | 0ms |
| dual_path_ms | 562ms |
| similarity_ms | 562ms |
| **TOTAL** | **17855ms** |
