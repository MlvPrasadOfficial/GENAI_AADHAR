# Aadhaar KYC Face Matching — Batch Report

**Timestamp:** 2026-04-05 15:04:28  
**Total pairs:** 90  
**Matches:** 9/90  
**Pipeline version:** v2  

## Results Summary

| # | Aadhaar | Selfie | Result | Cosine | Confidence | Aadhaar Age | Selfie Age | Age Gap | VLM |
|---|---------|--------|--------|--------|------------|-------------|------------|---------|-----|
| 1 | AADHAR001.jpg | USER_01.jpg | **MATCH** | 0.5739 | 70.4% | M age 36 | M age 30 | 6yr | Confirmed |
| 2 | AADHAR001.jpg | USER_02.jpg | **MATCH** | 0.5075 | 58.8% | M age 36 | M age 31 | 5yr | Confirmed |
| 3 | AADHAR001.jpg | USER_03.jpg | NO MATCH | 0.0000 | 0.0% | M age 36 | F age 28 | 8yr | --- :warning: |
| 4 | AADHAR001.jpg | USER_04.jpg | NO MATCH | 0.0469 | 4.7% | M age 38 | F age 42 | 4yr | --- :warning: |
| 5 | AADHAR001.jpg | USER_05.jpg | NO MATCH | 0.1110 | 11.1% | M age 36 | F age 25 | 11yr | --- :warning: |
| 6 | AADHAR001.jpg | USER_06.jpg | NO MATCH | 0.0826 | 8.3% | M age 36 | M age 45 | 9yr | --- |
| 7 | AADHAR001.jpg | USER_07.jpg | NO MATCH | 0.2143 | 21.4% | M age 36 | M age 38 | 2yr | --- |
| 8 | AADHAR001.jpg | USER_08.jpg | NO MATCH | 0.2622 | 26.2% | M age 36 | M age 54 | 18yr | --- |
| 9 | AADHAR001.jpg | USER_09.jpg | NO MATCH | 0.1618 | 16.2% | M age 36 | M age 79 | 43yr | --- |
| 10 | AADHAR001.jpg | USER_10.jpg | NO MATCH | 0.2456 | 24.6% | M age 38 | M age 21 | 17yr | --- |
| 11 | AADHAR02.jpg | USER_01.jpg | NO MATCH | 0.2388 | 23.9% | M age 33 | M age 30 | 3yr | --- |
| 12 | AADHAR02.jpg | USER_02.jpg | NO MATCH | 0.2564 | 25.6% | M age 35 | M age 31 | 4yr | --- |
| 13 | AADHAR02.jpg | USER_03.jpg | NO MATCH | 0.0021 | 0.2% | M age 33 | F age 28 | 5yr | --- :warning: |
| 14 | AADHAR02.jpg | USER_04.jpg | NO MATCH | 0.0388 | 3.9% | M age 33 | F age 42 | 9yr | --- :warning: |
| 15 | AADHAR02.jpg | USER_05.jpg | NO MATCH | 0.1259 | 12.6% | M age 33 | F age 25 | 8yr | --- :warning: |
| 16 | AADHAR02.jpg | USER_06.jpg | NO MATCH | 0.0517 | 5.2% | M age 35 | M age 45 | 10yr | --- |
| 17 | AADHAR02.jpg | USER_07.jpg | NO MATCH | 0.1027 | 10.3% | M age 35 | M age 38 | 3yr | --- |
| 18 | AADHAR02.jpg | USER_08.jpg | NO MATCH | 0.1639 | 16.4% | M age 35 | M age 54 | 19yr | --- |
| 19 | AADHAR02.jpg | USER_09.jpg | NO MATCH | 0.0822 | 8.2% | M age 35 | M age 79 | 44yr | --- |
| 20 | AADHAR02.jpg | USER_10.jpg | NO MATCH | 0.1247 | 12.5% | M age 33 | M age 21 | 12yr | --- |
| 21 | AADHAR03.jpg | USER_01.jpg | NO MATCH | 0.1454 | 14.5% | F age 36 | M age 30 | 6yr | --- :warning: |
| 22 | AADHAR03.jpg | USER_02.jpg | NO MATCH | 0.2570 | 25.7% | F age 36 | M age 31 | 5yr | --- :warning: |
| 23 | AADHAR03.jpg | USER_03.jpg | NO MATCH | 0.1512 | 15.1% | F age 36 | F age 28 | 8yr | --- |
| 24 | AADHAR03.jpg | USER_04.jpg | NO MATCH | 0.0712 | 7.1% | F age 33 | F age 42 | 9yr | --- |
| 25 | AADHAR03.jpg | USER_05.jpg | NO MATCH | 0.1873 | 18.7% | F age 33 | F age 25 | 8yr | --- |
| 26 | AADHAR03.jpg | USER_06.jpg | NO MATCH | 0.1859 | 18.6% | F age 36 | M age 45 | 9yr | --- :warning: |
| 27 | AADHAR03.jpg | USER_07.jpg | NO MATCH | 0.1483 | 14.8% | F age 36 | M age 38 | 2yr | --- :warning: |
| 28 | AADHAR03.jpg | USER_08.jpg | NO MATCH | 0.1968 | 19.7% | F age 36 | M age 54 | 18yr | --- :warning: |
| 29 | AADHAR03.jpg | USER_09.jpg | NO MATCH | 0.1237 | 12.4% | F age 36 | M age 79 | 43yr | --- :warning: |
| 30 | AADHAR03.jpg | USER_10.jpg | NO MATCH | 0.0930 | 9.3% | F age 33 | M age 21 | 12yr | --- :warning: |
| 31 | AADHAR04.jpg | USER_01.jpg | NO MATCH | 0.0484 | 4.8% | F age 29 | M age 30 | 1yr | --- :warning: |
| 32 | AADHAR04.jpg | USER_02.jpg | NO MATCH | 0.0307 | 3.1% | F age 29 | M age 31 | 2yr | --- :warning: |
| 33 | AADHAR04.jpg | USER_03.jpg | NO MATCH | 0.1176 | 11.8% | F age 29 | F age 28 | 1yr | --- |
| 34 | AADHAR04.jpg | USER_04.jpg | NO MATCH | 0.0653 | 6.5% | F age 29 | F age 42 | 13yr | --- |
| 35 | AADHAR04.jpg | USER_05.jpg | NO MATCH | 0.1058 | 10.6% | F age 29 | F age 25 | 4yr | --- |
| 36 | AADHAR04.jpg | USER_06.jpg | NO MATCH | 0.1176 | 11.8% | F age 31 | M age 45 | 14yr | --- :warning: |
| 37 | AADHAR04.jpg | USER_07.jpg | NO MATCH | 0.0477 | 4.8% | F age 29 | M age 38 | 9yr | --- :warning: |
| 38 | AADHAR04.jpg | USER_08.jpg | NO MATCH | 0.0384 | 3.8% | F age 31 | M age 54 | 23yr | --- :warning: |
| 39 | AADHAR04.jpg | USER_09.jpg | NO MATCH | 0.0371 | 3.7% | F age 29 | M age 79 | 50yr | --- :warning: |
| 40 | AADHAR04.jpg | USER_10.jpg | NO MATCH | 0.0237 | 2.4% | F age 29 | M age 21 | 8yr | --- :warning: |
| 41 | AADHAR05.pdf | USER_01.jpg | NO MATCH | 0.0701 | 7.0% | F age 33 | M age 30 | 3yr | --- :warning: |
| 42 | AADHAR05.pdf | USER_02.jpg | NO MATCH | 0.0925 | 9.3% | F age 28 | M age 31 | 3yr | --- :warning: |
| 43 | AADHAR05.pdf | USER_03.jpg | **MATCH** | 0.6303 | 63.0% | F age 28 | F age 28 | 0yr | --- |
| 44 | AADHAR05.pdf | USER_04.jpg | NO MATCH | 0.0364 | 3.6% | F age 28 | F age 42 | 14yr | --- |
| 45 | AADHAR05.pdf | USER_05.jpg | NO MATCH | 0.0459 | 4.6% | F age 33 | F age 25 | 8yr | --- |
| 46 | AADHAR05.pdf | USER_06.jpg | NO MATCH | 0.0799 | 8.0% | F age 33 | M age 45 | 12yr | --- :warning: |
| 47 | AADHAR05.pdf | USER_07.jpg | NO MATCH | 0.0895 | 9.0% | F age 33 | M age 38 | 5yr | --- :warning: |
| 48 | AADHAR05.pdf | USER_08.jpg | NO MATCH | 0.1724 | 17.2% | F age 33 | M age 54 | 21yr | --- :warning: |
| 49 | AADHAR05.pdf | USER_09.jpg | NO MATCH | 0.0780 | 7.8% | F age 28 | M age 79 | 51yr | --- :warning: |
| 50 | AADHAR05.pdf | USER_10.jpg | NO MATCH | 0.0566 | 5.7% | F age 33 | M age 21 | 12yr | --- :warning: |
| 51 | AADHAR06.pdf | USER_01.jpg | NO MATCH | 0.2274 | 22.7% | M age 38 | M age 30 | 8yr | --- |
| 52 | AADHAR06.pdf | USER_02.jpg | NO MATCH | 0.3732 | 27.3% | M age 39 | M age 31 | 8yr | --- |
| 53 | AADHAR06.pdf | USER_03.jpg | NO MATCH | 0.0960 | 9.6% | M age 38 | F age 28 | 10yr | --- :warning: |
| 54 | AADHAR06.pdf | USER_04.jpg | NO MATCH | 0.0000 | 0.0% | M age 38 | F age 42 | 4yr | --- :warning: |
| 55 | AADHAR06.pdf | USER_05.jpg | NO MATCH | 0.1722 | 17.2% | M age 39 | F age 25 | 14yr | --- :warning: |
| 56 | AADHAR06.pdf | USER_06.jpg | NO MATCH | 0.1824 | 18.2% | M age 39 | M age 45 | 6yr | --- |
| 57 | AADHAR06.pdf | USER_07.jpg | **MATCH** | 0.5986 | 67.9% | M age 38 | M age 38 | 0yr | Confirmed |
| 58 | AADHAR06.pdf | USER_08.jpg | **MATCH** | 0.6161 | 61.6% | M age 38 | M age 54 | 16yr | --- |
| 59 | AADHAR06.pdf | USER_09.jpg | **MATCH** | 0.4876 | 61.8% | M age 38 | M age 79 | 41yr | Confirmed |
| 60 | AADHAR06.pdf | USER_10.jpg | NO MATCH | 0.2322 | 23.2% | M age 38 | M age 21 | 17yr | --- |
| 61 | AADHAR07.pdf | USER_01.jpg | NO MATCH | 0.0551 | 5.5% | M age 24 | M age 30 | 6yr | --- |
| 62 | AADHAR07.pdf | USER_02.jpg | NO MATCH | 0.2092 | 20.9% | M age 24 | M age 31 | 7yr | --- |
| 63 | AADHAR07.pdf | USER_03.jpg | NO MATCH | 0.1662 | 16.6% | F age 25 | F age 28 | 3yr | --- |
| 64 | AADHAR07.pdf | USER_04.jpg | NO MATCH | 0.0646 | 6.5% | F age 25 | F age 42 | 17yr | --- |
| 65 | AADHAR07.pdf | USER_05.jpg | NO MATCH | 0.2239 | 22.4% | F age 25 | F age 25 | 0yr | --- |
| 66 | AADHAR07.pdf | USER_06.jpg | NO MATCH | 0.2841 | 28.4% | F age 25 | M age 45 | 20yr | --- :warning: |
| 67 | AADHAR07.pdf | USER_07.jpg | NO MATCH | 0.2082 | 20.8% | F age 25 | M age 38 | 13yr | --- :warning: |
| 68 | AADHAR07.pdf | USER_08.jpg | NO MATCH | 0.2035 | 20.3% | F age 25 | M age 54 | 29yr | --- :warning: |
| 69 | AADHAR07.pdf | USER_09.jpg | NO MATCH | 0.1893 | 18.9% | F age 25 | M age 79 | 54yr | --- :warning: |
| 70 | AADHAR07.pdf | USER_10.jpg | NO MATCH | 0.5236 | 42.4% | M age 24 | M age 21 | 3yr | Rejected |
| 71 | AADHAR08.pdf | USER_01.jpg | NO MATCH | 0.1281 | 12.8% | F age 21 | M age 30 | 9yr | --- :warning: |
| 72 | AADHAR08.pdf | USER_02.jpg | NO MATCH | 0.1939 | 19.4% | F age 21 | M age 31 | 10yr | --- :warning: |
| 73 | AADHAR08.pdf | USER_03.jpg | NO MATCH | 0.2529 | 25.3% | F age 21 | F age 28 | 7yr | --- |
| 74 | AADHAR08.pdf | USER_04.jpg | NO MATCH | 0.1620 | 16.2% | F age 21 | F age 42 | 21yr | --- |
| 75 | AADHAR08.pdf | USER_05.jpg | **MATCH** | 0.5615 | 64.1% | F age 22 | F age 25 | 3yr | Confirmed |
| 76 | AADHAR08.pdf | USER_06.jpg | **MATCH** | 0.5427 | 67.3% | F age 22 | M age 45 | 23yr | Confirmed :warning: |
| 77 | AADHAR08.pdf | USER_07.jpg | NO MATCH | 0.1710 | 17.1% | F age 22 | M age 38 | 16yr | --- :warning: |
| 78 | AADHAR08.pdf | USER_08.jpg | NO MATCH | 0.1804 | 18.0% | F age 21 | M age 54 | 33yr | --- :warning: |
| 79 | AADHAR08.pdf | USER_09.jpg | NO MATCH | 0.1704 | 17.0% | F age 22 | M age 79 | 57yr | --- :warning: |
| 80 | AADHAR08.pdf | USER_10.jpg | NO MATCH | 0.2137 | 21.4% | F age 22 | M age 21 | 1yr | --- :warning: |
| 81 | AADHAR09.pdf | USER_01.jpg | NO MATCH | 0.0753 | 7.5% | M age 39 | M age 30 | 9yr | --- |
| 82 | AADHAR09.pdf | USER_02.jpg | NO MATCH | 0.1469 | 14.7% | M age 39 | M age 31 | 8yr | --- |
| 83 | AADHAR09.pdf | USER_03.jpg | NO MATCH | 0.1099 | 11.0% | M age 31 | F age 28 | 3yr | --- :warning: |
| 84 | AADHAR09.pdf | USER_04.jpg | **MATCH** | 0.6337 | 66.4% | M age 39 | F age 42 | 3yr | Confirmed :warning: |
| 85 | AADHAR09.pdf | USER_05.jpg | NO MATCH | 0.0000 | 0.0% | M age 31 | F age 25 | 6yr | --- :warning: |
| 86 | AADHAR09.pdf | USER_06.jpg | NO MATCH | 0.1303 | 13.0% | M age 31 | M age 45 | 14yr | --- |
| 87 | AADHAR09.pdf | USER_07.jpg | NO MATCH | 0.0052 | 0.5% | M age 31 | M age 38 | 7yr | --- |
| 88 | AADHAR09.pdf | USER_08.jpg | NO MATCH | 0.1670 | 16.7% | M age 31 | M age 54 | 23yr | --- |
| 89 | AADHAR09.pdf | USER_09.jpg | NO MATCH | 0.0519 | 5.2% | M age 31 | M age 79 | 48yr | --- |
| 90 | AADHAR09.pdf | USER_10.jpg | NO MATCH | 0.0091 | 0.9% | M age 39 | M age 21 | 18yr | --- |

