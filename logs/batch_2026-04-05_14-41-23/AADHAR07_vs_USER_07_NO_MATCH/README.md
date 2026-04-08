# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:53:25  
**Aadhaar:** FILES\AADHAR\AADHAR07.pdf  
**Selfie:** FILES\SELFIE\USER_07.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2082 |
| **Confidence** | 20.8% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.2584 (score: 0.1514) |
| **SSIM** | 0.3330 |
| **Landmark Score** | 0.3344 |
| **Pose Diff** | 13.8 deg |
| **Fused Score** | 0.2466 |
| **Aadhaar** | F, age 25 |
| **Selfie** | M, age 38 |
| **Age Gap** | 13 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.2082 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 13yr gap → threshold relaxed by 0.080 (effective: match=0.520, uncertain=0.320)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 20.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (7600ms total)
| Stage | Time |
|-------|------|
| load_ms | 62ms |
| enhancement_ms | 5944ms |
| clahe_ms | 13ms |
| face_processing_ms | 0ms |
| dual_path_ms | 789ms |
| similarity_ms | 792ms |
| **TOTAL** | **7600ms** |
