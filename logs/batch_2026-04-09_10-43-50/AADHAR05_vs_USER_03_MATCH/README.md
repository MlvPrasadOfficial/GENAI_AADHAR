# KYC Face Match — MATCH

**Timestamp:** 2026-04-09 10:52:23  
**Aadhaar:** FILES\AADHAR\AADHAR05.pdf  
**Selfie:** FILES\SELFIE\USER_03.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | MATCH |
| **Cosine Score** | 0.6303 |
| **Confidence** | 63.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 0.8599 (score: 0.2753) |
| **SSIM** | 0.2301 |
| **Landmark Score** | 0.6264 |
| **Pose Diff** | 8.6 deg |
| **Fused Score** | 0.5538 |
| **Aadhaar** | F, age 28 |
| **Selfie** | F, age 28 |
| **Age Gap** | 0 years |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.67, threshold=0.4)
  2. Cosine similarity: 0.6303 → MATCH zone (>= 0.6 match threshold)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score above threshold with good quality
  5. Final decision: MATCH at 63.0% confidence
     Reason: Score above threshold with good quality — confident match
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (878ms total)
| Stage | Time |
|-------|------|
| load_ms | 42ms |
| enhancement_ms | 34ms |
| clahe_ms | 11ms |
| face_processing_ms | 0ms |
| dual_path_ms | 395ms |
| similarity_ms | 396ms |
| **TOTAL** | **878ms** |
