# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:55:49  
**Aadhaar:** FILES\AADHAR\AADHAR09.pdf  
**Selfie:** FILES\SELFIE\USER_01.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0753 |
| **Confidence** | 7.5% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3599 (score: 0.1300) |
| **SSIM** | 0.1392 |
| **Landmark Score** | 0.5759 |
| **Pose Diff** | 14.6 deg |
| **Fused Score** | 0.2123 |
| **Aadhaar** | M, age 39 |
| **Selfie** | M, age 30 |
| **Age Gap** | 9 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.0753 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 9yr gap → threshold relaxed by 0.040 (effective: match=0.560, uncertain=0.360)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 7.5% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1824ms total)
| Stage | Time |
|-------|------|
| load_ms | 16ms |
| enhancement_ms | 14ms |
| clahe_ms | 12ms |
| face_processing_ms | 585ms |
| dual_path_ms | 597ms |
| similarity_ms | 599ms |
| **TOTAL** | **1824ms** |
