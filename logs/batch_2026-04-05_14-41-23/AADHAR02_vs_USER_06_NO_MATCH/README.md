# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:45:19  
**Aadhaar:** FILES\AADHAR\AADHAR02.jpg  
**Selfie:** FILES\SELFIE\USER_06.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0517 |
| **Confidence** | 5.2% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3772 (score: 0.1267) |
| **SSIM** | 0.2458 |
| **Landmark Score** | 0.5601 |
| **Pose Diff** | 11.8 deg |
| **Fused Score** | 0.2057 |
| **Aadhaar** | M, age 35 |
| **Selfie** | M, age 45 |
| **Age Gap** | 10 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4)
  2. Cosine similarity: 0.0517 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 10yr gap → threshold relaxed by 0.050 (effective: match=0.550, uncertain=0.350)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 5.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (11740ms total)
| Stage | Time |
|-------|------|
| load_ms | 140ms |
| enhancement_ms | 10438ms |
| clahe_ms | 49ms |
| face_processing_ms | 0ms |
| dual_path_ms | 555ms |
| similarity_ms | 557ms |
| **TOTAL** | **11740ms** |
