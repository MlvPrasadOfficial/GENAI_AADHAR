# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:58:09  
**Aadhaar:** FILES\AADHAR\AADHAR08.pdf  
**Selfie:** FILES\SELFIE\USER_08.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1804 |
| **Confidence** | 18.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2803 (score: 0.1465) |
| **SSIM** | 0.2580 |
| **Landmark Score** | 0.2587 |
| **Pose Diff** | 40.2 deg |
| **Fused Score** | 0.2043 |
| **Aadhaar** | F, age 21 |
| **Selfie** | M, age 54 |
| **Age Gap** | 33 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1804 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 33yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 18.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (874ms total)
| Stage | Time |
|-------|------|
| load_ms | 34ms |
| enhancement_ms | 30ms |
| clahe_ms | 12ms |
| face_processing_ms | 0ms |
| dual_path_ms | 399ms |
| similarity_ms | 400ms |
| **TOTAL** | **874ms** |
