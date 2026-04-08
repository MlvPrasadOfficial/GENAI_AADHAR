# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:54:18  
**Aadhaar:** FILES\AADHAR\AADHAR08.pdf  
**Selfie:** FILES\SELFIE\USER_04.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1620 |
| **Confidence** | 16.2% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.2946 (score: 0.1434) |
| **SSIM** | 0.3505 |
| **Landmark Score** | 0.2753 |
| **Pose Diff** | 26.7 deg |
| **Fused Score** | 0.2073 |
| **Aadhaar** | F, age 21 |
| **Selfie** | F, age 42 |
| **Age Gap** | 21 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.1620 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 21yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 16.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (14365ms total)
| Stage | Time |
|-------|------|
| load_ms | 34ms |
| enhancement_ms | 13105ms |
| clahe_ms | 13ms |
| face_processing_ms | 0ms |
| dual_path_ms | 605ms |
| similarity_ms | 607ms |
| **TOTAL** | **14365ms** |
