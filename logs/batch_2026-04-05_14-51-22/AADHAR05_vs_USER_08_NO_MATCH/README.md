# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 15:00:27  
**Aadhaar:** FILES\AADHAR\AADHAR05.pdf  
**Selfie:** FILES\SELFIE\USER_08.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1724 |
| **Confidence** | 17.2% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2865 (score: 0.1452) |
| **SSIM** | 0.1867 |
| **Landmark Score** | 0.2826 |
| **Pose Diff** | 25.5 deg |
| **Fused Score** | 0.1987 |
| **Aadhaar** | F, age 33 |
| **Selfie** | M, age 54 |
| **Age Gap** | 21 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1724 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 21yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 17.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1114ms total)
| Stage | Time |
|-------|------|
| load_ms | 43ms |
| enhancement_ms | 32ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 514ms |
| similarity_ms | 517ms |
| **TOTAL** | **1114ms** |
