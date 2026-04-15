# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:28:01  
**Aadhaar:** FILES\AADHAR\AADHAR001.jpg  
**Selfie:** FILES\SELFIE\USER_10.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2456 |
| **Confidence** | 24.6% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.2283 (score: 0.1584) |
| **SSIM** | 0.4578 |
| **Landmark Score** | 0.3429 |
| **Pose Diff** | 10.1 deg |
| **Fused Score** | 0.2825 |
| **Aadhaar** | M, age 38 |
| **Selfie** | M, age 21 |
| **Age Gap** | 17 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.2456 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 17yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 24.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (7346ms total)
| Stage | Time |
|-------|------|
| load_ms | 116ms |
| enhancement_ms | 5613ms |
| clahe_ms | 44ms |
| face_processing_ms | 491ms |
| dual_path_ms | 540ms |
| similarity_ms | 543ms |
| **TOTAL** | **7346ms** |
