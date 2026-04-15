# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:47:32  
**Aadhaar:** FILES\AADHAR\AADHAR001.jpg  
**Selfie:** FILES\SELFIE\USER_08.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2622 |
| **Confidence** | 26.2% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2147 (score: 0.1617) |
| **SSIM** | 0.2281 |
| **Landmark Score** | 0.6064 |
| **Pose Diff** | 33.3 deg |
| **Fused Score** | 0.3348 |
| **Aadhaar** | M, age 36 |
| **Selfie** | M, age 54 |
| **Age Gap** | 18 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=0.85, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.2622 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 18yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 26.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1803ms total)
| Stage | Time |
|-------|------|
| load_ms | 103ms |
| enhancement_ms | 104ms |
| clahe_ms | 44ms |
| face_processing_ms | 490ms |
| dual_path_ms | 530ms |
| similarity_ms | 533ms |
| **TOTAL** | **1803ms** |
