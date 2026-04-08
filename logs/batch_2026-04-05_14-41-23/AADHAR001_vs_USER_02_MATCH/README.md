# KYC Face Match — MATCH

**Timestamp:** 2026-04-05 14:42:45  
**Aadhaar:** FILES\AADHAR\AADHAR001.jpg  
**Selfie:** FILES\SELFIE\USER_02.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | MATCH |
| **Cosine Score** | 0.5075 |
| **Confidence** | 58.8% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 0.9925 (score: 0.2257) |
| **SSIM** | 0.3046 |
| **Landmark Score** | 0.6841 |
| **Pose Diff** | 7.0 deg |
| **Fused Score** | 0.5032 |
| **Aadhaar** | M, age 36 |
| **Selfie** | M, age 31 |
| **Age Gap** | 5 years |
| **VLM Verdict** | Same person |
| **VLM Reasoning** | The eye socket shape, inter-pupillary distance, and nose bridge width are consistent, indicating the same bone structure. |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=0.85, Selfie=0.92, threshold=0.4)
  2. Cosine similarity: 0.5075 → UNCERTAIN zone (between 0.4 and 0.6)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Invoked — cosine score in uncertain zone → VLM decides
     VLM verdict: SAME PERSON
  5. Final decision: MATCH at 58.8% confidence
     Confidence breakdown: base 50.8% → +8 VLM confirmation
     Reason: Score in uncertain zone, but VLM confirmed same person
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (47165ms total)
| Stage | Time |
|-------|------|
| load_ms | 207ms |
| enhancement_ms | 172ms |
| clahe_ms | 83ms |
| face_processing_ms | 1232ms |
| dual_path_ms | 1112ms |
| similarity_ms | 1116ms |
| vlm_ms | 43243ms |
| **TOTAL** | **47165ms** |
