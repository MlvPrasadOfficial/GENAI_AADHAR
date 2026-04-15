# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:51:10  
**Aadhaar:** FILES\AADHAR\AADHAR04.jpg  
**Selfie:** FILES\SELFIE\USER_05.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1058 |
| **Confidence** | 10.6% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3373 (score: 0.1345) |
| **SSIM** | 0.3286 |
| **Landmark Score** | 0.6548 |
| **Pose Diff** | 14.2 deg |
| **Fused Score** | 0.2682 |
| **Aadhaar** | F, age 29 |
| **Selfie** | F, age 25 |
| **Age Gap** | 4 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4)
  2. Cosine similarity: 0.1058 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 10.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (11860ms total)
| Stage | Time |
|-------|------|
| load_ms | 131ms |
| enhancement_ms | 10667ms |
| clahe_ms | 56ms |
| face_processing_ms | 0ms |
| dual_path_ms | 503ms |
| similarity_ms | 504ms |
| **TOTAL** | **11860ms** |
