# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:33:12  
**Aadhaar:** FILES\AADHAR\AADHAR06.pdf  
**Selfie:** FILES\SELFIE\USER_04.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0000 |
| **Confidence** | 0.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.4341 (score: 0.1163) |
| **SSIM** | 0.3034 |
| **Landmark Score** | 0.2652 |
| **Pose Diff** | 12.1 deg |
| **Fused Score** | 0.1083 |
| **Aadhaar** | M, age 38 |
| **Selfie** | F, age 42 |
| **Age Gap** | 4 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.0000 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 0.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (7339ms total)
| Stage | Time |
|-------|------|
| load_ms | 40ms |
| enhancement_ms | 6328ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 480ms |
| similarity_ms | 482ms |
| **TOTAL** | **7339ms** |
