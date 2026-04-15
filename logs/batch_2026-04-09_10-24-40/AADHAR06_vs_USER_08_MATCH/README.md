# KYC Face Match — MATCH

**Timestamp:** 2026-04-09 10:38:23  
**Aadhaar:** FILES\AADHAR\AADHAR06.pdf  
**Selfie:** FILES\SELFIE\USER_08.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | MATCH |
| **Cosine Score** | 0.6161 |
| **Confidence** | 61.6% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 0.8762 (score: 0.2686) |
| **SSIM** | 0.1634 |
| **Landmark Score** | 0.3403 |
| **Pose Diff** | 27.8 deg |
| **Fused Score** | 0.4671 |
| **Aadhaar** | M, age 38 |
| **Selfie** | M, age 54 |
| **Age Gap** | 16 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.6161 → MATCH zone (>= 0.6 match threshold)
  2b. Age-gap relaxation: 16yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score above threshold with good quality
  5. Final decision: MATCH at 61.6% confidence
     Reason: Score above threshold with good quality — confident match
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (1173ms total)
| Stage | Time |
|-------|------|
| load_ms | 46ms |
| enhancement_ms | 38ms |
| clahe_ms | 13ms |
| face_processing_ms | 0ms |
| dual_path_ms | 537ms |
| similarity_ms | 539ms |
| **TOTAL** | **1173ms** |
