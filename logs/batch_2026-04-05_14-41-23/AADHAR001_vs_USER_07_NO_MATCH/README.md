# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:43:13  
**Aadhaar:** FILES\AADHAR\AADHAR001.jpg  
**Selfie:** FILES\SELFIE\USER_07.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2143 |
| **Confidence** | 21.4% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.2535 (score: 0.1525) |
| **SSIM** | 0.3849 |
| **Landmark Score** | 0.6209 |
| **Pose Diff** | 18.9 deg |
| **Fused Score** | 0.3268 |
| **Aadhaar** | M, age 36 |
| **Selfie** | M, age 38 |
| **Age Gap** | 2 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.2143 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 21.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (9238ms total)
| Stage | Time |
|-------|------|
| load_ms | 252ms |
| enhancement_ms | 6316ms |
| clahe_ms | 94ms |
| face_processing_ms | 888ms |
| dual_path_ms | 841ms |
| similarity_ms | 846ms |
| **TOTAL** | **9238ms** |