## Per-Pair Details

### 1. AADHAR001.jpg vs USER_01.jpg

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
| **Aadhaar Demographics** | M, age 36 |
| **Selfie Demographics** | M, age 30 |
| **Age Gap** | 6 years |
| **Gender** | Consistent |
| **VLM Verdict** | Same person |
| **VLM Reasoning** | The eye socket shape, inter-pupillary distance, and nose bridge width are consistent, indicating the same bone structure. |

<details><summary>Decision Trace</summary>

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
</details>

<details><summary>Timings (total 61380ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 153ms |
| enhancement_ms | 147ms |
| clahe_ms | 184ms |
| face_processing_ms | 2490ms |
| dual_path_ms | 1200ms |
| similarity_ms | 1208ms |
| vlm_ms | 55998ms |
| **TOTAL** | **61380ms** |
</details>

**Face Crops:** [AADHAR001_vs_USER_01_MATCH/aadhaar_crop.jpg](AADHAR001_vs_USER_01_MATCH/aadhaar_crop.jpg) | [AADHAR001_vs_USER_01_MATCH/selfie_crop.jpg](AADHAR001_vs_USER_01_MATCH/selfie_crop.jpg)

---

### 2. AADHAR001.jpg vs USER_02.jpg

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
| **Aadhaar Demographics** | M, age 36 |
| **Selfie Demographics** | M, age 31 |
| **Age Gap** | 5 years |
| **Gender** | Consistent |
| **VLM Verdict** | Same person |
| **VLM Reasoning** | The eye socket shape, inter-pupillary distance, and nose bridge width are consistent, indicating the same bone structure. |

<details><summary>Decision Trace</summary>

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
</details>

<details><summary>Timings (total 68090ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 199ms |
| enhancement_ms | 176ms |
| clahe_ms | 90ms |
| face_processing_ms | 927ms |
| dual_path_ms | 1174ms |
| similarity_ms | 1176ms |
| vlm_ms | 64348ms |
| **TOTAL** | **68090ms** |
</details>

**Face Crops:** [AADHAR001_vs_USER_02_MATCH/aadhaar_crop.jpg](AADHAR001_vs_USER_02_MATCH/aadhaar_crop.jpg) | [AADHAR001_vs_USER_02_MATCH/selfie_crop.jpg](AADHAR001_vs_USER_02_MATCH/selfie_crop.jpg)

---

### 3. AADHAR001.jpg vs USER_03.jpg

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
| **Aadhaar Demographics** | M, age 36 |
| **Selfie Demographics** | F, age 28 |
| **Age Gap** | 8 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=0.85, Selfie=0.67, threshold=0.4)
  2. Cosine similarity: 0.0000 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 0.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 2049ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 159ms |
| enhancement_ms | 108ms |
| clahe_ms | 44ms |
| face_processing_ms | 483ms |
| dual_path_ms | 627ms |
| similarity_ms | 628ms |
| **TOTAL** | **2049ms** |
</details>

**Face Crops:** [AADHAR001_vs_USER_03_NO_MATCH/aadhaar_crop.jpg](AADHAR001_vs_USER_03_NO_MATCH/aadhaar_crop.jpg) | [AADHAR001_vs_USER_03_NO_MATCH/selfie_crop.jpg](AADHAR001_vs_USER_03_NO_MATCH/selfie_crop.jpg)

---

### 4. AADHAR001.jpg vs USER_04.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0469 |
| **Confidence** | 4.7% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.3806 (score: 0.1261) |
| **SSIM** | 0.3580 |
| **Landmark Score** | 0.5621 |
| **Pose Diff** | 20.5 deg |
| **Fused Score** | 0.2147 |
| **Aadhaar Demographics** | M, age 38 |
| **Selfie Demographics** | F, age 42 |
| **Age Gap** | 4 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.0469 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 4.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 10014ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 138ms |
| enhancement_ms | 6524ms |
| clahe_ms | 95ms |
| face_processing_ms | 939ms |
| dual_path_ms | 1158ms |
| similarity_ms | 1161ms |
| **TOTAL** | **10014ms** |
</details>

**Face Crops:** [AADHAR001_vs_USER_04_NO_MATCH/aadhaar_crop.jpg](AADHAR001_vs_USER_04_NO_MATCH/aadhaar_crop.jpg) | [AADHAR001_vs_USER_04_NO_MATCH/selfie_crop.jpg](AADHAR001_vs_USER_04_NO_MATCH/selfie_crop.jpg)

---

### 5. AADHAR001.jpg vs USER_05.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1110 |
| **Confidence** | 11.1% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3335 (score: 0.1353) |
| **SSIM** | 0.2917 |
| **Landmark Score** | 0.6421 |
| **Pose Diff** | 26.2 deg |
| **Fused Score** | 0.2642 |
| **Aadhaar Demographics** | M, age 36 |
| **Selfie Demographics** | F, age 25 |
| **Age Gap** | 11 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=0.85, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1110 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 11yr gap → threshold relaxed by 0.060 (effective: match=0.540, uncertain=0.340)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 11.1% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 3907ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 253ms |
| enhancement_ms | 184ms |
| clahe_ms | 92ms |
| face_processing_ms | 723ms |
| dual_path_ms | 1326ms |
| similarity_ms | 1329ms |
| **TOTAL** | **3907ms** |
</details>

**Face Crops:** [AADHAR001_vs_USER_05_NO_MATCH/aadhaar_crop.jpg](AADHAR001_vs_USER_05_NO_MATCH/aadhaar_crop.jpg) | [AADHAR001_vs_USER_05_NO_MATCH/selfie_crop.jpg](AADHAR001_vs_USER_05_NO_MATCH/selfie_crop.jpg)

---

### 6. AADHAR001.jpg vs USER_06.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0826 |
| **Confidence** | 8.3% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3545 (score: 0.1311) |
| **SSIM** | 0.3240 |
| **Landmark Score** | 0.6306 |
| **Pose Diff** | 8.2 deg |
| **Fused Score** | 0.2486 |
| **Aadhaar Demographics** | M, age 36 |
| **Selfie Demographics** | M, age 45 |
| **Age Gap** | 9 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=0.85, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.0826 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 9yr gap → threshold relaxed by 0.040 (effective: match=0.560, uncertain=0.360)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 8.3% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 3635ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 212ms |
| enhancement_ms | 246ms |
| clahe_ms | 90ms |
| face_processing_ms | 983ms |
| dual_path_ms | 1050ms |
| similarity_ms | 1053ms |
| **TOTAL** | **3635ms** |
</details>

**Face Crops:** [AADHAR001_vs_USER_06_NO_MATCH/aadhaar_crop.jpg](AADHAR001_vs_USER_06_NO_MATCH/aadhaar_crop.jpg) | [AADHAR001_vs_USER_06_NO_MATCH/selfie_crop.jpg](AADHAR001_vs_USER_06_NO_MATCH/selfie_crop.jpg)

---

### 7. AADHAR001.jpg vs USER_07.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2143 |
| **Confidence** | 21.4% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.2535 (score: 0.1525) |
| **SSIM** | 0.3849 |
| **Landmark Score** | 0.6209 |
| **Pose Diff** | 18.9 deg |
| **Fused Score** | 0.3268 |
| **Aadhaar Demographics** | M, age 36 |
| **Selfie Demographics** | M, age 38 |
| **Age Gap** | 2 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.2143 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 21.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 10178ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 257ms |
| enhancement_ms | 6552ms |
| clahe_ms | 88ms |
| face_processing_ms | 829ms |
| dual_path_ms | 1224ms |
| similarity_ms | 1228ms |
| **TOTAL** | **10178ms** |
</details>

**Face Crops:** [AADHAR001_vs_USER_07_NO_MATCH/aadhaar_crop.jpg](AADHAR001_vs_USER_07_NO_MATCH/aadhaar_crop.jpg) | [AADHAR001_vs_USER_07_NO_MATCH/selfie_crop.jpg](AADHAR001_vs_USER_07_NO_MATCH/selfie_crop.jpg)

---

### 8. AADHAR001.jpg vs USER_08.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2622 |
| **Confidence** | 26.2% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2147 (score: 0.1617) |
| **SSIM** | 0.2281 |
| **Landmark Score** | 0.6064 |
| **Pose Diff** | 33.3 deg |
| **Fused Score** | 0.3348 |
| **Aadhaar Demographics** | M, age 36 |
| **Selfie Demographics** | M, age 54 |
| **Age Gap** | 18 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=0.85, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.2622 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 18yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 26.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 3300ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 259ms |
| enhancement_ms | 241ms |
| clahe_ms | 80ms |
| face_processing_ms | 1030ms |
| dual_path_ms | 843ms |
| similarity_ms | 847ms |
| **TOTAL** | **3300ms** |
</details>

**Face Crops:** [AADHAR001_vs_USER_08_NO_MATCH/aadhaar_crop.jpg](AADHAR001_vs_USER_08_NO_MATCH/aadhaar_crop.jpg) | [AADHAR001_vs_USER_08_NO_MATCH/selfie_crop.jpg](AADHAR001_vs_USER_08_NO_MATCH/selfie_crop.jpg)

---

### 9. AADHAR001.jpg vs USER_09.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1618 |
| **Confidence** | 16.2% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 0.40 |
| **L2 Distance** | 1.2948 (score: 0.1434) |
| **SSIM** | 0.2798 |
| **Landmark Score** | 0.5672 |
| **Pose Diff** | 16.3 deg |
| **Fused Score** | 0.2731 |
| **Aadhaar Demographics** | M, age 36 |
| **Selfie Demographics** | M, age 79 |
| **Age Gap** | 43 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=0.85, Selfie=0.40, threshold=0.4)
  2. Cosine similarity: 0.1618 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 43yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 16.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 5508ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 258ms |
| enhancement_ms | 210ms |
| clahe_ms | 92ms |
| face_processing_ms | 942ms |
| dual_path_ms | 2001ms |
| similarity_ms | 2005ms |
| **TOTAL** | **5508ms** |
</details>

**Face Crops:** [AADHAR001_vs_USER_09_NO_MATCH/aadhaar_crop.jpg](AADHAR001_vs_USER_09_NO_MATCH/aadhaar_crop.jpg) | [AADHAR001_vs_USER_09_NO_MATCH/selfie_crop.jpg](AADHAR001_vs_USER_09_NO_MATCH/selfie_crop.jpg)

---

### 10. AADHAR001.jpg vs USER_10.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2456 |
| **Confidence** | 24.6% |
| **Aadhaar Quality** | 0.85 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.2283 (score: 0.1584) |
| **SSIM** | 0.4578 |
| **Landmark Score** | 0.3429 |
| **Pose Diff** | 10.1 deg |
| **Fused Score** | 0.2825 |
| **Aadhaar Demographics** | M, age 38 |
| **Selfie Demographics** | M, age 21 |
| **Age Gap** | 17 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.2456 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 17yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 24.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 14978ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 402ms |
| enhancement_ms | 12596ms |
| clahe_ms | 62ms |
| face_processing_ms | 557ms |
| dual_path_ms | 679ms |
| similarity_ms | 682ms |
| **TOTAL** | **14978ms** |
</details>

**Face Crops:** [AADHAR001_vs_USER_10_NO_MATCH/aadhaar_crop.jpg](AADHAR001_vs_USER_10_NO_MATCH/aadhaar_crop.jpg) | [AADHAR001_vs_USER_10_NO_MATCH/selfie_crop.jpg](AADHAR001_vs_USER_10_NO_MATCH/selfie_crop.jpg)

---

### 11. AADHAR02.jpg vs USER_01.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2388 |
| **Confidence** | 23.9% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2339 (score: 0.1571) |
| **SSIM** | 0.2065 |
| **Landmark Score** | 0.4406 |
| **Pose Diff** | 13.4 deg |
| **Fused Score** | 0.2778 |
| **Aadhaar Demographics** | M, age 33 |
| **Selfie Demographics** | M, age 30 |
| **Age Gap** | 3 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4)
  2. Cosine similarity: 0.2388 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 23.9% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 14845ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 178ms |
| enhancement_ms | 10591ms |
| clahe_ms | 87ms |
| face_processing_ms | 1039ms |
| dual_path_ms | 1474ms |
| similarity_ms | 1477ms |
| **TOTAL** | **14845ms** |
</details>

**Face Crops:** [AADHAR02_vs_USER_01_NO_MATCH/aadhaar_crop.jpg](AADHAR02_vs_USER_01_NO_MATCH/aadhaar_crop.jpg) | [AADHAR02_vs_USER_01_NO_MATCH/selfie_crop.jpg](AADHAR02_vs_USER_01_NO_MATCH/selfie_crop.jpg)

---

### 12. AADHAR02.jpg vs USER_02.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2564 |
| **Confidence** | 25.6% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.2195 (score: 0.1605) |
| **SSIM** | 0.2501 |
| **Landmark Score** | 0.5933 |
| **Pose Diff** | 8.6 deg |
| **Fused Score** | 0.3304 |
| **Aadhaar Demographics** | M, age 35 |
| **Selfie Demographics** | M, age 31 |
| **Age Gap** | 4 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4)
  2. Cosine similarity: 0.2564 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 25.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 14343ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 284ms |
| enhancement_ms | 10720ms |
| clahe_ms | 93ms |
| face_processing_ms | 0ms |
| dual_path_ms | 1622ms |
| similarity_ms | 1624ms |
| **TOTAL** | **14343ms** |
</details>

**Face Crops:** [AADHAR02_vs_USER_02_NO_MATCH/aadhaar_crop.jpg](AADHAR02_vs_USER_02_NO_MATCH/aadhaar_crop.jpg) | [AADHAR02_vs_USER_02_NO_MATCH/selfie_crop.jpg](AADHAR02_vs_USER_02_NO_MATCH/selfie_crop.jpg)

---

### 13. AADHAR02.jpg vs USER_03.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0021 |
| **Confidence** | 0.2% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 1.4127 (score: 0.1201) |
| **SSIM** | 0.2456 |
| **Landmark Score** | 0.6167 |
| **Pose Diff** | 6.9 deg |
| **Fused Score** | 0.1919 |
| **Aadhaar Demographics** | M, age 33 |
| **Selfie Demographics** | F, age 28 |
| **Age Gap** | 5 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4)
  2. Cosine similarity: 0.0021 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 0.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 13449ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 318ms |
| enhancement_ms | 10685ms |
| clahe_ms | 95ms |
| face_processing_ms | 0ms |
| dual_path_ms | 1174ms |
| similarity_ms | 1177ms |
| **TOTAL** | **13449ms** |
</details>

