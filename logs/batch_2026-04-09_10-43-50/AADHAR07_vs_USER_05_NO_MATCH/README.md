# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:56:36  
**Aadhaar:** FILES\AADHAR\AADHAR07.pdf  
**Selfie:** FILES\SELFIE\USER_05.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2239 |
| **Confidence** | 22.4% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2459 (score: 0.1543) |
| **SSIM** | 0.2745 |
| **Landmark Score** | 0.4373 |
| **Pose Diff** | 22.4 deg |
| **Fused Score** | 0.2753 |
| **Aadhaar** | F, age 25 |
| **Selfie** | F, age 25 |
| **Age Gap** | 0 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.2239 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 22.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (989ms total)
| Stage | Time |
|-------|------|
| load_ms | 20ms |
| enhancement_ms | 30ms |
| clahe_ms | 11ms |
| face_processing_ms | 0ms |
| dual_path_ms | 463ms |
| similarity_ms | 464ms |
| **TOTAL** | **989ms** |
