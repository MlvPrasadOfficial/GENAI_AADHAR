# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:58:09  
**Aadhaar:** FILES\AADHAR\AADHAR08.pdf  
**Selfie:** FILES\SELFIE\USER_09.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1704 |
| **Confidence** | 17.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.40 |
| **L2 Distance** | 1.2881 (score: 0.1448) |
| **SSIM** | 0.3471 |
| **Landmark Score** | 0.2730 |
| **Pose Diff** | 21.1 deg |
| **Fused Score** | 0.2112 |
| **Aadhaar** | F, age 22 |
| **Selfie** | M, age 79 |
| **Age Gap** | 57 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.40, threshold=0.4)
  2. Cosine similarity: 0.1704 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 57yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 17.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (957ms total)
| Stage | Time |
|-------|------|
| load_ms | 40ms |
| enhancement_ms | 42ms |
| clahe_ms | 10ms |
| face_processing_ms | 0ms |
| dual_path_ms | 432ms |
| similarity_ms | 433ms |
| **TOTAL** | **957ms** |