**Face Crops:** [AADHAR02_vs_USER_03_NO_MATCH/aadhaar_crop.jpg](AADHAR02_vs_USER_03_NO_MATCH/aadhaar_crop.jpg) | [AADHAR02_vs_USER_03_NO_MATCH/selfie_crop.jpg](AADHAR02_vs_USER_03_NO_MATCH/selfie_crop.jpg)

---

### 14. AADHAR02.jpg vs USER_04.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0388 |
| **Confidence** | 3.9% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.3865 (score: 0.1250) |
| **SSIM** | 0.3511 |
| **Landmark Score** | 0.3974 |
| **Pose Diff** | 10.3 deg |
| **Fused Score** | 0.1683 |
| **Aadhaar Demographics** | M, age 33 |
| **Selfie Demographics** | F, age 42 |
| **Age Gap** | 9 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4), Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.0388 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 9yr gap → threshold relaxed by 0.040 (effective: match=0.560, uncertain=0.360)
  3. Quality flag: LOW (Aadhaar, Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 3.9% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 19986ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 267ms |
| enhancement_ms | 17736ms |
| clahe_ms | 90ms |
| face_processing_ms | 0ms |
| dual_path_ms | 946ms |
| similarity_ms | 948ms |
| **TOTAL** | **19986ms** |
</details>

**Face Crops:** [AADHAR02_vs_USER_04_NO_MATCH/aadhaar_crop.jpg](AADHAR02_vs_USER_04_NO_MATCH/aadhaar_crop.jpg) | [AADHAR02_vs_USER_04_NO_MATCH/selfie_crop.jpg](AADHAR02_vs_USER_04_NO_MATCH/selfie_crop.jpg)

---

### 15. AADHAR02.jpg vs USER_05.jpg

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
| **Aadhaar Demographics** | M, age 33 |
| **Selfie Demographics** | F, age 25 |
| **Age Gap** | 8 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4)
  2. Cosine similarity: 0.1259 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 12.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 26713ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 239ms |
| enhancement_ms | 25276ms |
| clahe_ms | 52ms |
| face_processing_ms | 0ms |
| dual_path_ms | 572ms |
| similarity_ms | 574ms |
| **TOTAL** | **26713ms** |
</details>

**Face Crops:** [AADHAR02_vs_USER_05_NO_MATCH/aadhaar_crop.jpg](AADHAR02_vs_USER_05_NO_MATCH/aadhaar_crop.jpg) | [AADHAR02_vs_USER_05_NO_MATCH/selfie_crop.jpg](AADHAR02_vs_USER_05_NO_MATCH/selfie_crop.jpg)

---

### 16. AADHAR02.jpg vs USER_06.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0517 |
| **Confidence** | 5.2% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3772 (score: 0.1267) |
| **SSIM** | 0.2458 |
| **Landmark Score** | 0.5601 |
| **Pose Diff** | 11.8 deg |
| **Fused Score** | 0.2057 |
| **Aadhaar Demographics** | M, age 35 |
| **Selfie Demographics** | M, age 45 |
| **Age Gap** | 10 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4)
  2. Cosine similarity: 0.0517 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 10yr gap → threshold relaxed by 0.050 (effective: match=0.550, uncertain=0.350)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 5.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 23873ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 120ms |
| enhancement_ms | 22652ms |
| clahe_ms | 50ms |
| face_processing_ms | 0ms |
| dual_path_ms | 524ms |
| similarity_ms | 526ms |
| **TOTAL** | **23873ms** |
</details>

**Face Crops:** [AADHAR02_vs_USER_06_NO_MATCH/aadhaar_crop.jpg](AADHAR02_vs_USER_06_NO_MATCH/aadhaar_crop.jpg) | [AADHAR02_vs_USER_06_NO_MATCH/selfie_crop.jpg](AADHAR02_vs_USER_06_NO_MATCH/selfie_crop.jpg)

---

### 17. AADHAR02.jpg vs USER_07.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1027 |
| **Confidence** | 10.3% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.3397 (score: 0.1341) |
| **SSIM** | 0.3573 |
| **Landmark Score** | 0.4911 |
| **Pose Diff** | 12.7 deg |
| **Fused Score** | 0.2284 |
| **Aadhaar Demographics** | M, age 35 |
| **Selfie Demographics** | M, age 38 |
| **Age Gap** | 3 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4), Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.1027 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar, Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 10.3% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 20983ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 167ms |
| enhancement_ms | 19228ms |
| clahe_ms | 80ms |
| face_processing_ms | 0ms |
| dual_path_ms | 753ms |
| similarity_ms | 755ms |
| **TOTAL** | **20983ms** |
</details>

**Face Crops:** [AADHAR02_vs_USER_07_NO_MATCH/aadhaar_crop.jpg](AADHAR02_vs_USER_07_NO_MATCH/aadhaar_crop.jpg) | [AADHAR02_vs_USER_07_NO_MATCH/selfie_crop.jpg](AADHAR02_vs_USER_07_NO_MATCH/selfie_crop.jpg)

---

### 18. AADHAR02.jpg vs USER_08.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1639 |
| **Confidence** | 16.4% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2931 (score: 0.1437) |
| **SSIM** | 0.1990 |
| **Landmark Score** | 0.4568 |
| **Pose Diff** | 25.6 deg |
| **Fused Score** | 0.2386 |
| **Aadhaar Demographics** | M, age 35 |
| **Selfie Demographics** | M, age 54 |
| **Age Gap** | 19 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4)
  2. Cosine similarity: 0.1639 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 19yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 16.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 23241ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 195ms |
| enhancement_ms | 21895ms |
| clahe_ms | 52ms |
| face_processing_ms | 0ms |
| dual_path_ms | 547ms |
| similarity_ms | 550ms |
| **TOTAL** | **23241ms** |
</details>

**Face Crops:** [AADHAR02_vs_USER_08_NO_MATCH/aadhaar_crop.jpg](AADHAR02_vs_USER_08_NO_MATCH/aadhaar_crop.jpg) | [AADHAR02_vs_USER_08_NO_MATCH/selfie_crop.jpg](AADHAR02_vs_USER_08_NO_MATCH/selfie_crop.jpg)

---

### 19. AADHAR02.jpg vs USER_09.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0822 |
| **Confidence** | 8.2% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 0.40 |
| **L2 Distance** | 1.3548 (score: 0.1310) |
| **SSIM** | 0.2411 |
| **Landmark Score** | 0.5983 |
| **Pose Diff** | 7.3 deg |
| **Fused Score** | 0.2320 |
| **Aadhaar Demographics** | M, age 35 |
| **Selfie Demographics** | M, age 79 |
| **Age Gap** | 44 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4)
  2. Cosine similarity: 0.0822 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 44yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 8.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 20562ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 135ms |
| enhancement_ms | 19381ms |
| clahe_ms | 47ms |
| face_processing_ms | 0ms |
| dual_path_ms | 498ms |
| similarity_ms | 500ms |
| **TOTAL** | **20562ms** |
</details>

**Face Crops:** [AADHAR02_vs_USER_09_NO_MATCH/aadhaar_crop.jpg](AADHAR02_vs_USER_09_NO_MATCH/aadhaar_crop.jpg) | [AADHAR02_vs_USER_09_NO_MATCH/selfie_crop.jpg](AADHAR02_vs_USER_09_NO_MATCH/selfie_crop.jpg)

---

### 20. AADHAR02.jpg vs USER_10.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1247 |
| **Confidence** | 12.5% |
| **Aadhaar Quality** | 0.40 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.3231 (score: 0.1374) |
| **SSIM** | 0.3695 |
| **Landmark Score** | 0.2855 |
| **Pose Diff** | 9.3 deg |
| **Fused Score** | 0.1907 |
| **Aadhaar Demographics** | M, age 33 |
| **Selfie Demographics** | M, age 21 |
| **Age Gap** | 12 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.40 < 0.4), Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.1247 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 12yr gap → threshold relaxed by 0.070 (effective: match=0.530, uncertain=0.330)
  3. Quality flag: LOW (Aadhaar, Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 12.5% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 18335ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 140ms |
| enhancement_ms | 17053ms |
| clahe_ms | 50ms |
| face_processing_ms | 0ms |
| dual_path_ms | 545ms |
| similarity_ms | 547ms |
| **TOTAL** | **18335ms** |
</details>

**Face Crops:** [AADHAR02_vs_USER_10_NO_MATCH/aadhaar_crop.jpg](AADHAR02_vs_USER_10_NO_MATCH/aadhaar_crop.jpg) | [AADHAR02_vs_USER_10_NO_MATCH/selfie_crop.jpg](AADHAR02_vs_USER_10_NO_MATCH/selfie_crop.jpg)

---

### 21. AADHAR03.jpg vs USER_01.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1454 |
| **Confidence** | 14.5% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3073 (score: 0.1407) |
| **SSIM** | 0.1894 |
| **Landmark Score** | 0.4290 |
| **Pose Diff** | 18.0 deg |
| **Fused Score** | 0.2202 |
| **Aadhaar Demographics** | F, age 36 |
| **Selfie Demographics** | M, age 30 |
| **Age Gap** | 6 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1454 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 6yr gap → threshold relaxed by 0.010 (effective: match=0.590, uncertain=0.390)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 14.5% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1853ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 114ms |
| enhancement_ms | 100ms |
| clahe_ms | 48ms |
| face_processing_ms | 458ms |
| dual_path_ms | 566ms |
| similarity_ms | 568ms |
| **TOTAL** | **1853ms** |
</details>

**Face Crops:** [AADHAR03_vs_USER_01_NO_MATCH/aadhaar_crop.jpg](AADHAR03_vs_USER_01_NO_MATCH/aadhaar_crop.jpg) | [AADHAR03_vs_USER_01_NO_MATCH/selfie_crop.jpg](AADHAR03_vs_USER_01_NO_MATCH/selfie_crop.jpg)

---

### 22. AADHAR03.jpg vs USER_02.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2570 |
| **Confidence** | 25.7% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.2191 (score: 0.1606) |
| **SSIM** | 0.3217 |
| **Landmark Score** | 0.5561 |
| **Pose Diff** | 8.7 deg |
| **Fused Score** | 0.3286 |
| **Aadhaar Demographics** | F, age 36 |
| **Selfie Demographics** | M, age 31 |
| **Age Gap** | 5 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.92, threshold=0.4)
  2. Cosine similarity: 0.2570 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 25.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1456ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 140ms |
| enhancement_ms | 113ms |
| clahe_ms | 49ms |
| face_processing_ms | 0ms |
| dual_path_ms | 576ms |
| similarity_ms | 577ms |
| **TOTAL** | **1456ms** |
</details>

**Face Crops:** [AADHAR03_vs_USER_02_NO_MATCH/aadhaar_crop.jpg](AADHAR03_vs_USER_02_NO_MATCH/aadhaar_crop.jpg) | [AADHAR03_vs_USER_02_NO_MATCH/selfie_crop.jpg](AADHAR03_vs_USER_02_NO_MATCH/selfie_crop.jpg)

---

### 23. AADHAR03.jpg vs USER_03.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1512 |
| **Confidence** | 15.1% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 1.3029 (score: 0.1417) |
| **SSIM** | 0.2462 |
| **Landmark Score** | 0.6365 |
| **Pose Diff** | 9.7 deg |
| **Fused Score** | 0.2811 |
| **Aadhaar Demographics** | F, age 36 |
| **Selfie Demographics** | F, age 28 |
| **Age Gap** | 8 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.67, threshold=0.4)
  2. Cosine similarity: 0.1512 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 15.1% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1290ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 131ms |
| enhancement_ms | 122ms |
| clahe_ms | 51ms |
| face_processing_ms | 0ms |
| dual_path_ms | 492ms |
| similarity_ms | 494ms |
| **TOTAL** | **1290ms** |
</details>

**Face Crops:** [AADHAR03_vs_USER_03_NO_MATCH/aadhaar_crop.jpg](AADHAR03_vs_USER_03_NO_MATCH/aadhaar_crop.jpg) | [AADHAR03_vs_USER_03_NO_MATCH/selfie_crop.jpg](AADHAR03_vs_USER_03_NO_MATCH/selfie_crop.jpg)

---

### 24. AADHAR03.jpg vs USER_04.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0712 |
| **Confidence** | 7.1% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.3630 (score: 0.1295) |
| **SSIM** | 0.4178 |
| **Landmark Score** | 0.4067 |
| **Pose Diff** | 5.0 deg |
| **Fused Score** | 0.1956 |
| **Aadhaar Demographics** | F, age 33 |
| **Selfie Demographics** | F, age 42 |
| **Age Gap** | 9 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.0712 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 9yr gap → threshold relaxed by 0.040 (effective: match=0.560, uncertain=0.360)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 7.1% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 7596ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 132ms |
| enhancement_ms | 6517ms |
| clahe_ms | 48ms |
| face_processing_ms | 0ms |
| dual_path_ms | 448ms |
| similarity_ms | 450ms |
| **TOTAL** | **7596ms** |
</details>

**Face Crops:** [AADHAR03_vs_USER_04_NO_MATCH/aadhaar_crop.jpg](AADHAR03_vs_USER_04_NO_MATCH/aadhaar_crop.jpg) | [AADHAR03_vs_USER_04_NO_MATCH/selfie_crop.jpg](AADHAR03_vs_USER_04_NO_MATCH/selfie_crop.jpg)

---

### 25. AADHAR03.jpg vs USER_05.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1873 |
| **Confidence** | 18.7% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2749 (score: 0.1477) |
| **SSIM** | 0.3586 |
| **Landmark Score** | 0.5349 |
| **Pose Diff** | 13.5 deg |
| **Fused Score** | 0.2874 |
| **Aadhaar Demographics** | F, age 33 |
| **Selfie Demographics** | F, age 25 |
| **Age Gap** | 8 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1873 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 18.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1303ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 126ms |
| enhancement_ms | 112ms |
| clahe_ms | 49ms |
| face_processing_ms | 0ms |
| dual_path_ms | 507ms |
| similarity_ms | 510ms |
| **TOTAL** | **1303ms** |
</details>

**Face Crops:** [AADHAR03_vs_USER_05_NO_MATCH/aadhaar_crop.jpg](AADHAR03_vs_USER_05_NO_MATCH/aadhaar_crop.jpg) | [AADHAR03_vs_USER_05_NO_MATCH/selfie_crop.jpg](AADHAR03_vs_USER_05_NO_MATCH/selfie_crop.jpg)

---

### 26. AADHAR03.jpg vs USER_06.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1859 |
| **Confidence** | 18.6% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2760 (score: 0.1475) |
| **SSIM** | 0.2687 |
| **Landmark Score** | 0.6214 |
| **Pose Diff** | 14.7 deg |
| **Fused Score** | 0.2992 |
| **Aadhaar Demographics** | F, age 36 |
| **Selfie Demographics** | M, age 45 |
| **Age Gap** | 9 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1859 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 9yr gap → threshold relaxed by 0.040 (effective: match=0.560, uncertain=0.360)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 18.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1190ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 123ms |
| enhancement_ms | 106ms |
| clahe_ms | 52ms |
| face_processing_ms | 0ms |
| dual_path_ms | 454ms |
| similarity_ms | 456ms |
| **TOTAL** | **1190ms** |
</details>

