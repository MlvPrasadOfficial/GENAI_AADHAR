# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:57:07  
**Aadhaar:** FILES\AADHAR\AADHAR07.pdf  
**Selfie:** FILES\SELFIE\USER_10.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.5236 |
| **Confidence** | 42.4% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 0.9761 (score: 0.2313) |
| **SSIM** | 0.3158 |
| **Landmark Score** | 0.2184 |
| **Pose Diff** | 6.0 deg |
| **Fused Score** | 0.3973 |
| **Aadhaar** | M, age 24 |
| **Selfie** | M, age 21 |
| **Age Gap** | 3 years |
| **VLM Verdict** | Different person |
| **VLM Reasoning** | Bone structure differences in eye socket shape and inter-pupillary distance suggest different individuals. |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.5236 → UNCERTAIN zone (between 0.4 and 0.6)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Invoked — cosine score in uncertain zone → VLM decides
     VLM verdict: DIFFERENT PERSON
  5. Final decision: NO MATCH at 42.4% confidence
     Confidence breakdown: base 52.4% → -10 VLM rejection (uncertain zone)
     Reason: Score in uncertain zone and VLM says different person
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (23554ms total)
| Stage | Time |
|-------|------|
| load_ms | 52ms |
| enhancement_ms | 5526ms |
| clahe_ms | 14ms |
| face_processing_ms | 0ms |
| dual_path_ms | 532ms |
| similarity_ms | 535ms |
| vlm_ms | 16895ms |
| **TOTAL** | **23554ms** |
