# KYC Face Match — MATCH

**Timestamp:** 2026-04-09 10:56:20  
**Aadhaar:** FILES\AADHAR\AADHAR06.pdf  
**Selfie:** FILES\SELFIE\USER_09.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | MATCH |
| **Cosine Score** | 0.4876 |
| **Confidence** | 61.8% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.40 |
| **L2 Distance** | 1.0124 (score: 0.2190) |
| **SSIM** | 0.2255 |
| **Landmark Score** | 0.4165 |
| **Pose Diff** | 8.9 deg |
| **Fused Score** | 0.4168 |
| **Aadhaar** | M, age 38 |
| **Selfie** | M, age 79 |
| **Age Gap** | 41 years |
| **VLM Verdict** | Same person |
| **VLM Reasoning** | The eye socket shape, inter-pupillary distance, and nose bridge width are consistent, indicating the same bone structure. |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.40, threshold=0.4)
  2. Cosine similarity: 0.4876 → UNCERTAIN zone (between 0.4 and 0.6)
  2b. Age-gap relaxation: 41yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Invoked — cosine score in uncertain zone → VLM decides
     VLM verdict: SAME PERSON
  5. Final decision: MATCH at 61.8% confidence
     Confidence breakdown: base 48.8% → +8 VLM confirmation
     Reason: Score in uncertain zone, but VLM confirmed same person
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (29655ms total)
| Stage | Time |
|-------|------|
| load_ms | 55ms |
| enhancement_ms | 21ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 515ms |
| similarity_ms | 516ms |
| vlm_ms | 28540ms |
| **TOTAL** | **29655ms** |