**Face Crops:** [AADHAR03_vs_USER_06_NO_MATCH/aadhaar_crop.jpg](AADHAR03_vs_USER_06_NO_MATCH/aadhaar_crop.jpg) | [AADHAR03_vs_USER_06_NO_MATCH/selfie_crop.jpg](AADHAR03_vs_USER_06_NO_MATCH/selfie_crop.jpg)

---

### 27. AADHAR03.jpg vs USER_07.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1483 |
| **Confidence** | 14.8% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.3052 (score: 0.1412) |
| **SSIM** | 0.4785 |
| **Landmark Score** | 0.5360 |
| **Pose Diff** | 9.6 deg |
| **Fused Score** | 0.2775 |
| **Aadhaar Demographics** | F, age 36 |
| **Selfie Demographics** | M, age 38 |
| **Age Gap** | 2 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.1483 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 14.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 7706ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 120ms |
| enhancement_ms | 6523ms |
| clahe_ms | 47ms |
| face_processing_ms | 0ms |
| dual_path_ms | 507ms |
| similarity_ms | 509ms |
| **TOTAL** | **7706ms** |
</details>

**Face Crops:** [AADHAR03_vs_USER_07_NO_MATCH/aadhaar_crop.jpg](AADHAR03_vs_USER_07_NO_MATCH/aadhaar_crop.jpg) | [AADHAR03_vs_USER_07_NO_MATCH/selfie_crop.jpg](AADHAR03_vs_USER_07_NO_MATCH/selfie_crop.jpg)

---

### 28. AADHAR03.jpg vs USER_08.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1968 |
| **Confidence** | 19.7% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2674 (score: 0.1494) |
| **SSIM** | 0.2392 |
| **Landmark Score** | 0.3880 |
| **Pose Diff** | 19.1 deg |
| **Fused Score** | 0.2441 |
| **Aadhaar Demographics** | F, age 36 |
| **Selfie Demographics** | M, age 54 |
| **Age Gap** | 18 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1968 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 18yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 19.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1182ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 127ms |
| enhancement_ms | 111ms |
| clahe_ms | 47ms |
| face_processing_ms | 0ms |
| dual_path_ms | 447ms |
| similarity_ms | 450ms |
| **TOTAL** | **1182ms** |
</details>

**Face Crops:** [AADHAR03_vs_USER_08_NO_MATCH/aadhaar_crop.jpg](AADHAR03_vs_USER_08_NO_MATCH/aadhaar_crop.jpg) | [AADHAR03_vs_USER_08_NO_MATCH/selfie_crop.jpg](AADHAR03_vs_USER_08_NO_MATCH/selfie_crop.jpg)

---

### 29. AADHAR03.jpg vs USER_09.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1237 |
| **Confidence** | 12.4% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.40 |
| **L2 Distance** | 1.3239 (score: 0.1373) |
| **SSIM** | 0.3182 |
| **Landmark Score** | 0.4759 |
| **Pose Diff** | 11.0 deg |
| **Fused Score** | 0.2326 |
| **Aadhaar Demographics** | F, age 36 |
| **Selfie Demographics** | M, age 79 |
| **Age Gap** | 43 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.40, threshold=0.4)
  2. Cosine similarity: 0.1237 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 43yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 12.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1301ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 135ms |
| enhancement_ms | 120ms |
| clahe_ms | 52ms |
| face_processing_ms | 0ms |
| dual_path_ms | 496ms |
| similarity_ms | 497ms |
| **TOTAL** | **1301ms** |
</details>

**Face Crops:** [AADHAR03_vs_USER_09_NO_MATCH/aadhaar_crop.jpg](AADHAR03_vs_USER_09_NO_MATCH/aadhaar_crop.jpg) | [AADHAR03_vs_USER_09_NO_MATCH/selfie_crop.jpg](AADHAR03_vs_USER_09_NO_MATCH/selfie_crop.jpg)

---

### 30. AADHAR03.jpg vs USER_10.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0930 |
| **Confidence** | 9.3% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.3469 (score: 0.1326) |
| **SSIM** | 0.3902 |
| **Landmark Score** | 0.3464 |
| **Pose Diff** | 6.2 deg |
| **Fused Score** | 0.1900 |
| **Aadhaar Demographics** | F, age 33 |
| **Selfie Demographics** | M, age 21 |
| **Age Gap** | 12 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.0930 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 12yr gap → threshold relaxed by 0.070 (effective: match=0.530, uncertain=0.330)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 9.3% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 7689ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 134ms |
| enhancement_ms | 6470ms |
| clahe_ms | 48ms |
| face_processing_ms | 0ms |
| dual_path_ms | 518ms |
| similarity_ms | 519ms |
| **TOTAL** | **7689ms** |
</details>

**Face Crops:** [AADHAR03_vs_USER_10_NO_MATCH/aadhaar_crop.jpg](AADHAR03_vs_USER_10_NO_MATCH/aadhaar_crop.jpg) | [AADHAR03_vs_USER_10_NO_MATCH/selfie_crop.jpg](AADHAR03_vs_USER_10_NO_MATCH/selfie_crop.jpg)

---

### 31. AADHAR04.jpg vs USER_01.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0484 |
| **Confidence** | 4.8% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3796 (score: 0.1263) |
| **SSIM** | 0.1998 |
| **Landmark Score** | 0.4881 |
| **Pose Diff** | 16.7 deg |
| **Fused Score** | 0.1813 |
| **Aadhaar Demographics** | F, age 29 |
| **Selfie Demographics** | M, age 30 |
| **Age Gap** | 1 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4)
  2. Cosine similarity: 0.0484 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 4.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 11972ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 97ms |
| enhancement_ms | 10252ms |
| clahe_ms | 48ms |
| face_processing_ms | 487ms |
| dual_path_ms | 544ms |
| similarity_ms | 545ms |
| **TOTAL** | **11972ms** |
</details>

**Face Crops:** [AADHAR04_vs_USER_01_NO_MATCH/aadhaar_crop.jpg](AADHAR04_vs_USER_01_NO_MATCH/aadhaar_crop.jpg) | [AADHAR04_vs_USER_01_NO_MATCH/selfie_crop.jpg](AADHAR04_vs_USER_01_NO_MATCH/selfie_crop.jpg)

---

### 32. AADHAR04.jpg vs USER_02.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0307 |
| **Confidence** | 3.1% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.3923 (score: 0.1239) |
| **SSIM** | 0.3366 |
| **Landmark Score** | 0.5661 |
| **Pose Diff** | 6.9 deg |
| **Fused Score** | 0.2045 |
| **Aadhaar Demographics** | F, age 29 |
| **Selfie Demographics** | M, age 31 |
| **Age Gap** | 2 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4)
  2. Cosine similarity: 0.0307 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 3.1% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 11652ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 130ms |
| enhancement_ms | 10406ms |
| clahe_ms | 47ms |
| face_processing_ms | 0ms |
| dual_path_ms | 533ms |
| similarity_ms | 536ms |
| **TOTAL** | **11652ms** |
</details>

**Face Crops:** [AADHAR04_vs_USER_02_NO_MATCH/aadhaar_crop.jpg](AADHAR04_vs_USER_02_NO_MATCH/aadhaar_crop.jpg) | [AADHAR04_vs_USER_02_NO_MATCH/selfie_crop.jpg](AADHAR04_vs_USER_02_NO_MATCH/selfie_crop.jpg)

---

### 33. AADHAR04.jpg vs USER_03.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1176 |
| **Confidence** | 11.8% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 1.3285 (score: 0.1363) |
| **SSIM** | 0.2862 |
| **Landmark Score** | 0.6236 |
| **Pose Diff** | 10.2 deg |
| **Fused Score** | 0.2628 |
| **Aadhaar Demographics** | F, age 29 |
| **Selfie Demographics** | F, age 28 |
| **Age Gap** | 1 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4)
  2. Cosine similarity: 0.1176 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 11.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 11375ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 135ms |
| enhancement_ms | 10321ms |
| clahe_ms | 46ms |
| face_processing_ms | 0ms |
| dual_path_ms | 435ms |
| similarity_ms | 438ms |
| **TOTAL** | **11375ms** |
</details>

**Face Crops:** [AADHAR04_vs_USER_03_NO_MATCH/aadhaar_crop.jpg](AADHAR04_vs_USER_03_NO_MATCH/aadhaar_crop.jpg) | [AADHAR04_vs_USER_03_NO_MATCH/selfie_crop.jpg](AADHAR04_vs_USER_03_NO_MATCH/selfie_crop.jpg)

---

### 34. AADHAR04.jpg vs USER_04.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0653 |
| **Confidence** | 6.5% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.3672 (score: 0.1286) |
| **SSIM** | 0.3953 |
| **Landmark Score** | 0.4497 |
| **Pose Diff** | 11.6 deg |
| **Fused Score** | 0.2008 |
| **Aadhaar Demographics** | F, age 29 |
| **Selfie Demographics** | F, age 42 |
| **Age Gap** | 13 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4), Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.0653 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 13yr gap → threshold relaxed by 0.080 (effective: match=0.520, uncertain=0.320)
  3. Quality flag: LOW (Aadhaar, Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 6.5% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 17855ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 127ms |
| enhancement_ms | 16557ms |
| clahe_ms | 47ms |
| face_processing_ms | 0ms |
| dual_path_ms | 562ms |
| similarity_ms | 562ms |
| **TOTAL** | **17855ms** |
</details>

**Face Crops:** [AADHAR04_vs_USER_04_NO_MATCH/aadhaar_crop.jpg](AADHAR04_vs_USER_04_NO_MATCH/aadhaar_crop.jpg) | [AADHAR04_vs_USER_04_NO_MATCH/selfie_crop.jpg](AADHAR04_vs_USER_04_NO_MATCH/selfie_crop.jpg)

---

### 35. AADHAR04.jpg vs USER_05.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1058 |
| **Confidence** | 10.6% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3373 (score: 0.1345) |
| **SSIM** | 0.3286 |
| **Landmark Score** | 0.6548 |
| **Pose Diff** | 14.2 deg |
| **Fused Score** | 0.2682 |
| **Aadhaar Demographics** | F, age 29 |
| **Selfie Demographics** | F, age 25 |
| **Age Gap** | 4 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4)
  2. Cosine similarity: 0.1058 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 10.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 11525ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 107ms |
| enhancement_ms | 10421ms |
| clahe_ms | 48ms |
| face_processing_ms | 0ms |
| dual_path_ms | 473ms |
| similarity_ms | 475ms |
| **TOTAL** | **11525ms** |
</details>

**Face Crops:** [AADHAR04_vs_USER_05_NO_MATCH/aadhaar_crop.jpg](AADHAR04_vs_USER_05_NO_MATCH/aadhaar_crop.jpg) | [AADHAR04_vs_USER_05_NO_MATCH/selfie_crop.jpg](AADHAR04_vs_USER_05_NO_MATCH/selfie_crop.jpg)

---

### 36. AADHAR04.jpg vs USER_06.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1176 |
| **Confidence** | 11.8% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3284 (score: 0.1363) |
| **SSIM** | 0.2167 |
| **Landmark Score** | 0.5838 |
| **Pose Diff** | 13.9 deg |
| **Fused Score** | 0.2460 |
| **Aadhaar Demographics** | F, age 31 |
| **Selfie Demographics** | M, age 45 |
| **Age Gap** | 14 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4)
  2. Cosine similarity: 0.1176 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 14yr gap → threshold relaxed by 0.090 (effective: match=0.510, uncertain=0.310)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 11.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 11673ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 123ms |
| enhancement_ms | 10530ms |
| clahe_ms | 45ms |
| face_processing_ms | 0ms |
| dual_path_ms | 486ms |
| similarity_ms | 488ms |
| **TOTAL** | **11673ms** |
</details>

**Face Crops:** [AADHAR04_vs_USER_06_NO_MATCH/aadhaar_crop.jpg](AADHAR04_vs_USER_06_NO_MATCH/aadhaar_crop.jpg) | [AADHAR04_vs_USER_06_NO_MATCH/selfie_crop.jpg](AADHAR04_vs_USER_06_NO_MATCH/selfie_crop.jpg)

---

### 37. AADHAR04.jpg vs USER_07.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0477 |
| **Confidence** | 4.8% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.3801 (score: 0.1262) |
| **SSIM** | 0.4445 |
| **Landmark Score** | 0.5496 |
| **Pose Diff** | 13.4 deg |
| **Fused Score** | 0.2207 |
| **Aadhaar Demographics** | F, age 29 |
| **Selfie Demographics** | M, age 38 |
| **Age Gap** | 9 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4), Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.0477 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 9yr gap → threshold relaxed by 0.040 (effective: match=0.560, uncertain=0.360)
  3. Quality flag: LOW (Aadhaar, Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 4.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 18055ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 137ms |
| enhancement_ms | 16786ms |
| clahe_ms | 52ms |
| face_processing_ms | 0ms |
| dual_path_ms | 539ms |
| similarity_ms | 542ms |
| **TOTAL** | **18055ms** |
</details>

**Face Crops:** [AADHAR04_vs_USER_07_NO_MATCH/aadhaar_crop.jpg](AADHAR04_vs_USER_07_NO_MATCH/aadhaar_crop.jpg) | [AADHAR04_vs_USER_07_NO_MATCH/selfie_crop.jpg](AADHAR04_vs_USER_07_NO_MATCH/selfie_crop.jpg)

---

### 38. AADHAR04.jpg vs USER_08.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0384 |
| **Confidence** | 3.8% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3868 (score: 0.1249) |
| **SSIM** | 0.2416 |
| **Landmark Score** | 0.4658 |
| **Pose Diff** | 22.5 deg |
| **Fused Score** | 0.1742 |
| **Aadhaar Demographics** | F, age 31 |
| **Selfie Demographics** | M, age 54 |
| **Age Gap** | 23 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4)
  2. Cosine similarity: 0.0384 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 23yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 3.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 11740ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 133ms |
| enhancement_ms | 10647ms |
| clahe_ms | 51ms |
| face_processing_ms | 0ms |
| dual_path_ms | 454ms |
| similarity_ms | 455ms |
| **TOTAL** | **11740ms** |
</details>

**Face Crops:** [AADHAR04_vs_USER_08_NO_MATCH/aadhaar_crop.jpg](AADHAR04_vs_USER_08_NO_MATCH/aadhaar_crop.jpg) | [AADHAR04_vs_USER_08_NO_MATCH/selfie_crop.jpg](AADHAR04_vs_USER_08_NO_MATCH/selfie_crop.jpg)

---

### 39. AADHAR04.jpg vs USER_09.jpg

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
| **Aadhaar Demographics** | F, age 29 |
| **Selfie Demographics** | M, age 79 |
| **Age Gap** | 50 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4)
  2. Cosine similarity: 0.0371 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 50yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Aadhaar below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 3.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 11894ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 142ms |
| enhancement_ms | 10756ms |
| clahe_ms | 50ms |
| face_processing_ms | 0ms |
| dual_path_ms | 471ms |
| similarity_ms | 473ms |
| **TOTAL** | **11894ms** |
</details>

**Face Crops:** [AADHAR04_vs_USER_09_NO_MATCH/aadhaar_crop.jpg](AADHAR04_vs_USER_09_NO_MATCH/aadhaar_crop.jpg) | [AADHAR04_vs_USER_09_NO_MATCH/selfie_crop.jpg](AADHAR04_vs_USER_09_NO_MATCH/selfie_crop.jpg)

