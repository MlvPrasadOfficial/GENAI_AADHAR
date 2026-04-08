# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 15:02:31  
**Aadhaar:** FILES\AADHAR\AADHAR08.pdf  
**Selfie:** FILES\SELFIE\USER_01.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1281 |
| **Confidence** | 12.8% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3206 (score: 0.1380) |
| **SSIM** | 0.2886 |
| **Landmark Score** | 0.2898 |
| **Pose Diff** | 5.9 deg |
| **Fused Score** | 0.1855 |
| **Aadhaar** | F, age 21 |
| **Selfie** | M, age 30 |
| **Age Gap** | 9 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1281 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 9yr gap → threshold relaxed by 0.040 (effective: match=0.560, uncertain=0.360)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 12.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (2032ms total)
| Stage | Time |
|-------|------|
| load_ms | 21ms |
| enhancement_ms | 22ms |
| clahe_ms | 12ms |
| face_processing_ms | 552ms |
| dual_path_ms | 711ms |
| similarity_ms | 713ms |
| **TOTAL** | **2032ms** |
