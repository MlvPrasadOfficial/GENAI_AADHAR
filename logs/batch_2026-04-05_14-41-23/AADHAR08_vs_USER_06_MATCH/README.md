# KYC Face Match — MATCH

**Timestamp:** 2026-04-05 14:55:16  
**Aadhaar:** FILES\AADHAR\AADHAR08.pdf  
**Selfie:** FILES\SELFIE\USER_06.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | MATCH |
| **Cosine Score** | 0.5427 |
| **Confidence** | 67.3% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 0.9564 (score: 0.2382) |
| **SSIM** | 0.3884 |
| **Landmark Score** | 0.3610 |
| **Pose Diff** | 12.3 deg |
| **Fused Score** | 0.4514 |
| **Aadhaar** | F, age 22 |
| **Selfie** | M, age 45 |
| **Age Gap** | 23 years |
| **VLM Verdict** | Same person |
| **VLM Reasoning** | The eye socket shape, inter-pupillary distance, and nose bridge width are consistent, indicating the same bone structure. |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.5427 → UNCERTAIN zone (between 0.4 and 0.6)
  2b. Age-gap relaxation: 23yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Invoked — cosine score in uncertain zone → VLM decides
     VLM verdict: SAME PERSON
  5. Final decision: MATCH at 67.3% confidence
     Confidence breakdown: base 54.3% → +8 VLM confirmation
     Reason: Score in uncertain zone, but VLM confirmed same person
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (35641ms total)
| Stage | Time |
|-------|------|
| load_ms | 125ms |
| enhancement_ms | 54ms |
| clahe_ms | 57ms |
| face_processing_ms | 0ms |
| dual_path_ms | 1405ms |
| similarity_ms | 1407ms |
| vlm_ms | 32594ms |
| **TOTAL** | **35641ms** |
