# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:54:30  
**Aadhaar:** FILES\AADHAR\AADHAR02.jpg  
**Selfie:** FILES\SELFIE\USER_01.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2388 |
| **Confidence** | 23.9% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2339 (score: 0.1571) |
| **SSIM** | 0.2065 |
| **Landmark Score** | 0.4406 |
| **Pose Diff** | 13.4 deg |
| **Fused Score** | 0.2778 |
| **Aadhaar** | M, age 33 |
| **Selfie** | M, age 30 |
| **Age Gap** | 3 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4)
  2. Cosine similarity: 0.2388 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 23.9% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (14845ms total)
| Stage | Time |
|-------|------|
| load_ms | 178ms |
| enhancement_ms | 10591ms |
| clahe_ms | 87ms |
| face_processing_ms | 1039ms |
| dual_path_ms | 1474ms |
| similarity_ms | 1477ms |
| **TOTAL** | **14845ms** |
