# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:53:27  
**Aadhaar:** FILES\AADHAR\AADHAR07.pdf  
**Selfie:** FILES\SELFIE\USER_09.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1893 |
| **Confidence** | 18.9% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.40 |
| **L2 Distance** | 1.2733 (score: 0.1481) |
| **SSIM** | 0.2141 |
| **Landmark Score** | 0.3157 |
| **Pose Diff** | 10.9 deg |
| **Fused Score** | 0.2193 |
| **Aadhaar** | F, age 25 |
| **Selfie** | M, age 79 |
| **Age Gap** | 54 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.40, threshold=0.4)
  2. Cosine similarity: 0.1893 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 54yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 18.9% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1904ms total)
| Stage | Time |
|-------|------|
| load_ms | 66ms |
| enhancement_ms | 43ms |
| clahe_ms | 11ms |
| face_processing_ms | 0ms |
| dual_path_ms | 891ms |
| similarity_ms | 892ms |
| **TOTAL** | **1904ms** |
