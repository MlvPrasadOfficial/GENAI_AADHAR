# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:27:43  
**Aadhaar:** FILES\AADHAR\AADHAR001.jpg  
**Selfie:** FILES\SELFIE\USER_05.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1110 |
| **Confidence** | 11.1% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3335 (score: 0.1353) |
| **SSIM** | 0.2917 |
| **Landmark Score** | 0.6421 |
| **Pose Diff** | 26.2 deg |
| **Fused Score** | 0.2642 |
| **Aadhaar** | M, age 36 |
| **Selfie** | F, age 25 |
| **Age Gap** | 11 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=0.85, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1110 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 11yr gap → threshold relaxed by 0.060 (effective: match=0.540, uncertain=0.340)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 11.1% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1972ms total)
| Stage | Time |
|-------|------|
| load_ms | 110ms |
| enhancement_ms | 92ms |
| clahe_ms | 46ms |
| face_processing_ms | 482ms |
| dual_path_ms | 620ms |
| similarity_ms | 622ms |
| **TOTAL** | **1972ms** |