---

### 40. AADHAR04.jpg vs USER_10.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0237 |
| **Confidence** | 2.4% |
| **Aadhaar Quality** | 0.21 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.3974 (score: 0.1229) |
| **SSIM** | 0.4011 |
| **Landmark Score** | 0.3191 |
| **Pose Diff** | 4.1 deg |
| **Fused Score** | 0.1452 |
| **Aadhaar Demographics** | F, age 29 |
| **Selfie Demographics** | M, age 21 |
| **Age Gap** | 8 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Aadhaar (quality 0.21 < 0.4), Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.0237 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: LOW (Aadhaar, Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 2.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 18586ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 128ms |
| enhancement_ms | 17416ms |
| clahe_ms | 53ms |
| face_processing_ms | 0ms |
| dual_path_ms | 494ms |
| similarity_ms | 496ms |
| **TOTAL** | **18586ms** |
</details>

**Face Crops:** [AADHAR04_vs_USER_10_NO_MATCH/aadhaar_crop.jpg](AADHAR04_vs_USER_10_NO_MATCH/aadhaar_crop.jpg) | [AADHAR04_vs_USER_10_NO_MATCH/selfie_crop.jpg](AADHAR04_vs_USER_10_NO_MATCH/selfie_crop.jpg)

---

### 41. AADHAR05.pdf vs USER_01.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0701 |
| **Confidence** | 7.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3638 (score: 0.1293) |
| **SSIM** | 0.1803 |
| **Landmark Score** | 0.3243 |
| **Pose Diff** | 14.6 deg |
| **Fused Score** | 0.1506 |
| **Aadhaar Demographics** | F, age 33 |
| **Selfie Demographics** | M, age 30 |
| **Age Gap** | 3 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.0701 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 7.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1726ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 162ms |
| enhancement_ms | 12ms |
| clahe_ms | 9ms |
| face_processing_ms | 453ms |
| dual_path_ms | 544ms |
| similarity_ms | 547ms |
| **TOTAL** | **1726ms** |
</details>

**Face Crops:** [AADHAR05_vs_USER_01_NO_MATCH/aadhaar_crop.jpg](AADHAR05_vs_USER_01_NO_MATCH/aadhaar_crop.jpg) | [AADHAR05_vs_USER_01_NO_MATCH/selfie_crop.jpg](AADHAR05_vs_USER_01_NO_MATCH/selfie_crop.jpg)

---

### 42. AADHAR05.pdf vs USER_02.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0925 |
| **Confidence** | 9.3% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.3472 (score: 0.1325) |
| **SSIM** | 0.2575 |
| **Landmark Score** | 0.3962 |
| **Pose Diff** | 10.2 deg |
| **Fused Score** | 0.1889 |
| **Aadhaar Demographics** | F, age 28 |
| **Selfie Demographics** | M, age 31 |
| **Age Gap** | 3 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.92, threshold=0.4)
  2. Cosine similarity: 0.0925 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 9.3% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1138ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 47ms |
| enhancement_ms | 26ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 528ms |
| similarity_ms | 529ms |
| **TOTAL** | **1138ms** |
</details>

**Face Crops:** [AADHAR05_vs_USER_02_NO_MATCH/aadhaar_crop.jpg](AADHAR05_vs_USER_02_NO_MATCH/aadhaar_crop.jpg) | [AADHAR05_vs_USER_02_NO_MATCH/selfie_crop.jpg](AADHAR05_vs_USER_02_NO_MATCH/selfie_crop.jpg)

---

### 43. AADHAR05.pdf vs USER_03.jpg

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
| **Aadhaar Demographics** | F, age 28 |
| **Selfie Demographics** | F, age 28 |
| **Age Gap** | 0 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.67, threshold=0.4)
  2. Cosine similarity: 0.6303 → MATCH zone (>= 0.6 match threshold)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score above threshold with good quality
  5. Final decision: MATCH at 63.0% confidence
     Reason: Score above threshold with good quality — confident match
```
</details>

<details><summary>Timings (total 986ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 34ms |
| enhancement_ms | 38ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 452ms |
| similarity_ms | 453ms |
| **TOTAL** | **986ms** |
</details>

**Face Crops:** [AADHAR05_vs_USER_03_MATCH/aadhaar_crop.jpg](AADHAR05_vs_USER_03_MATCH/aadhaar_crop.jpg) | [AADHAR05_vs_USER_03_MATCH/selfie_crop.jpg](AADHAR05_vs_USER_03_MATCH/selfie_crop.jpg)

---

### 44. AADHAR05.pdf vs USER_04.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0364 |
| **Confidence** | 3.6% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.3882 (score: 0.1246) |
| **SSIM** | 0.3708 |
| **Landmark Score** | 0.2751 |
| **Pose Diff** | 9.6 deg |
| **Fused Score** | 0.1384 |
| **Aadhaar Demographics** | F, age 28 |
| **Selfie Demographics** | F, age 42 |
| **Age Gap** | 14 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.0364 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 14yr gap → threshold relaxed by 0.090 (effective: match=0.510, uncertain=0.310)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 3.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 7490ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 43ms |
| enhancement_ms | 6506ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 465ms |
| similarity_ms | 466ms |
| **TOTAL** | **7490ms** |
</details>

**Face Crops:** [AADHAR05_vs_USER_04_NO_MATCH/aadhaar_crop.jpg](AADHAR05_vs_USER_04_NO_MATCH/aadhaar_crop.jpg) | [AADHAR05_vs_USER_04_NO_MATCH/selfie_crop.jpg](AADHAR05_vs_USER_04_NO_MATCH/selfie_crop.jpg)

---

### 45. AADHAR05.pdf vs USER_05.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0459 |
| **Confidence** | 4.6% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3814 (score: 0.1259) |
| **SSIM** | 0.2767 |
| **Landmark Score** | 0.4260 |
| **Pose Diff** | 21.6 deg |
| **Fused Score** | 0.1720 |
| **Aadhaar Demographics** | F, age 33 |
| **Selfie Demographics** | F, age 25 |
| **Age Gap** | 8 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.0459 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 4.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1087ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 46ms |
| enhancement_ms | 24ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 504ms |
| similarity_ms | 506ms |
| **TOTAL** | **1087ms** |
</details>

**Face Crops:** [AADHAR05_vs_USER_05_NO_MATCH/aadhaar_crop.jpg](AADHAR05_vs_USER_05_NO_MATCH/aadhaar_crop.jpg) | [AADHAR05_vs_USER_05_NO_MATCH/selfie_crop.jpg](AADHAR05_vs_USER_05_NO_MATCH/selfie_crop.jpg)

---

### 46. AADHAR05.pdf vs USER_06.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0799 |
| **Confidence** | 8.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3566 (score: 0.1307) |
| **SSIM** | 0.2293 |
| **Landmark Score** | 0.4225 |
| **Pose Diff** | 13.7 deg |
| **Fused Score** | 0.1855 |
| **Aadhaar Demographics** | F, age 33 |
| **Selfie Demographics** | M, age 45 |
| **Age Gap** | 12 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.0799 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 12yr gap → threshold relaxed by 0.070 (effective: match=0.530, uncertain=0.330)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 8.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1273ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 50ms |
| enhancement_ms | 27ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 593ms |
| similarity_ms | 595ms |
| **TOTAL** | **1273ms** |
</details>

**Face Crops:** [AADHAR05_vs_USER_06_NO_MATCH/aadhaar_crop.jpg](AADHAR05_vs_USER_06_NO_MATCH/aadhaar_crop.jpg) | [AADHAR05_vs_USER_06_NO_MATCH/selfie_crop.jpg](AADHAR05_vs_USER_06_NO_MATCH/selfie_crop.jpg)

---

### 47. AADHAR05.pdf vs USER_07.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0895 |
| **Confidence** | 9.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.3494 (score: 0.1321) |
| **SSIM** | 0.3544 |
| **Landmark Score** | 0.3814 |
| **Pose Diff** | 13.8 deg |
| **Fused Score** | 0.1932 |
| **Aadhaar Demographics** | F, age 33 |
| **Selfie Demographics** | M, age 38 |
| **Age Gap** | 5 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.0895 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 9.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 7633ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 44ms |
| enhancement_ms | 6579ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 499ms |
| similarity_ms | 502ms |
| **TOTAL** | **7633ms** |
</details>

**Face Crops:** [AADHAR05_vs_USER_07_NO_MATCH/aadhaar_crop.jpg](AADHAR05_vs_USER_07_NO_MATCH/aadhaar_crop.jpg) | [AADHAR05_vs_USER_07_NO_MATCH/selfie_crop.jpg](AADHAR05_vs_USER_07_NO_MATCH/selfie_crop.jpg)

---

### 48. AADHAR05.pdf vs USER_08.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1724 |
| **Confidence** | 17.2% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2865 (score: 0.1452) |
| **SSIM** | 0.1867 |
| **Landmark Score** | 0.2826 |
| **Pose Diff** | 25.5 deg |
| **Fused Score** | 0.1987 |
| **Aadhaar Demographics** | F, age 33 |
| **Selfie Demographics** | M, age 54 |
| **Age Gap** | 21 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1724 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 21yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 17.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1114ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 43ms |
| enhancement_ms | 32ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 514ms |
| similarity_ms | 517ms |
| **TOTAL** | **1114ms** |
</details>

**Face Crops:** [AADHAR05_vs_USER_08_NO_MATCH/aadhaar_crop.jpg](AADHAR05_vs_USER_08_NO_MATCH/aadhaar_crop.jpg) | [AADHAR05_vs_USER_08_NO_MATCH/selfie_crop.jpg](AADHAR05_vs_USER_08_NO_MATCH/selfie_crop.jpg)

---

### 49. AADHAR05.pdf vs USER_09.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0780 |
| **Confidence** | 7.8% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.40 |
| **L2 Distance** | 1.3579 (score: 0.1304) |
| **SSIM** | 0.2672 |
| **Landmark Score** | 0.3195 |
| **Pose Diff** | 8.2 deg |
| **Fused Score** | 0.1625 |
| **Aadhaar Demographics** | F, age 28 |
| **Selfie Demographics** | M, age 79 |
| **Age Gap** | 51 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.40, threshold=0.4)
  2. Cosine similarity: 0.0780 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 51yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 7.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1054ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 31ms |
| enhancement_ms | 30ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 491ms |
| similarity_ms | 494ms |
| **TOTAL** | **1054ms** |
</details>

**Face Crops:** [AADHAR05_vs_USER_09_NO_MATCH/aadhaar_crop.jpg](AADHAR05_vs_USER_09_NO_MATCH/aadhaar_crop.jpg) | [AADHAR05_vs_USER_09_NO_MATCH/selfie_crop.jpg](AADHAR05_vs_USER_09_NO_MATCH/selfie_crop.jpg)

---

### 50. AADHAR05.pdf vs USER_10.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0566 |
| **Confidence** | 5.7% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.3736 (score: 0.1274) |
| **SSIM** | 0.3415 |
| **Landmark Score** | 0.2060 |
| **Pose Diff** | 10.3 deg |
| **Fused Score** | 0.1295 |
| **Aadhaar Demographics** | F, age 33 |
| **Selfie Demographics** | M, age 21 |
| **Age Gap** | 12 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.0566 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 12yr gap → threshold relaxed by 0.070 (effective: match=0.530, uncertain=0.330)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 5.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 7636ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 31ms |
| enhancement_ms | 6656ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 470ms |
| similarity_ms | 471ms |
| **TOTAL** | **7636ms** |
</details>

**Face Crops:** [AADHAR05_vs_USER_10_NO_MATCH/aadhaar_crop.jpg](AADHAR05_vs_USER_10_NO_MATCH/aadhaar_crop.jpg) | [AADHAR05_vs_USER_10_NO_MATCH/selfie_crop.jpg](AADHAR05_vs_USER_10_NO_MATCH/selfie_crop.jpg)

---

### 51. AADHAR06.pdf vs USER_01.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2274 |
| **Confidence** | 22.7% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2430 (score: 0.1550) |
| **SSIM** | 0.1418 |
| **Landmark Score** | 0.3539 |
| **Pose Diff** | 14.1 deg |
| **Fused Score** | 0.2432 |
| **Aadhaar Demographics** | M, age 38 |
| **Selfie Demographics** | M, age 30 |
| **Age Gap** | 8 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.2274 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 22.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1578ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 28ms |
| enhancement_ms | 16ms |
| clahe_ms | 8ms |
| face_processing_ms | 430ms |
| dual_path_ms | 547ms |
| similarity_ms | 549ms |
| **TOTAL** | **1578ms** |
</details>

**Face Crops:** [AADHAR06_vs_USER_01_NO_MATCH/aadhaar_crop.jpg](AADHAR06_vs_USER_01_NO_MATCH/aadhaar_crop.jpg) | [AADHAR06_vs_USER_01_NO_MATCH/selfie_crop.jpg](AADHAR06_vs_USER_01_NO_MATCH/selfie_crop.jpg)

---

### 52. AADHAR06.pdf vs USER_02.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.3732 |
| **Confidence** | 27.3% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.1197 (score: 0.1865) |
| **SSIM** | 0.2199 |
| **Landmark Score** | 0.4095 |
| **Pose Diff** | 12.5 deg |
| **Fused Score** | 0.3483 |
| **Aadhaar Demographics** | M, age 39 |
| **Selfie Demographics** | M, age 31 |
| **Age Gap** | 8 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.92, threshold=0.4)
  2. Cosine similarity: 0.3732 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 27.3% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1102ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 39ms |
| enhancement_ms | 28ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 512ms |
| similarity_ms | 515ms |
| **TOTAL** | **1102ms** |
</details>

**Face Crops:** [AADHAR06_vs_USER_02_NO_MATCH/aadhaar_crop.jpg](AADHAR06_vs_USER_02_NO_MATCH/aadhaar_crop.jpg) | [AADHAR06_vs_USER_02_NO_MATCH/selfie_crop.jpg](AADHAR06_vs_USER_02_NO_MATCH/selfie_crop.jpg)

---

### 53. AADHAR06.pdf vs USER_03.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0960 |
| **Confidence** | 9.6% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 1.3446 (score: 0.1331) |
| **SSIM** | 0.1713 |
| **Landmark Score** | 0.5934 |
| **Pose Diff** | 9.6 deg |
| **Fused Score** | 0.2316 |
| **Aadhaar Demographics** | M, age 38 |
| **Selfie Demographics** | F, age 28 |
| **Age Gap** | 10 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.67, threshold=0.4)
  2. Cosine similarity: 0.0960 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 10yr gap → threshold relaxed by 0.050 (effective: match=0.550, uncertain=0.350)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 9.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1150ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 52ms |
| enhancement_ms | 32ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 528ms |
| similarity_ms | 530ms |
| **TOTAL** | **1150ms** |
</details>

**Face Crops:** [AADHAR06_vs_USER_03_NO_MATCH/aadhaar_crop.jpg](AADHAR06_vs_USER_03_NO_MATCH/aadhaar_crop.jpg) | [AADHAR06_vs_USER_03_NO_MATCH/selfie_crop.jpg](AADHAR06_vs_USER_03_NO_MATCH/selfie_crop.jpg)

---

### 54. AADHAR06.pdf vs USER_04.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0000 |
| **Confidence** | 0.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.4341 (score: 0.1163) |
| **SSIM** | 0.3034 |
| **Landmark Score** | 0.2652 |
| **Pose Diff** | 12.1 deg |
| **Fused Score** | 0.1083 |
| **Aadhaar Demographics** | M, age 38 |
| **Selfie Demographics** | F, age 42 |
| **Age Gap** | 4 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.0000 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 0.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 7353ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 37ms |
| enhancement_ms | 6316ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 494ms |
| similarity_ms | 496ms |
| **TOTAL** | **7353ms** |
</details>

**Face Crops:** [AADHAR06_vs_USER_04_NO_MATCH/aadhaar_crop.jpg](AADHAR06_vs_USER_04_NO_MATCH/aadhaar_crop.jpg) | [AADHAR06_vs_USER_04_NO_MATCH/selfie_crop.jpg](AADHAR06_vs_USER_04_NO_MATCH/selfie_crop.jpg)

---

### 55. AADHAR06.pdf vs USER_05.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1722 |
| **Confidence** | 17.2% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2867 (score: 0.1451) |
| **SSIM** | 0.2372 |
| **Landmark Score** | 0.3973 |
| **Pose Diff** | 24.6 deg |
| **Fused Score** | 0.2323 |
| **Aadhaar Demographics** | M, age 39 |
| **Selfie Demographics** | F, age 25 |
| **Age Gap** | 14 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1722 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 14yr gap → threshold relaxed by 0.090 (effective: match=0.510, uncertain=0.310)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 17.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1013ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 44ms |
| enhancement_ms | 22ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 468ms |
| similarity_ms | 470ms |
| **TOTAL** | **1013ms** |
</details>

**Face Crops:** [AADHAR06_vs_USER_05_NO_MATCH/aadhaar_crop.jpg](AADHAR06_vs_USER_05_NO_MATCH/aadhaar_crop.jpg) | [AADHAR06_vs_USER_05_NO_MATCH/selfie_crop.jpg](AADHAR06_vs_USER_05_NO_MATCH/selfie_crop.jpg)

---

### 56. AADHAR06.pdf vs USER_06.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1824 |
| **Confidence** | 18.2% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2787 (score: 0.1469) |
| **SSIM** | 0.2076 |
| **Landmark Score** | 0.4227 |
| **Pose Diff** | 14.6 deg |
| **Fused Score** | 0.2415 |
| **Aadhaar Demographics** | M, age 39 |
| **Selfie Demographics** | M, age 45 |
| **Age Gap** | 6 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1824 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 6yr gap → threshold relaxed by 0.010 (effective: match=0.590, uncertain=0.390)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 18.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1175ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 44ms |
| enhancement_ms | 34ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 543ms |
| similarity_ms | 545ms |
| **TOTAL** | **1175ms** |
</details>

**Face Crops:** [AADHAR06_vs_USER_06_NO_MATCH/aadhaar_crop.jpg](AADHAR06_vs_USER_06_NO_MATCH/aadhaar_crop.jpg) | [AADHAR06_vs_USER_06_NO_MATCH/selfie_crop.jpg](AADHAR06_vs_USER_06_NO_MATCH/selfie_crop.jpg)

---

### 57. AADHAR06.pdf vs USER_07.jpg

| Metric | Value |
|--------|-------|
| **Result** | MATCH |
| **Cosine Score** | 0.5986 |
| **Confidence** | 67.9% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 0.8960 (score: 0.2608) |
| **SSIM** | 0.3271 |
| **Landmark Score** | 0.3785 |
| **Pose Diff** | 15.6 deg |
| **Fused Score** | 0.4826 |
| **Aadhaar Demographics** | M, age 38 |
| **Selfie Demographics** | M, age 38 |
| **Age Gap** | 0 years |
| **Gender** | Consistent |
| **VLM Verdict** | Same person |
| **VLM Reasoning** | The eye socket shape, inter-pupillary distance, and nose bridge width are consistent, indicating the same bone structure. |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.5986 → UNCERTAIN zone (between 0.4 and 0.6)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Invoked — cosine score in uncertain zone → VLM decides
     VLM verdict: SAME PERSON
  5. Final decision: MATCH at 67.9% confidence
     Confidence breakdown: base 59.9% → +8 VLM confirmation
     Reason: Score in uncertain zone, but VLM confirmed same person
```
</details>

