# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:52:30  
**Aadhaar:** FILES\AADHAR\AADHAR05.pdf  
**Selfie:** FILES\SELFIE\USER_04.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0364 |
| **Confidence** | 3.6% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.3882 (score: 0.1246) |
| **SSIM** | 0.3708 |
| **Landmark Score** | 0.2751 |
| **Pose Diff** | 9.6 deg |
| **Fused Score** | 0.1384 |
| **Aadhaar** | F, age 28 |
| **Selfie** | F, age 42 |
| **Age Gap** | 14 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.0364 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 14yr gap → threshold relaxed by 0.090 (effective: match=0.510, uncertain=0.310)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 3.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (7527ms total)
| Stage | Time |
|-------|------|
| load_ms | 39ms |
| enhancement_ms | 6462ms |
| clahe_ms | 11ms |
| face_processing_ms | 0ms |
| dual_path_ms | 506ms |
| similarity_ms | 509ms |
| **TOTAL** | **7527ms** |
