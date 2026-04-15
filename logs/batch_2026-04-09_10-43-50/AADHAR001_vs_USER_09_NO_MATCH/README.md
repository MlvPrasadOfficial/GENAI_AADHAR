# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:47:33  
**Aadhaar:** FILES\AADHAR\AADHAR001.jpg  
**Selfie:** FILES\SELFIE\USER_09.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1618 |
| **Confidence** | 16.2% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 0.40 |
| **L2 Distance** | 1.2948 (score: 0.1434) |
| **SSIM** | 0.2798 |
| **Landmark Score** | 0.5672 |
| **Pose Diff** | 16.3 deg |
| **Fused Score** | 0.2731 |
| **Aadhaar** | M, age 36 |
| **Selfie** | M, age 79 |
| **Age Gap** | 43 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=0.85, Selfie=0.40, threshold=0.4)
  2. Cosine similarity: 0.1618 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 43yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 16.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1795ms total)
| Stage | Time |
|-------|------|
| load_ms | 117ms |
| enhancement_ms | 99ms |
| clahe_ms | 44ms |
| face_processing_ms | 548ms |
| dual_path_ms | 492ms |
| similarity_ms | 495ms |
| **TOTAL** | **1795ms** |
