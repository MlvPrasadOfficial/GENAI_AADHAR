# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:56:36  
**Aadhaar:** FILES\AADHAR\AADHAR07.pdf  
**Selfie:** FILES\SELFIE\USER_04.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0646 |
| **Confidence** | 6.5% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.3678 (score: 0.1285) |
| **SSIM** | 0.3131 |
| **Landmark Score** | 0.2874 |
| **Pose Diff** | 15.0 deg |
| **Fused Score** | 0.1515 |
| **Aadhaar** | F, age 25 |
| **Selfie** | F, age 42 |
| **Age Gap** | 17 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.0646 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 17yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 6.5% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (6805ms total)
| Stage | Time |
|-------|------|
| load_ms | 50ms |
| enhancement_ms | 5726ms |
| clahe_ms | 13ms |
| face_processing_ms | 0ms |
| dual_path_ms | 508ms |
| similarity_ms | 509ms |
| **TOTAL** | **6805ms** |
