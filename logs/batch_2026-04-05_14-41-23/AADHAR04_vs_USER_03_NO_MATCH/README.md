# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:47:22  
**Aadhaar:** FILES\AADHAR\AADHAR04.jpg  
**Selfie:** FILES\SELFIE\USER_03.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1176 |
| **Confidence** | 11.8% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 1.3285 (score: 0.1363) |
| **SSIM** | 0.2862 |
| **Landmark Score** | 0.6236 |
| **Pose Diff** | 10.2 deg |
| **Fused Score** | 0.2628 |
| **Aadhaar** | F, age 29 |
| **Selfie** | F, age 28 |
| **Age Gap** | 1 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4)
  2. Cosine similarity: 0.1176 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 11.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (11918ms total)
| Stage | Time |
|-------|------|
| load_ms | 200ms |
| enhancement_ms | 10624ms |
| clahe_ms | 50ms |
| face_processing_ms | 0ms |
| dual_path_ms | 522ms |
| similarity_ms | 523ms |
| **TOTAL** | **11918ms** |
