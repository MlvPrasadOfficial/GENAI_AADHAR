# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:43:04  
**Aadhaar:** FILES\AADHAR\AADHAR001.jpg  
**Selfie:** FILES\SELFIE\USER_06.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0826 |
| **Confidence** | 8.3% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3545 (score: 0.1311) |
| **SSIM** | 0.3240 |
| **Landmark Score** | 0.6306 |
| **Pose Diff** | 8.2 deg |
| **Fused Score** | 0.2486 |
| **Aadhaar** | M, age 36 |
| **Selfie** | M, age 45 |
| **Age Gap** | 9 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=0.85, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.0826 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 9yr gap → threshold relaxed by 0.040 (effective: match=0.560, uncertain=0.360)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 8.3% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (3629ms total)
| Stage | Time |
|-------|------|
| load_ms | 276ms |
| enhancement_ms | 233ms |
| clahe_ms | 87ms |
| face_processing_ms | 1065ms |
| dual_path_ms | 982ms |
| similarity_ms | 985ms |
| **TOTAL** | **3629ms** |
