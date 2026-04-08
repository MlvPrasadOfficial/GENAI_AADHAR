# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:53:32  
**Aadhaar:** FILES\AADHAR\AADHAR001.jpg  
**Selfie:** FILES\SELFIE\USER_03.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0000 |
| **Confidence** | 0.0% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 1.4227 (score: 0.1183) |
| **SSIM** | 0.2115 |
| **Landmark Score** | 0.5250 |
| **Pose Diff** | 7.7 deg |
| **Fused Score** | 0.1642 |
| **Aadhaar** | M, age 36 |
| **Selfie** | F, age 28 |
| **Age Gap** | 8 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=0.85, Selfie=0.67, threshold=0.4)
  2. Cosine similarity: 0.0000 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 0.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (2049ms total)
| Stage | Time |
|-------|------|
| load_ms | 159ms |
| enhancement_ms | 108ms |
| clahe_ms | 44ms |
| face_processing_ms | 483ms |
| dual_path_ms | 627ms |
| similarity_ms | 628ms |
| **TOTAL** | **2049ms** |