<details><summary>Timings (total 26780ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 48ms |
| enhancement_ms | 6579ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 522ms |
| similarity_ms | 524ms |
| vlm_ms | 19098ms |
| **TOTAL** | **26780ms** |
</details>

**Face Crops:** [AADHAR06_vs_USER_07_MATCH/aadhaar_crop.jpg](AADHAR06_vs_USER_07_MATCH/aadhaar_crop.jpg) | [AADHAR06_vs_USER_07_MATCH/selfie_crop.jpg](AADHAR06_vs_USER_07_MATCH/selfie_crop.jpg)

---

### 58. AADHAR06.pdf vs USER_08.jpg

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
| **Aadhaar Demographics** | M, age 38 |
| **Selfie Demographics** | M, age 54 |
| **Age Gap** | 16 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.6161 → MATCH zone (>= 0.6 match threshold)
  2b. Age-gap relaxation: 16yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score above threshold with good quality
  5. Final decision: MATCH at 61.6% confidence
     Reason: Score above threshold with good quality — confident match
```
</details>

<details><summary>Timings (total 1068ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 38ms |
| enhancement_ms | 46ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 487ms |
| similarity_ms | 488ms |
| **TOTAL** | **1068ms** |
</details>

**Face Crops:** [AADHAR06_vs_USER_08_MATCH/aadhaar_crop.jpg](AADHAR06_vs_USER_08_MATCH/aadhaar_crop.jpg) | [AADHAR06_vs_USER_08_MATCH/selfie_crop.jpg](AADHAR06_vs_USER_08_MATCH/selfie_crop.jpg)

---

### 59. AADHAR06.pdf vs USER_09.jpg

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
| **Aadhaar Demographics** | M, age 38 |
| **Selfie Demographics** | M, age 79 |
| **Age Gap** | 41 years |
| **Gender** | Consistent |
| **VLM Verdict** | Same person |
| **VLM Reasoning** | The eye socket shape, inter-pupillary distance, and nose bridge width are consistent, indicating the same bone structure. |

<details><summary>Decision Trace</summary>

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
</details>

<details><summary>Timings (total 28068ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 28ms |
| enhancement_ms | 33ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 485ms |
| similarity_ms | 486ms |
| vlm_ms | 27028ms |
| **TOTAL** | **28068ms** |
</details>

**Face Crops:** [AADHAR06_vs_USER_09_MATCH/aadhaar_crop.jpg](AADHAR06_vs_USER_09_MATCH/aadhaar_crop.jpg) | [AADHAR06_vs_USER_09_MATCH/selfie_crop.jpg](AADHAR06_vs_USER_09_MATCH/selfie_crop.jpg)

---

### 60. AADHAR06.pdf vs USER_10.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2322 |
| **Confidence** | 23.2% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.2392 (score: 0.1559) |
| **SSIM** | 0.3185 |
| **Landmark Score** | 0.2036 |
| **Pose Diff** | 12.4 deg |
| **Fused Score** | 0.2260 |
| **Aadhaar Demographics** | M, age 38 |
| **Selfie Demographics** | M, age 21 |
| **Age Gap** | 17 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.2322 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 17yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 23.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 6857ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 38ms |
| enhancement_ms | 5891ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 459ms |
| similarity_ms | 461ms |
| **TOTAL** | **6857ms** |
</details>

**Face Crops:** [AADHAR06_vs_USER_10_NO_MATCH/aadhaar_crop.jpg](AADHAR06_vs_USER_10_NO_MATCH/aadhaar_crop.jpg) | [AADHAR06_vs_USER_10_NO_MATCH/selfie_crop.jpg](AADHAR06_vs_USER_10_NO_MATCH/selfie_crop.jpg)

---

### 61. AADHAR07.pdf vs USER_01.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0551 |
| **Confidence** | 5.5% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3747 (score: 0.1272) |
| **SSIM** | 0.1951 |
| **Landmark Score** | 0.3235 |
| **Pose Diff** | 8.0 deg |
| **Fused Score** | 0.1434 |
| **Aadhaar Demographics** | M, age 24 |
| **Selfie Demographics** | M, age 30 |
| **Age Gap** | 6 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.0551 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 6yr gap → threshold relaxed by 0.010 (effective: match=0.590, uncertain=0.390)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 5.5% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1661ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 13ms |
| enhancement_ms | 22ms |
| clahe_ms | 11ms |
| face_processing_ms | 427ms |
| dual_path_ms | 593ms |
| similarity_ms | 595ms |
| **TOTAL** | **1661ms** |
</details>

**Face Crops:** [AADHAR07_vs_USER_01_NO_MATCH/aadhaar_crop.jpg](AADHAR07_vs_USER_01_NO_MATCH/aadhaar_crop.jpg) | [AADHAR07_vs_USER_01_NO_MATCH/selfie_crop.jpg](AADHAR07_vs_USER_01_NO_MATCH/selfie_crop.jpg)

---

### 62. AADHAR07.pdf vs USER_02.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2092 |
| **Confidence** | 20.9% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.2576 (score: 0.1516) |
| **SSIM** | 0.2561 |
| **Landmark Score** | 0.4230 |
| **Pose Diff** | 2.9 deg |
| **Fused Score** | 0.2616 |
| **Aadhaar Demographics** | M, age 24 |
| **Selfie Demographics** | M, age 31 |
| **Age Gap** | 7 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.92, threshold=0.4)
  2. Cosine similarity: 0.2092 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 7yr gap → threshold relaxed by 0.020 (effective: match=0.580, uncertain=0.380)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 20.9% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 984ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 22ms |
| enhancement_ms | 32ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 460ms |
| similarity_ms | 462ms |
| **TOTAL** | **984ms** |
</details>

**Face Crops:** [AADHAR07_vs_USER_02_NO_MATCH/aadhaar_crop.jpg](AADHAR07_vs_USER_02_NO_MATCH/aadhaar_crop.jpg) | [AADHAR07_vs_USER_02_NO_MATCH/selfie_crop.jpg](AADHAR07_vs_USER_02_NO_MATCH/selfie_crop.jpg)

---

### 63. AADHAR07.pdf vs USER_03.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1662 |
| **Confidence** | 16.6% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 1.2913 (score: 0.1441) |
| **SSIM** | 0.2482 |
| **Landmark Score** | 0.6098 |
| **Pose Diff** | 2.0 deg |
| **Fused Score** | 0.2831 |
| **Aadhaar Demographics** | F, age 25 |
| **Selfie Demographics** | F, age 28 |
| **Age Gap** | 3 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.67, threshold=0.4)
  2. Cosine similarity: 0.1662 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 16.6% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1017ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 26ms |
| enhancement_ms | 29ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 476ms |
| similarity_ms | 478ms |
| **TOTAL** | **1017ms** |
</details>

**Face Crops:** [AADHAR07_vs_USER_03_NO_MATCH/aadhaar_crop.jpg](AADHAR07_vs_USER_03_NO_MATCH/aadhaar_crop.jpg) | [AADHAR07_vs_USER_03_NO_MATCH/selfie_crop.jpg](AADHAR07_vs_USER_03_NO_MATCH/selfie_crop.jpg)

---

### 64. AADHAR07.pdf vs USER_04.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0646 |
| **Confidence** | 6.5% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.3678 (score: 0.1285) |
| **SSIM** | 0.3131 |
| **Landmark Score** | 0.2874 |
| **Pose Diff** | 15.0 deg |
| **Fused Score** | 0.1515 |
| **Aadhaar Demographics** | F, age 25 |
| **Selfie Demographics** | F, age 42 |
| **Age Gap** | 17 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.0646 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 17yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 6.5% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 6618ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 43ms |
| enhancement_ms | 5602ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 481ms |
| similarity_ms | 483ms |
| **TOTAL** | **6618ms** |
</details>

**Face Crops:** [AADHAR07_vs_USER_04_NO_MATCH/aadhaar_crop.jpg](AADHAR07_vs_USER_04_NO_MATCH/aadhaar_crop.jpg) | [AADHAR07_vs_USER_04_NO_MATCH/selfie_crop.jpg](AADHAR07_vs_USER_04_NO_MATCH/selfie_crop.jpg)

---

### 65. AADHAR07.pdf vs USER_05.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2239 |
| **Confidence** | 22.4% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2459 (score: 0.1543) |
| **SSIM** | 0.2745 |
| **Landmark Score** | 0.4373 |
| **Pose Diff** | 22.4 deg |
| **Fused Score** | 0.2753 |
| **Aadhaar Demographics** | F, age 25 |
| **Selfie Demographics** | F, age 25 |
| **Age Gap** | 0 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.2239 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 22.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 940ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 33ms |
| enhancement_ms | 25ms |
| clahe_ms | 7ms |
| face_processing_ms | 0ms |
| dual_path_ms | 436ms |
| similarity_ms | 437ms |
| **TOTAL** | **940ms** |
</details>

**Face Crops:** [AADHAR07_vs_USER_05_NO_MATCH/aadhaar_crop.jpg](AADHAR07_vs_USER_05_NO_MATCH/aadhaar_crop.jpg) | [AADHAR07_vs_USER_05_NO_MATCH/selfie_crop.jpg](AADHAR07_vs_USER_05_NO_MATCH/selfie_crop.jpg)

---

### 66. AADHAR07.pdf vs USER_06.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2841 |
| **Confidence** | 28.4% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.1966 (score: 0.1661) |
| **SSIM** | 0.2291 |
| **Landmark Score** | 0.4122 |
| **Pose Diff** | 6.2 deg |
| **Fused Score** | 0.2988 |
| **Aadhaar Demographics** | F, age 25 |
| **Selfie Demographics** | M, age 45 |
| **Age Gap** | 20 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.2841 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 20yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 28.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1118ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 48ms |
| enhancement_ms | 26ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 518ms |
| similarity_ms | 518ms |
| **TOTAL** | **1118ms** |
</details>

**Face Crops:** [AADHAR07_vs_USER_06_NO_MATCH/aadhaar_crop.jpg](AADHAR07_vs_USER_06_NO_MATCH/aadhaar_crop.jpg) | [AADHAR07_vs_USER_06_NO_MATCH/selfie_crop.jpg](AADHAR07_vs_USER_06_NO_MATCH/selfie_crop.jpg)

---

### 67. AADHAR07.pdf vs USER_07.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2082 |
| **Confidence** | 20.8% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.2584 (score: 0.1514) |
| **SSIM** | 0.3330 |
| **Landmark Score** | 0.3344 |
| **Pose Diff** | 13.8 deg |
| **Fused Score** | 0.2466 |
| **Aadhaar Demographics** | F, age 25 |
| **Selfie Demographics** | M, age 38 |
| **Age Gap** | 13 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.2082 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 13yr gap → threshold relaxed by 0.080 (effective: match=0.520, uncertain=0.320)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 20.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 6804ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 29ms |
| enhancement_ms | 5748ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 509ms |
| similarity_ms | 510ms |
| **TOTAL** | **6804ms** |
</details>

**Face Crops:** [AADHAR07_vs_USER_07_NO_MATCH/aadhaar_crop.jpg](AADHAR07_vs_USER_07_NO_MATCH/aadhaar_crop.jpg) | [AADHAR07_vs_USER_07_NO_MATCH/selfie_crop.jpg](AADHAR07_vs_USER_07_NO_MATCH/selfie_crop.jpg)

---

### 68. AADHAR07.pdf vs USER_08.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2035 |
| **Confidence** | 20.3% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2622 (score: 0.1506) |
| **SSIM** | 0.1983 |
| **Landmark Score** | 0.2741 |
| **Pose Diff** | 28.5 deg |
| **Fused Score** | 0.2153 |
| **Aadhaar Demographics** | F, age 25 |
| **Selfie Demographics** | M, age 54 |
| **Age Gap** | 29 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.2035 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 29yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 20.3% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1075ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 38ms |
| enhancement_ms | 33ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 497ms |
| similarity_ms | 498ms |
| **TOTAL** | **1075ms** |
</details>

**Face Crops:** [AADHAR07_vs_USER_08_NO_MATCH/aadhaar_crop.jpg](AADHAR07_vs_USER_08_NO_MATCH/aadhaar_crop.jpg) | [AADHAR07_vs_USER_08_NO_MATCH/selfie_crop.jpg](AADHAR07_vs_USER_08_NO_MATCH/selfie_crop.jpg)

---

### 69. AADHAR07.pdf vs USER_09.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1893 |
| **Confidence** | 18.9% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.40 |
| **L2 Distance** | 1.2733 (score: 0.1481) |
| **SSIM** | 0.2141 |
| **Landmark Score** | 0.3157 |
| **Pose Diff** | 10.9 deg |
| **Fused Score** | 0.2193 |
| **Aadhaar Demographics** | F, age 25 |
| **Selfie Demographics** | M, age 79 |
| **Age Gap** | 54 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.40, threshold=0.4)
  2. Cosine similarity: 0.1893 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 54yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 18.9% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 944ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 32ms |
| enhancement_ms | 28ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 437ms |
| similarity_ms | 440ms |
| **TOTAL** | **944ms** |
</details>

**Face Crops:** [AADHAR07_vs_USER_09_NO_MATCH/aadhaar_crop.jpg](AADHAR07_vs_USER_09_NO_MATCH/aadhaar_crop.jpg) | [AADHAR07_vs_USER_09_NO_MATCH/selfie_crop.jpg](AADHAR07_vs_USER_09_NO_MATCH/selfie_crop.jpg)

---

### 70. AADHAR07.pdf vs USER_10.jpg

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
| **Aadhaar Demographics** | M, age 24 |
| **Selfie Demographics** | M, age 21 |
| **Age Gap** | 3 years |
| **Gender** | Consistent |
| **VLM Verdict** | Different person |
| **VLM Reasoning** | Bone structure differences in eye socket shape and inter-pupillary distance indicate a mismatch. |

<details><summary>Decision Trace</summary>

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
</details>

<details><summary>Timings (total 26093ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 32ms |
| enhancement_ms | 5864ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 480ms |
| similarity_ms | 481ms |
| vlm_ms | 19228ms |
| **TOTAL** | **26093ms** |
</details>

**Face Crops:** [AADHAR07_vs_USER_10_NO_MATCH/aadhaar_crop.jpg](AADHAR07_vs_USER_10_NO_MATCH/aadhaar_crop.jpg) | [AADHAR07_vs_USER_10_NO_MATCH/selfie_crop.jpg](AADHAR07_vs_USER_10_NO_MATCH/selfie_crop.jpg)

---

### 71. AADHAR08.pdf vs USER_01.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1281 |
| **Confidence** | 12.8% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3206 (score: 0.1380) |
| **SSIM** | 0.2886 |
| **Landmark Score** | 0.2898 |
| **Pose Diff** | 5.9 deg |
| **Fused Score** | 0.1855 |
| **Aadhaar Demographics** | F, age 21 |
| **Selfie Demographics** | M, age 30 |
| **Age Gap** | 9 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1281 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 9yr gap → threshold relaxed by 0.040 (effective: match=0.560, uncertain=0.360)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 12.8% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 2032ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 21ms |
| enhancement_ms | 22ms |
| clahe_ms | 12ms |
| face_processing_ms | 552ms |
| dual_path_ms | 711ms |
| similarity_ms | 713ms |
| **TOTAL** | **2032ms** |
</details>

**Face Crops:** [AADHAR08_vs_USER_01_NO_MATCH/aadhaar_crop.jpg](AADHAR08_vs_USER_01_NO_MATCH/aadhaar_crop.jpg) | [AADHAR08_vs_USER_01_NO_MATCH/selfie_crop.jpg](AADHAR08_vs_USER_01_NO_MATCH/selfie_crop.jpg)

---

### 72. AADHAR08.pdf vs USER_02.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1939 |
| **Confidence** | 19.4% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.2697 (score: 0.1489) |
| **SSIM** | 0.3148 |
| **Landmark Score** | 0.3714 |
| **Pose Diff** | 13.8 deg |
| **Fused Score** | 0.2459 |
| **Aadhaar Demographics** | F, age 21 |
| **Selfie Demographics** | M, age 31 |
| **Age Gap** | 10 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.92, threshold=0.4)
  2. Cosine similarity: 0.1939 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 10yr gap → threshold relaxed by 0.050 (effective: match=0.550, uncertain=0.350)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 19.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1268ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 42ms |
| enhancement_ms | 33ms |
| clahe_ms | 11ms |
| face_processing_ms | 0ms |
| dual_path_ms | 590ms |
| similarity_ms | 591ms |
| **TOTAL** | **1268ms** |
</details>

**Face Crops:** [AADHAR08_vs_USER_02_NO_MATCH/aadhaar_crop.jpg](AADHAR08_vs_USER_02_NO_MATCH/aadhaar_crop.jpg) | [AADHAR08_vs_USER_02_NO_MATCH/selfie_crop.jpg](AADHAR08_vs_USER_02_NO_MATCH/selfie_crop.jpg)

---

### 73. AADHAR08.pdf vs USER_03.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2529 |
| **Confidence** | 25.3% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 1.2224 (score: 0.1598) |
| **SSIM** | 0.3077 |
| **Landmark Score** | 0.5398 |
| **Pose Diff** | 13.5 deg |
| **Fused Score** | 0.3208 |
| **Aadhaar Demographics** | F, age 21 |
| **Selfie Demographics** | F, age 28 |
| **Age Gap** | 7 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.67, threshold=0.4)
  2. Cosine similarity: 0.2529 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 7yr gap → threshold relaxed by 0.020 (effective: match=0.580, uncertain=0.380)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 25.3% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1121ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 53ms |
| enhancement_ms | 37ms |
| clahe_ms | 10ms |
| face_processing_ms | 0ms |
| dual_path_ms | 510ms |
| similarity_ms | 511ms |
| **TOTAL** | **1121ms** |
</details>

**Face Crops:** [AADHAR08_vs_USER_03_NO_MATCH/aadhaar_crop.jpg](AADHAR08_vs_USER_03_NO_MATCH/aadhaar_crop.jpg) | [AADHAR08_vs_USER_03_NO_MATCH/selfie_crop.jpg](AADHAR08_vs_USER_03_NO_MATCH/selfie_crop.jpg)

---

### 74. AADHAR08.pdf vs USER_04.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1620 |
| **Confidence** | 16.2% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 1.2946 (score: 0.1434) |
| **SSIM** | 0.3505 |
| **Landmark Score** | 0.2753 |
| **Pose Diff** | 26.7 deg |
| **Fused Score** | 0.2073 |
| **Aadhaar Demographics** | F, age 21 |
| **Selfie Demographics** | F, age 42 |
| **Age Gap** | 21 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.1620 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 21yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 16.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 6512ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 46ms |
| enhancement_ms | 5489ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 484ms |
| similarity_ms | 486ms |
| **TOTAL** | **6512ms** |
</details>

**Face Crops:** [AADHAR08_vs_USER_04_NO_MATCH/aadhaar_crop.jpg](AADHAR08_vs_USER_04_NO_MATCH/aadhaar_crop.jpg) | [AADHAR08_vs_USER_04_NO_MATCH/selfie_crop.jpg](AADHAR08_vs_USER_04_NO_MATCH/selfie_crop.jpg)

---

### 75. AADHAR08.pdf vs USER_05.jpg

| Metric | Value |
|--------|-------|
| **Result** | MATCH |
| **Cosine Score** | 0.5615 |
| **Confidence** | 64.1% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 0.9365 (score: 0.2454) |
| **SSIM** | 0.4157 |
| **Landmark Score** | 0.3644 |
| **Pose Diff** | 33.3 deg |
| **Fused Score** | 0.4660 |
| **Aadhaar Demographics** | F, age 22 |
| **Selfie Demographics** | F, age 25 |
| **Age Gap** | 3 years |
| **Gender** | Consistent |
| **VLM Verdict** | Same person |
| **VLM Reasoning** | The eye socket shape, inter-pupillary distance, and nose bridge width are consistent, indicating the same bone structure. |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.5615 → UNCERTAIN zone (between 0.4 and 0.6)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Invoked — cosine score in uncertain zone → VLM decides
     VLM verdict: SAME PERSON
  5. Final decision: MATCH at 64.1% confidence
     Confidence breakdown: base 56.1% → +8 VLM confirmation
     Reason: Score in uncertain zone, but VLM confirmed same person
```
</details>

<details><summary>Timings (total 20824ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 33ms |
| enhancement_ms | 25ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 504ms |
| similarity_ms | 506ms |
| vlm_ms | 19747ms |
| **TOTAL** | **20824ms** |
</details>

**Face Crops:** [AADHAR08_vs_USER_05_MATCH/aadhaar_crop.jpg](AADHAR08_vs_USER_05_MATCH/aadhaar_crop.jpg) | [AADHAR08_vs_USER_05_MATCH/selfie_crop.jpg](AADHAR08_vs_USER_05_MATCH/selfie_crop.jpg)

---

### 76. AADHAR08.pdf vs USER_06.jpg

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
| **Aadhaar Demographics** | F, age 22 |
| **Selfie Demographics** | M, age 45 |
| **Age Gap** | 23 years |
| **Gender** | MISMATCH |
| **VLM Verdict** | Same person |
| **VLM Reasoning** | The eye socket shape, inter-pupillary distance, and nose bridge width are consistent, indicating the same bone structure. |

<details><summary>Decision Trace</summary>

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
</details>

<details><summary>Timings (total 29276ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 60ms |
| enhancement_ms | 38ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 531ms |
| similarity_ms | 533ms |
| vlm_ms | 28103ms |
| **TOTAL** | **29276ms** |
</details>

**Face Crops:** [AADHAR08_vs_USER_06_MATCH/aadhaar_crop.jpg](AADHAR08_vs_USER_06_MATCH/aadhaar_crop.jpg) | [AADHAR08_vs_USER_06_MATCH/selfie_crop.jpg](AADHAR08_vs_USER_06_MATCH/selfie_crop.jpg)

---

### 77. AADHAR08.pdf vs USER_07.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1710 |
| **Confidence** | 17.1% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.2876 (score: 0.1449) |
| **SSIM** | 0.4699 |
| **Landmark Score** | 0.3018 |
| **Pose Diff** | 25.2 deg |
| **Fused Score** | 0.2310 |
| **Aadhaar Demographics** | F, age 22 |
| **Selfie Demographics** | M, age 38 |
| **Age Gap** | 16 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.1710 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 16yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 17.1% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 6779ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 56ms |
| enhancement_ms | 5770ms |
| clahe_ms | 14ms |
| face_processing_ms | 0ms |
| dual_path_ms | 468ms |
| similarity_ms | 471ms |
| **TOTAL** | **6779ms** |
</details>

**Face Crops:** [AADHAR08_vs_USER_07_NO_MATCH/aadhaar_crop.jpg](AADHAR08_vs_USER_07_NO_MATCH/aadhaar_crop.jpg) | [AADHAR08_vs_USER_07_NO_MATCH/selfie_crop.jpg](AADHAR08_vs_USER_07_NO_MATCH/selfie_crop.jpg)

---

### 78. AADHAR08.pdf vs USER_08.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1804 |
| **Confidence** | 18.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2803 (score: 0.1465) |
| **SSIM** | 0.2580 |
| **Landmark Score** | 0.2587 |
| **Pose Diff** | 40.2 deg |
| **Fused Score** | 0.2043 |
| **Aadhaar Demographics** | F, age 21 |
| **Selfie Demographics** | M, age 54 |
| **Age Gap** | 33 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1804 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 33yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 18.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1109ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 37ms |
| enhancement_ms | 50ms |
| clahe_ms | 13ms |
| face_processing_ms | 0ms |
| dual_path_ms | 504ms |
| similarity_ms | 505ms |
| **TOTAL** | **1109ms** |
</details>

**Face Crops:** [AADHAR08_vs_USER_08_NO_MATCH/aadhaar_crop.jpg](AADHAR08_vs_USER_08_NO_MATCH/aadhaar_crop.jpg) | [AADHAR08_vs_USER_08_NO_MATCH/selfie_crop.jpg](AADHAR08_vs_USER_08_NO_MATCH/selfie_crop.jpg)

---

### 79. AADHAR08.pdf vs USER_09.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1704 |
| **Confidence** | 17.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.40 |
| **L2 Distance** | 1.2881 (score: 0.1448) |
| **SSIM** | 0.3471 |
| **Landmark Score** | 0.2730 |
| **Pose Diff** | 21.1 deg |
| **Fused Score** | 0.2112 |
| **Aadhaar Demographics** | F, age 22 |
| **Selfie Demographics** | M, age 79 |
| **Age Gap** | 57 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.40, threshold=0.4)
  2. Cosine similarity: 0.1704 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 57yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 17.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1016ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 39ms |
| enhancement_ms | 37ms |
| clahe_ms | 13ms |
| face_processing_ms | 0ms |
| dual_path_ms | 462ms |
| similarity_ms | 465ms |
| **TOTAL** | **1016ms** |
</details>

**Face Crops:** [AADHAR08_vs_USER_09_NO_MATCH/aadhaar_crop.jpg](AADHAR08_vs_USER_09_NO_MATCH/aadhaar_crop.jpg) | [AADHAR08_vs_USER_09_NO_MATCH/selfie_crop.jpg](AADHAR08_vs_USER_09_NO_MATCH/selfie_crop.jpg)

---

### 80. AADHAR08.pdf vs USER_10.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.2137 |
| **Confidence** | 21.4% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.2540 (score: 0.1524) |
| **SSIM** | 0.4504 |
| **Landmark Score** | 0.2170 |
| **Pose Diff** | 16.8 deg |
| **Fused Score** | 0.2321 |
| **Aadhaar Demographics** | F, age 22 |
| **Selfie Demographics** | M, age 21 |
| **Age Gap** | 1 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.2137 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 21.4% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 6467ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 51ms |
| enhancement_ms | 5424ms |
| clahe_ms | 11ms |
| face_processing_ms | 0ms |
| dual_path_ms | 489ms |
| similarity_ms | 492ms |
| **TOTAL** | **6467ms** |
</details>

**Face Crops:** [AADHAR08_vs_USER_10_NO_MATCH/aadhaar_crop.jpg](AADHAR08_vs_USER_10_NO_MATCH/aadhaar_crop.jpg) | [AADHAR08_vs_USER_10_NO_MATCH/selfie_crop.jpg](AADHAR08_vs_USER_10_NO_MATCH/selfie_crop.jpg)

---

### 81. AADHAR09.pdf vs USER_01.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0753 |
| **Confidence** | 7.5% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3599 (score: 0.1300) |
| **SSIM** | 0.1392 |
| **Landmark Score** | 0.5759 |
| **Pose Diff** | 14.6 deg |
| **Fused Score** | 0.2123 |
| **Aadhaar Demographics** | M, age 39 |
| **Selfie Demographics** | M, age 30 |
| **Age Gap** | 9 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.0753 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 9yr gap → threshold relaxed by 0.040 (effective: match=0.560, uncertain=0.360)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 7.5% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1524ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 17ms |
| enhancement_ms | 22ms |
| clahe_ms | 10ms |
| face_processing_ms | 466ms |
| dual_path_ms | 504ms |
| similarity_ms | 506ms |
| **TOTAL** | **1524ms** |
</details>

**Face Crops:** [AADHAR09_vs_USER_01_NO_MATCH/aadhaar_crop.jpg](AADHAR09_vs_USER_01_NO_MATCH/aadhaar_crop.jpg) | [AADHAR09_vs_USER_01_NO_MATCH/selfie_crop.jpg](AADHAR09_vs_USER_01_NO_MATCH/selfie_crop.jpg)

---

### 82. AADHAR09.pdf vs USER_02.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1469 |
| **Confidence** | 14.7% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.92 |
| **L2 Distance** | 1.3062 (score: 0.1410) |
| **SSIM** | 0.2074 |
| **Landmark Score** | 0.7729 |
| **Pose Diff** | 8.1 deg |
| **Fused Score** | 0.3089 |
| **Aadhaar Demographics** | M, age 39 |
| **Selfie Demographics** | M, age 31 |
| **Age Gap** | 8 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.92, threshold=0.4)
  2. Cosine similarity: 0.1469 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 8yr gap → threshold relaxed by 0.030 (effective: match=0.570, uncertain=0.370)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 14.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1004ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 41ms |
| enhancement_ms | 22ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 466ms |
| similarity_ms | 466ms |
| **TOTAL** | **1004ms** |
</details>

**Face Crops:** [AADHAR09_vs_USER_02_NO_MATCH/aadhaar_crop.jpg](AADHAR09_vs_USER_02_NO_MATCH/aadhaar_crop.jpg) | [AADHAR09_vs_USER_02_NO_MATCH/selfie_crop.jpg](AADHAR09_vs_USER_02_NO_MATCH/selfie_crop.jpg)

---

### 83. AADHAR09.pdf vs USER_03.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1099 |
| **Confidence** | 11.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.67 |
| **L2 Distance** | 1.3342 (score: 0.1352) |
| **SSIM** | 0.2105 |
| **Landmark Score** | 0.6601 |
| **Pose Diff** | 8.9 deg |
| **Fused Score** | 0.2600 |
| **Aadhaar Demographics** | M, age 31 |
| **Selfie Demographics** | F, age 28 |
| **Age Gap** | 3 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.67, threshold=0.4)
  2. Cosine similarity: 0.1099 → NO MATCH zone (< 0.4 uncertain threshold)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 11.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1060ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 48ms |
