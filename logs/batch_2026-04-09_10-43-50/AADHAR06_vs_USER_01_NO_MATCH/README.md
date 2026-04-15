# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:52:48  
**Aadhaar:** FILES\AADHAR\AADHAR06.pdf  
**Selfie:** FILES\SELFIE\USER_01.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2274 |
| **Confidence** | 22.7% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2430 (score: 0.1550) |
| **SSIM** | 0.1418 |
| **Landmark Score** | 0.3539 |
| **Pose Diff** | 14.1 deg |
| **Fused Score** | 0.2432 |
| **Aadhaar** | M, age 38 |
| **Selfie** | M, age 30 |
| **Age Gap** | 8 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.2274 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 22.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1622ms total)
| Stage | Time |
|-------|------|
| load_ms | 28ms |
| enhancement_ms | 22ms |
| clahe_ms | 9ms |
| face_processing_ms | 544ms |
| dual_path_ms | 508ms |
| similarity_ms | 510ms |
| **TOTAL** | **1622ms** |
