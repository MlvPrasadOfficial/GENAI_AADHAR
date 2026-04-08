# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:58:07  
**Aadhaar:** FILES\AADHAR\AADHAR04.jpg  
**Selfie:** FILES\SELFIE\USER_01.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0484 |
| **Confidence** | 4.8% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3796 (score: 0.1263) |
| **SSIM** | 0.1998 |
| **Landmark Score** | 0.4881 |
| **Pose Diff** | 16.7 deg |
| **Fused Score** | 0.1813 |
| **Aadhaar** | F, age 29 |
| **Selfie** | M, age 30 |
| **Age Gap** | 1 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4)
  2. Cosine similarity: 0.0484 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 4.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (11972ms total)
| Stage | Time |
|-------|------|
| load_ms | 97ms |
| enhancement_ms | 10252ms |
| clahe_ms | 48ms |
| face_processing_ms | 487ms |
| dual_path_ms | 544ms |
| similarity_ms | 545ms |
| **TOTAL** | **11972ms** |