| enhancement_ms | 26ms |
| clahe_ms | 9ms |
| face_processing_ms | 0ms |
| dual_path_ms | 488ms |
| similarity_ms | 489ms |
| **TOTAL** | **1060ms** |
</details>

**Face Crops:** [AADHAR09_vs_USER_03_NO_MATCH/aadhaar_crop.jpg](AADHAR09_vs_USER_03_NO_MATCH/aadhaar_crop.jpg) | [AADHAR09_vs_USER_03_NO_MATCH/selfie_crop.jpg](AADHAR09_vs_USER_03_NO_MATCH/selfie_crop.jpg)

---

### 84. AADHAR09.pdf vs USER_04.jpg

| Metric | Value |
|--------|-------|
| **Result** | MATCH |
| **Cosine Score** | 0.6337 |
| **Confidence** | 66.4% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.18 |
| **L2 Distance** | 0.8560 (score: 0.2769) |
| **SSIM** | 0.2814 |
| **Landmark Score** | 0.4999 |
| **Pose Diff** | 9.0 deg |
| **Fused Score** | 0.5293 |
| **Aadhaar Demographics** | M, age 39 |
| **Selfie Demographics** | F, age 42 |
| **Age Gap** | 3 years |
| **Gender** | MISMATCH |
| **VLM Verdict** | Same person |
| **VLM Reasoning** | The eye socket shape, inter-pupillary distance, and nose bridge width and profile are consistent, indicating the same bone structure. |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.18 < 0.4)
  2. Cosine similarity: 0.6337 → MATCH zone (>= 0.6 match threshold)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Invoked — high cosine score but low image quality → double-checking
     VLM verdict: SAME PERSON
  5. Final decision: MATCH at 66.4% confidence
     Confidence breakdown: base 63.4% → +8 VLM confirmation → -5 quality penalty
     Reason: Score above threshold, VLM confirmed despite low quality images
