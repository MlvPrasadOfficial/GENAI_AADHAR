# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:56:44  
**Aadhaar:** FILES\AADHAR\AADHAR07.pdf  
**Selfie:** FILES\SELFIE\USER_08.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2035 |
| **Confidence** | 20.3% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2622 (score: 0.1506) |
| **SSIM** | 0.1983 |
| **Landmark Score** | 0.2741 |
| **Pose Diff** | 28.5 deg |
| **Fused Score** | 0.2153 |
| **Aadhaar** | F, age 25 |
| **Selfie** | M, age 54 |
| **Age Gap** | 29 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.2035 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 29yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 20.3% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (872ms total)
| Stage | Time |
|-------|------|
| load_ms | 57ms |
| enhancement_ms | 59ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 373ms |
| similarity_ms | 374ms |
| **TOTAL** | **872ms** |
