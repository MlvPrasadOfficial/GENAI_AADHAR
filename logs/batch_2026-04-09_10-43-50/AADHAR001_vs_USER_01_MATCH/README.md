# KYC Face Match — MATCH

**Timestamp:** 2026-04-09 10:46:42  
**Aadhaar:** FILES\AADHAR\AADHAR001.jpg  
**Selfie:** FILES\SELFIE\USER_01.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | MATCH |
| **Cosine Score** | 0.5739 |
| **Confidence** | 70.4% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 0.9232 (score: 0.2504) |
| **SSIM** | 0.2317 |
| **Landmark Score** | 0.6095 |
| **Pose Diff** | 6.1 deg |
| **Fused Score** | 0.5162 |
| **Aadhaar** | M, age 36 |
| **Selfie** | M, age 30 |
| **Age Gap** | 6 years |
| **VLM Verdict** | Same person |
| **VLM Reasoning** | The eye socket shape, inter-pupillary distance, and nose bridge width are consistent, indicating the same bone structure. |

## Decision Trace
```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=0.85, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.5739 → UNCERTAIN zone (between 0.4 and 0.6)
  2b. Age-gap relaxation: 6yr gap → threshold relaxed by 0.010 (effective: match=0.590, uncertain=0.390)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Invoked — cosine score in uncertain zone → VLM decides
     VLM verdict: SAME PERSON
  5. Final decision: MATCH at 70.4% confidence
     Confidence breakdown: base 57.4% → +8 VLM confirmation
     Reason: Score in uncertain zone, but VLM confirmed same person
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (172196ms total)
| Stage | Time |
|-------|------|
| load_ms | 97ms |
| enhancement_ms | 91ms |
| clahe_ms | 130ms |
| face_processing_ms | 1419ms |
| dual_path_ms | 485ms |
| similarity_ms | 488ms |
| vlm_ms | 169486ms |
| **TOTAL** | **172196ms** |
