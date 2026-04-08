# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 15:03:41  
**Aadhaar:** FILES\AADHAR\AADHAR08.pdf  
**Selfie:** FILES\SELFIE\USER_10.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2137 |
| **Confidence** | 21.4% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.2540 (score: 0.1524) |
| **SSIM** | 0.4504 |
| **Landmark Score** | 0.2170 |
| **Pose Diff** | 16.8 deg |
| **Fused Score** | 0.2321 |
| **Aadhaar** | F, age 22 |
| **Selfie** | M, age 21 |
| **Age Gap** | 1 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.2137 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 21.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (6467ms total)
| Stage | Time |
|-------|------|
| load_ms | 51ms |
| enhancement_ms | 5424ms |
| clahe_ms | 11ms |
| face_processing_ms | 0ms |
| dual_path_ms | 489ms |
| similarity_ms | 492ms |
| **TOTAL** | **6467ms** |
