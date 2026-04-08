# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:59:39  
**Aadhaar:** FILES\AADHAR\AADHAR04.jpg  
**Selfie:** FILES\SELFIE\USER_08.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0384 |
| **Confidence** | 3.8% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3868 (score: 0.1249) |
| **SSIM** | 0.2416 |
| **Landmark Score** | 0.4658 |
| **Pose Diff** | 22.5 deg |
| **Fused Score** | 0.1742 |
| **Aadhaar** | F, age 31 |
| **Selfie** | M, age 54 |
| **Age Gap** | 23 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4)
  2. Cosine similarity: 0.0384 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 23yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 3.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (11740ms total)
| Stage | Time |
|-------|------|
| load_ms | 133ms |
| enhancement_ms | 10647ms |
| clahe_ms | 51ms |
| face_processing_ms | 0ms |
| dual_path_ms | 454ms |
| similarity_ms | 455ms |
| **TOTAL** | **11740ms** |
