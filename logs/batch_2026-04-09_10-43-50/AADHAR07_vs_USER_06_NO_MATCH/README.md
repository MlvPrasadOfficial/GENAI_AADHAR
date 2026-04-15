# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:56:37  
**Aadhaar:** FILES\AADHAR\AADHAR07.pdf  
**Selfie:** FILES\SELFIE\USER_06.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2841 |
| **Confidence** | 28.4% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.1966 (score: 0.1661) |
| **SSIM** | 0.2291 |
| **Landmark Score** | 0.4122 |
| **Pose Diff** | 6.2 deg |
| **Fused Score** | 0.2988 |
| **Aadhaar** | F, age 25 |
| **Selfie** | M, age 45 |
| **Age Gap** | 20 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.2841 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 20yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 28.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1075ms total)
| Stage | Time |
|-------|------|
| load_ms | 54ms |
| enhancement_ms | 24ms |
| clahe_ms | 12ms |
| face_processing_ms | 0ms |
| dual_path_ms | 491ms |
| similarity_ms | 494ms |
| **TOTAL** | **1075ms** |