```
</details>

<details><summary>Timings (total 25644ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 38ms |
| enhancement_ms | 5545ms |
| clahe_ms | 12ms |
| face_processing_ms | 0ms |
| dual_path_ms | 411ms |
| similarity_ms | 412ms |
| vlm_ms | 19226ms |
| **TOTAL** | **25644ms** |
</details>

**Face Crops:** [AADHAR09_vs_USER_04_MATCH/aadhaar_crop.jpg](AADHAR09_vs_USER_04_MATCH/aadhaar_crop.jpg) | [AADHAR09_vs_USER_04_MATCH/selfie_crop.jpg](AADHAR09_vs_USER_04_MATCH/selfie_crop.jpg)

---

### 85. AADHAR09.pdf vs USER_05.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0000 |
| **Confidence** | 0.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.4423 (score: 0.1149) |
| **SSIM** | 0.2708 |
| **Landmark Score** | 0.7751 |
| **Pose Diff** | 19.0 deg |
| **Fused Score** | 0.2323 |
| **Aadhaar Demographics** | M, age 31 |
| **Selfie Demographics** | F, age 25 |
| **Age Gap** | 6 years |
| **Gender** | MISMATCH |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.0000 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 6yr gap → threshold relaxed by 0.010 (effective: match=0.590, uncertain=0.390)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 0.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1250ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 55ms |
| enhancement_ms | 42ms |
| clahe_ms | 10ms |
| face_processing_ms | 0ms |
| dual_path_ms | 570ms |
| similarity_ms | 572ms |
| **TOTAL** | **1250ms** |
</details>

**Face Crops:** [AADHAR09_vs_USER_05_NO_MATCH/aadhaar_crop.jpg](AADHAR09_vs_USER_05_NO_MATCH/aadhaar_crop.jpg) | [AADHAR09_vs_USER_05_NO_MATCH/selfie_crop.jpg](AADHAR09_vs_USER_05_NO_MATCH/selfie_crop.jpg)

---

### 86. AADHAR09.pdf vs USER_06.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1303 |
| **Confidence** | 13.0% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.3188 (score: 0.1383) |
| **SSIM** | 0.2312 |
| **Landmark Score** | 0.6166 |
| **Pose Diff** | 14.8 deg |
| **Fused Score** | 0.2628 |
| **Aadhaar Demographics** | M, age 31 |
| **Selfie Demographics** | M, age 45 |
| **Age Gap** | 14 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1303 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 14yr gap → threshold relaxed by 0.090 (effective: match=0.510, uncertain=0.310)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 13.0% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 1322ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 38ms |
| enhancement_ms | 40ms |
| clahe_ms | 10ms |
| face_processing_ms | 0ms |
| dual_path_ms | 617ms |
| similarity_ms | 618ms |
| **TOTAL** | **1322ms** |
</details>

**Face Crops:** [AADHAR09_vs_USER_06_NO_MATCH/aadhaar_crop.jpg](AADHAR09_vs_USER_06_NO_MATCH/aadhaar_crop.jpg) | [AADHAR09_vs_USER_06_NO_MATCH/selfie_crop.jpg](AADHAR09_vs_USER_06_NO_MATCH/selfie_crop.jpg)

---

### 87. AADHAR09.pdf vs USER_07.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0052 |
| **Confidence** | 0.5% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.15 |
| **L2 Distance** | 1.4105 (score: 0.1205) |
| **SSIM** | 0.3442 |
| **Landmark Score** | 0.6707 |
| **Pose Diff** | 15.3 deg |
| **Fused Score** | 0.2170 |
| **Aadhaar Demographics** | M, age 31 |
| **Selfie Demographics** | M, age 38 |
| **Age Gap** | 7 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.15 < 0.4)
  2. Cosine similarity: 0.0052 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 7yr gap → threshold relaxed by 0.020 (effective: match=0.580, uncertain=0.380)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 0.5% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 7080ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 44ms |
| enhancement_ms | 5980ms |
| clahe_ms | 8ms |
| face_processing_ms | 0ms |
| dual_path_ms | 523ms |
| similarity_ms | 525ms |
| **TOTAL** | **7080ms** |
</details>

**Face Crops:** [AADHAR09_vs_USER_07_NO_MATCH/aadhaar_crop.jpg](AADHAR09_vs_USER_07_NO_MATCH/aadhaar_crop.jpg) | [AADHAR09_vs_USER_07_NO_MATCH/selfie_crop.jpg](AADHAR09_vs_USER_07_NO_MATCH/selfie_crop.jpg)

---

### 88. AADHAR09.pdf vs USER_08.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.1670 |
| **Confidence** | 16.7% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 1.00 |
| **L2 Distance** | 1.2907 (score: 0.1443) |
| **SSIM** | 0.1909 |
| **Landmark Score** | 0.5128 |
| **Pose Diff** | 25.2 deg |
| **Fused Score** | 0.2536 |
| **Aadhaar Demographics** | M, age 31 |
| **Selfie Demographics** | M, age 54 |
| **Age Gap** | 23 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=1.00, threshold=0.4)
  2. Cosine similarity: 0.1670 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 23yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 16.7% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 2029ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 51ms |
| enhancement_ms | 41ms |
| clahe_ms | 10ms |
| face_processing_ms | 0ms |
| dual_path_ms | 962ms |
| similarity_ms | 965ms |
| **TOTAL** | **2029ms** |
</details>

**Face Crops:** [AADHAR09_vs_USER_08_NO_MATCH/aadhaar_crop.jpg](AADHAR09_vs_USER_08_NO_MATCH/aadhaar_crop.jpg) | [AADHAR09_vs_USER_08_NO_MATCH/selfie_crop.jpg](AADHAR09_vs_USER_08_NO_MATCH/selfie_crop.jpg)

---

### 89. AADHAR09.pdf vs USER_09.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0519 |
| **Confidence** | 5.2% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.40 |
| **L2 Distance** | 1.3771 (score: 0.1267) |
| **SSIM** | 0.2482 |
| **Landmark Score** | 0.5530 |
| **Pose Diff** | 12.9 deg |
| **Fused Score** | 0.2043 |
| **Aadhaar Demographics** | M, age 31 |
| **Selfie Demographics** | M, age 79 |
| **Age Gap** | 48 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Skipped — both images above quality threshold (Aadhaar=1.00, Selfie=0.40, threshold=0.4)
  2. Cosine similarity: 0.0519 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 48yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: OK (both images above 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 5.2% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 4034ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 106ms |
| enhancement_ms | 50ms |
| clahe_ms | 94ms |
| face_processing_ms | 0ms |
| dual_path_ms | 1890ms |
| similarity_ms | 1893ms |
| **TOTAL** | **4034ms** |
</details>

**Face Crops:** [AADHAR09_vs_USER_09_NO_MATCH/aadhaar_crop.jpg](AADHAR09_vs_USER_09_NO_MATCH/aadhaar_crop.jpg) | [AADHAR09_vs_USER_09_NO_MATCH/selfie_crop.jpg](AADHAR09_vs_USER_09_NO_MATCH/selfie_crop.jpg)

---

### 90. AADHAR09.pdf vs USER_10.jpg

| Metric | Value |
|--------|-------|
| **Result** | NO MATCH |
| **Cosine Score** | 0.0091 |
| **Confidence** | 0.9% |
| **Aadhaar Quality** | 1.00 |
| **Selfie Quality** | 0.13 |
| **L2 Distance** | 1.4077 (score: 0.1210) |
| **SSIM** | 0.2653 |
| **Landmark Score** | 0.3443 |
| **Pose Diff** | 7.2 deg |
| **Fused Score** | 0.1297 |
| **Aadhaar Demographics** | M, age 39 |
| **Selfie Demographics** | M, age 21 |
| **Age Gap** | 18 years |
| **Gender** | Consistent |

<details><summary>Decision Trace</summary>

```
  1. Enhancement: Applied Real-ESRGAN to Selfie (quality 0.13 < 0.4)
  2. Cosine similarity: 0.0091 → NO MATCH zone (< 0.4 uncertain threshold)
  2b. Age-gap relaxation: 18yr gap → threshold relaxed by 0.100 (effective: match=0.500, uncertain=0.300)
  3. Quality flag: LOW (Selfie below 0.4 threshold)
  4. VLM guard: Not needed — score below uncertain zone (definite no-match)
  5. Final decision: NO MATCH at 0.9% confidence
     Reason: Score below 0.4 — definite no-match, VLM not needed
```
</details>

<details><summary>Timings (total 8807ms)</summary>

| Stage | Time |
|-------|------|
| load_ms | 76ms |
| enhancement_ms | 6526ms |
| clahe_ms | 14ms |
| face_processing_ms | 0ms |
| dual_path_ms | 1094ms |
| similarity_ms | 1096ms |
| **TOTAL** | **8807ms** |
</details>

**Face Crops:** [AADHAR09_vs_USER_10_NO_MATCH/aadhaar_crop.jpg](AADHAR09_vs_USER_10_NO_MATCH/aadhaar_crop.jpg) | [AADHAR09_vs_USER_10_NO_MATCH/selfie_crop.jpg](AADHAR09_vs_USER_10_NO_MATCH/selfie_crop.jpg)

---

## Pipeline Configuration

| Setting | Value |
|---------|-------|
| Match threshold | 0.6 |
| Uncertain zone | 0.4 - 0.6 |
| Age gap threshold | 5 years |
| Max age relaxation | 0.1 |
| CLAHE | Enabled (clip=2.0, tile=8) |
| Flip augment (TTA) | Enabled |
| Dual-path | Enabled |
| Grayscale normalize | Disabled |
| VLM model | qwen2.5vl:7b |
| VLM confirmation bonus | +8.0 |
| Age gap VLM bonus | +5.0 |
