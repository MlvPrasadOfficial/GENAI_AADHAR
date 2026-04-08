# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:44:09  
**Aadhaar:** FILES\AADHAR\AADHAR02.jpg  
**Selfie:** FILES\SELFIE\USER_02.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2564 |
| **Confidence** | 25.6% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.2195 (score: 0.1605) |
| **SSIM** | 0.2501 |
| **Landmark Score** | 0.5933 |
| **Pose Diff** | 8.6 deg |
| **Fused Score** | 0.3304 |
| **Aadhaar** | M, age 35 |
| **Selfie** | M, age 31 |
| **Age Gap** | 4 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4)
  2. Cosine similarity: 0.2564 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 25.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (18432ms total)
| Stage | Time |
|-------|------|
| load_ms | 102ms |
| enhancement_ms | 16685ms |
| clahe_ms | 88ms |
| face_processing_ms | 0ms |
| dual_path_ms | 777ms |
| similarity_ms | 779ms |
| **TOTAL** | **18432ms** |
