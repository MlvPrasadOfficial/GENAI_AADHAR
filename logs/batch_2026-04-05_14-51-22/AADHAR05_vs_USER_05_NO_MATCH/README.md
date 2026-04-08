# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 15:00:18  
**Aadhaar:** FILES\AADHAR\AADHAR05.pdf  
**Selfie:** FILES\SELFIE\USER_05.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0459 |
| **Confidence** | 4.6% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3814 (score: 0.1259) |
| **SSIM** | 0.2767 |
| **Landmark Score** | 0.4260 |
| **Pose Diff** | 21.6 deg |
| **Fused Score** | 0.1720 |
| **Aadhaar** | F, age 33 |
| **Selfie** | F, age 25 |
| **Age Gap** | 8 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.0459 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 4.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1087ms total)
| Stage | Time |
|-------|------|
| load_ms | 46ms |
| enhancement_ms | 24ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 504ms |
| similarity_ms | 506ms |
| **TOTAL** | **1087ms** |
