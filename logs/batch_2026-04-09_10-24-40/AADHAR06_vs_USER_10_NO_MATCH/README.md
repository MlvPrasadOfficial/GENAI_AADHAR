# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:43:33  
**Aadhaar:** FILES\AADHAR\AADHAR06.pdf  
**Selfie:** FILES\SELFIE\USER_10.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2322 |
| **Confidence** | 23.2% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.2392 (score: 0.1559) |
| **SSIM** | 0.3185 |
| **Landmark Score** | 0.2036 |
| **Pose Diff** | 12.4 deg |
| **Fused Score** | 0.2260 |
| **Aadhaar** | M, age 38 |
| **Selfie** | M, age 21 |
| **Age Gap** | 17 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.2322 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 17yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 23.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (7639ms total)
| Stage | Time |
|-------|------|
| load_ms | 31ms |
| enhancement_ms | 6627ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 486ms |
| similarity_ms | 487ms |
| **TOTAL** | **7639ms** |
