# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:52:57  
**Aadhaar:** FILES\AADHAR\AADHAR06.pdf  
**Selfie:** FILES\SELFIE\USER_05.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1722 |
| **Confidence** | 17.2% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2867 (score: 0.1451) |
| **SSIM** | 0.2372 |
| **Landmark Score** | 0.3973 |
| **Pose Diff** | 24.6 deg |
| **Fused Score** | 0.2323 |
| **Aadhaar** | M, age 39 |
| **Selfie** | F, age 25 |
| **Age Gap** | 14 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1722 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 14yr gap → threshold relaxed by 0.090 (effective: match=0.510, uncertain=0.310)
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
| load_ms | 44ms |
| enhancement_ms | 41ms |
| clahe_ms | 10ms |
| face_processing_ms | 0ms |
| dual_path_ms | 509ms |
| similarity_ms | 510ms |
| **TOTAL** | **1114ms** |
