# KYC Face Match — NO MATCH

**Timestamp:** 2026-04-09 10:28:56  
**Aadhaar:** FILES\AADHAR\AADHAR02.jpg  
**Selfie:** FILES\SELFIE\USER_05.jpg  

## Result

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1259 |
| **Confidence** | 12.6% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3222 (score: 0.1376) |
| **SSIM** | 0.2925 |
| **Landmark Score** | 0.5673 |
| **Pose Diff** | 21.6 deg |
| **Fused Score** | 0.2541 |
| **Aadhaar** | M, age 33 |
| **Selfie** | F, age 25 |
| **Age Gap** | 8 years |

## Decision Trace
```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4)
  2. Cosine similarity: 0.1259 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 12.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```

## Face Crops
| Aadhaar | Selfie |
|---------|--------|
| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |

## Timings (10458ms total)
| Stage | Time |
|-------|------|
| load_ms | 104ms |
| enhancement_ms | 9361ms |
| clahe_ms | 46ms |
| face_processing_ms | 0ms |
| dual_path_ms | 472ms |
| similarity_ms | 474ms |
| **TOTAL** | **10458ms** |
