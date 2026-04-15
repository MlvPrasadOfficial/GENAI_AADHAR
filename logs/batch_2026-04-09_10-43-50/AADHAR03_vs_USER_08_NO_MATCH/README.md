# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:50:00  
**Aadhaar:** FILES\AADHAR\AADHAR03.jpg  
**Selfie:** FILES\SELFIE\USER_08.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1968 |
| **Confidence** | 19.7% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2674 (score: 0.1494) |
| **SSIM** | 0.2392 |
| **Landmark Score** | 0.3880 |
| **Pose Diff** | 19.1 deg |
| **Fused Score** | 0.2441 |
| **Aadhaar** | F, age 36 |
| **Selfie** | M, age 54 |
| **Age Gap** | 18 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1968 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 18yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 19.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1170ms total)
| Stage | Time |
|-------|------|
| load_ms | 108ms |
| enhancement_ms | 120ms |
| clahe_ms | 51ms |
| face_processing_ms | 0ms |
| dual_path_ms | 444ms |
| similarity_ms | 445ms |
| **TOTAL** | **1170ms** |
