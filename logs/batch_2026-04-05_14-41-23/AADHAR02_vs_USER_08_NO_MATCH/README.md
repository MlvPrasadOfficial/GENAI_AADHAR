# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:45:48  
**Aadhaar:** FILES\AADHAR\AADHAR02.jpg  
**Selfie:** FILES\SELFIE\USER_08.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1639 |
| **Confidence** | 16.4% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2931 (score: 0.1437) |
| **SSIM** | 0.1990 |
| **Landmark Score** | 0.4568 |
| **Pose Diff** | 25.6 deg |
| **Fused Score** | 0.2386 |
| **Aadhaar** | M, age 35 |
| **Selfie** | M, age 54 |
| **Age Gap** | 19 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4)
  2. Cosine similarity: 0.1639 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 19yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 16.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (11869ms total)
| Stage | Time |
|-------|------|
| load_ms | 139ms |
| enhancement_ms | 10570ms |
| clahe_ms | 49ms |
| face_processing_ms | 0ms |
| dual_path_ms | 554ms |
| similarity_ms | 556ms |
| **TOTAL** | **11869ms** |
