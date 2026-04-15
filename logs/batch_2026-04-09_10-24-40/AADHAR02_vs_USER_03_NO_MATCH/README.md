# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:28:31  
**Aadhaar:** FILES\AADHAR\AADHAR02.jpg  
**Selfie:** FILES\SELFIE\USER_03.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0021 |
| **Confidence** | 0.2% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 1.4127 (score: 0.1201) |
| **SSIM** | 0.2456 |
| **Landmark Score** | 0.6167 |
| **Pose Diff** | 6.9 deg |
| **Fused Score** | 0.1919 |
| **Aadhaar** | M, age 33 |
| **Selfie** | F, age 28 |
| **Age Gap** | 5 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4)
  2. Cosine similarity: 0.0021 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 0.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (9866ms total)
| Stage | Time |
|-------|------|
| load_ms | 127ms |
| enhancement_ms | 8839ms |
| clahe_ms | 47ms |
| face_processing_ms | 0ms |
| dual_path_ms | 426ms |
| similarity_ms | 427ms |
| **TOTAL** | **9866ms** |
