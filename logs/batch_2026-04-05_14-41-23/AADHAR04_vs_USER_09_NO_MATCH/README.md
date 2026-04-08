# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-05 14:48:43  
**Aadhaar:** FILES\AADHAR\AADHAR04.jpg  
**Selfie:** FILES\SELFIE\USER_09.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0371 |
| **Confidence** | 3.7% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 0.40 |
| **L2 Distance** | 1.3877 (score: 0.1247) |
| **SSIM** | 0.2669 |
| **Landmark Score** | 0.4680 |
| **Pose Diff** | 15.9 deg |
| **Fused Score** | 0.1766 |
| **Aadhaar** | F, age 29 |
| **Selfie** | M, age 79 |
| **Age Gap** | 50 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4)
  2. Cosine similarity: 0.0371 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 50yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 3.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (11608ms total)
| Stage | Time |
|-------|------|
| load_ms | 136ms |
| enhancement_ms | 10373ms |
| clahe_ms | 48ms |
| face_processing_ms | 0ms |
| dual_path_ms | 524ms |
| similarity_ms | 527ms |
| **TOTAL** | **11608ms** |
