# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:57:10  
**Aadhaar:** FILES\AADHAR\AADHAR08.pdf  
**Selfie:** FILES\SELFIE\USER_03.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2529 |
| **Confidence** | 25.3% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 1.2224 (score: 0.1598) |
| **SSIM** | 0.3077 |
| **Landmark Score** | 0.5398 |
| **Pose Diff** | 13.5 deg |
| **Fused Score** | 0.3208 |
| **Aadhaar** | F, age 21 |
| **Selfie** | F, age 28 |
| **Age Gap** | 7 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.67, threshold=0.4)
  2. Cosine similarity: 0.2529 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 7yr gap → threshold relaxed by 0.020 (effective: match=0.580, uncertain=0.380)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 25.3% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1032ms total)
| Stage | Time |
|-------|------|
| load_ms | 58ms |
| enhancement_ms | 49ms |
| clahe_ms | 14ms |
| face_processing_ms | 0ms |
| dual_path_ms | 455ms |
| similarity_ms | 456ms |
| **TOTAL** | **1032ms** |
