# Recent Conversation Compact — v3 False-Negative Reduction

## Primary Request & Intent
A real same-person pair (Aadhaar 40yr vs selfie 37yr — clearly the same man, mustache + beard) was rejected on SageMaker:
- Match: False, Confidence: 43.5%, Cosine: 0.5351, Fused: 0.4730
- VLM: "eye socket shapes and IPD differ"

User: "the model is not able to detect, think about how can we improve the scenario."
Confirmed ground truth = same person, risk tolerance = reduce false negatives, scope = Tier 1 + 2 + 3.

## Root Causes Identified
1. Age gap threshold stuck at 5yr (gap only 3yr) → no relaxation
2. VLM over-strict on printed-card IPD / eye-socket geometry
3. Hard VLM override: `-20%` regardless of cosine strength
4. Fused 0.4730 < cosine 0.5351: landmark/L2/SSIM dragged score down on low-quality input
5. Real-ESRGAN enhancement gate (quality < 0.4) may skip Aadhaar cards

## Tier 1 — Config & Fusion Tuning
- `age_gap_threshold`: 5 → 3
- `age_gap_relaxation_per_year`: 0.01 → 0.015
- `max_age_gap_relaxation`: 0.10 → 0.12
- `vlm_rejection_above_threshold`: -20 → -12
- `vlm_rejection_uncertain`: -10 → -5
- `vlm_confirmation_bonus`: 8 → 10
- New: `vlm_soft_override_cosine: 0.50`, `vlm_soft_override_penalty: -5.0` — when cosine ≥ 0.50 + VLM=false in match zone, apply soft -5 and keep MATCH instead of hard -20/false
- `quality_weighted_fusion: true` — at quality<0.3 weights shift to cosine=0.80/landmark=0.10/L2=0.07/SSIM=0.03

## Tier 2 — Preprocessing + VLM Prompt
- `enhancement.force_enhance_aadhaar: true` — Real-ESRGAN always runs on Aadhaar crop regardless of quality score
- `preprocessing.histogram_matching: true` — Aadhaar histogram matched to selfie via per-channel CDF `np.interp` (in `utils/image_utils.py`)
- Rewrote `VLM_PROMPT` in `pipeline/vlm_guard.py`: explicitly names printed-card distortion; instructs to IGNORE exact IPD, eye-socket spacing, pixel-level landmarks; lists stable cues (face shape, nose shape, eyebrows, moles, facial hair, ear shape, hairline); "when ambiguous, prefer same_person=true"
- Age-gap supplement now triggers at `age_gap > 2` (was > 3)

## Tier 3 — antelopev2 Ensemble
- New `pipeline/secondary_face.py`: `SecondaryFaceEmbedder` loads antelopev2 (glintr100 ArcFace, Glint360K), reuses buffalo_l's aligned 112×112 crop to extract a secondary embedding
- `similarity.ensemble_cosine(cosines, strategy, secondary_weight)`: supports `max | mean | weighted`
- Orchestrator runs both models per face → ensemble cosine used downstream
- `scripts/download_models.py` now has `download_antelopev2()` + `--skip-secondary` flag
- config: `face.enable_ensemble`, `secondary_model`, `ensemble_strategy`, `secondary_weight`

## Files Modified
- `config.yaml` — all new thresholds/flags
- `pipeline/orchestrator.py` — soft-override in `_fuse_decision()`, histogram-matching stage, ensemble wiring
- `pipeline/similarity.py` — `ensemble_cosine()` + new `get_quality_adjusted_weights()`
- `pipeline/enhancement.py` — `force_enhance_aadhaar` path, `source=` arg
- `pipeline/vlm_guard.py` — rewritten prompt
- `pipeline/secondary_face.py` — new file
- `utils/image_utils.py` — `match_histogram()` helper
- `scripts/download_models.py` — antelopev2 download
- `tests/conftest.py` — updated fixtures
- `tests/test_orchestrator_unit.py` — soft-override tests (5 cases)
- `tests/test_similarity.py` — ensemble_cosine (7) + quality weights (4)
- `tests/test_image_utils.py` — `TestMatchHistogram` (5)
- `tests/test_enhancement.py` — relaxed assertion to match new log format
- `tests/test_new_features.py` — updated expected weights for v3 quality-weighted fusion

## Test Status
`pytest tests/ -m "not integration"` → **259 passed, 2 deselected**

## Verification Plan
1. `git pull` on SageMaker → re-run Step 5 (downloads antelopev2, ~350MB extra)
2. Re-run the rejected pair (04_ip.pdf vs 04_PHOTO.pdf) → expect MATCH with fused ≥ 0.55
3. Batch run pairs.csv → same-person pairs should improve without new false positives on impostors
4. Decision trace should show: soft-override applied, ensemble cosine per model, quality-weighted fusion weights active

## Commit Strategy
- Tier 1 commit: config + fusion tuning
- Tier 2 commit: force-enhance + histogram matching + prompt
- Tier 3 commit: antelopev2 ensemble
- Docs commit: CLAUDE.md + compact.md
