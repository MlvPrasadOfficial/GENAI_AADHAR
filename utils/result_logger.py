"""Log each pipeline run to a timestamped subfolder in logs/.

Single run:
    logs/2026-04-04_22-22-25_NO_MATCH_a1b2c3d4/
        result.txt, aadhaar_crop.jpg, selfie_crop.jpg

Batch run (multiple Aadhaar-selfie pairs):
    logs/batch_2026-04-04_22-22-25/
        summary.txt
        AADHAR001_vs_USER_01_NO_MATCH/
            result.txt, aadhaar_crop.jpg, selfie_crop.jpg
        AADHAR02_vs_USER_01_NO_MATCH/
            result.txt, aadhaar_crop.jpg, selfie_crop.jpg
"""

import hashlib
from datetime import datetime
from pathlib import Path

import cv2


def _age_comparison(aadhaar_age: int, selfie_age: int) -> str:
    """Return a human-readable age comparison between Aadhaar and selfie faces."""
    diff = selfie_age - aadhaar_age
    abs_diff = abs(diff)
    if abs_diff <= 2:
        return "Ages consistent (within 2 years)"
    elif diff > 0:
        return f"Aadhaar photo appears ~{abs_diff}yr YOUNGER than selfie (older Aadhaar card likely)"
    else:
        return f"Aadhaar photo appears ~{abs_diff}yr OLDER than selfie (unusual — verify document)"


def _gender_match_note(aadhaar_gender: str, selfie_gender: str) -> str:
    """Return a note if genders don't match."""
    if aadhaar_gender == selfie_gender:
        return "Gender: consistent"
    return f"Gender MISMATCH: Aadhaar={aadhaar_gender}, Selfie={selfie_gender}"


def _metrics_lines(result) -> list[str]:
    """Build similarity metrics section lines from a PipelineResult."""
    lines = [
        "--- Similarity Metrics ---",
        f"Cosine:         {result.cosine_score:.4f}",
        f"L2 Distance:    {getattr(result, 'l2_distance', 0):.4f}  (score: {getattr(result, 'l2_score', 0):.4f})",
        f"SSIM:           {getattr(result, 'ssim', 0):.4f}",
    ]
    lmk = getattr(result, 'landmark_score', -1)
    lines.append(f"Landmark Geom:  {lmk:.4f}" + (" (unavailable)" if lmk < 0 else ""))
    pose = getattr(result, 'pose_diff', -1)
    lines.append(f"Pose Diff:      {pose:.1f} deg" + (" (unavailable)" if pose < 0 else ""))
    lines.append(f"Fused Score:    {getattr(result, 'fused_score', 0):.4f}")
    return lines


def _demographics_lines(result) -> list[str]:
    """Build demographics section lines from a PipelineResult."""
    a_g = getattr(result, "aadhaar_gender", "unknown")
    a_a = getattr(result, "aadhaar_age", 0)
    s_g = getattr(result, "selfie_gender", "unknown")
    s_a = getattr(result, "selfie_age", 0)

    lines = [
        f"--- Demographics ---",
        f"Aadhaar: Gender={a_g}, Age={a_a}",
        f"Selfie:  Gender={s_g}, Age={s_a}",
        f"  {_age_comparison(a_a, s_a)}",
        f"  {_gender_match_note(a_g, s_g)}",
    ]
    return lines


def log_result(
    result,
    aadhaar_path: str,
    selfie_path: str,
    config: dict | None = None,
    log_dir: str = "logs",
) -> Path:
    """Write a human-readable summary + face crops to a per-run subfolder.

    Args:
        result: PipelineResult dataclass from the orchestrator.
        aadhaar_path: Path to the Aadhaar image that was processed.
        selfie_path: Path to the selfie image that was processed.
        config: Pipeline config dict (for threshold values in the trace).
        log_dir: Root directory for log folders (created if missing).

    Returns:
        Path to the run folder.
    """
    now = datetime.now()
    status = "MATCH" if result.match else "NO_MATCH"
    if result.error:
        status = "ERROR"

    # Short hash from input paths + timestamp for deduplication
    hash_input = f"{aadhaar_path}:{selfie_path}:{now.isoformat()}".encode()
    short_hash = hashlib.md5(hash_input).hexdigest()[:8]

    folder_name = f"{now.strftime('%Y-%m-%d_%H-%M-%S')}_{status}_{short_hash}"
    run_dir = Path(log_dir) / folder_name
    run_dir.mkdir(parents=True, exist_ok=True)

    total_ms = sum(result.stage_timings.values()) if result.stage_timings else 0

    lines = [
        f"Aadhaar KYC Face Matching — Run Log",
        f"{'=' * 50}",
        f"Timestamp:      {now.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Aadhaar Image:  {aadhaar_path}",
        f"Selfie Image:   {selfie_path}",
        f"",
        f"--- Result ---",
        f"Match:          {'YES' if result.match else 'NO'}",
        f"Confidence:     {result.confidence_pct:.1f}%",
        f"Cosine Score:   {result.cosine_score:.4f}",
        f"",
        *_metrics_lines(result),
        f"",
        f"--- Quality ---",
        f"Aadhaar Quality: {result.aadhaar_quality:.2f}",
        f"Selfie Quality:  {result.selfie_quality:.2f}",
        f"",
        *_demographics_lines(result),
        f"",
        f"--- VLM Guard ---",
        f"VLM Same Person: {result.vlm_same_person}",
        f"VLM Reasoning:   {result.vlm_reasoning or 'N/A'}",
        f"",
        f"--- Decision Trace ---",
    ]

    lines.extend(_build_decision_trace(result, config))

    lines.append(f"")
    lines.append(f"--- Timings ---")

    for stage, ms in result.stage_timings.items():
        lines.append(f"  {stage:.<30s} {ms:.0f} ms")
    lines.append(f"  {'TOTAL':.<30s} {total_ms:.0f} ms")

    if result.error:
        lines.extend([
            f"",
            f"--- Error ---",
            f"{result.error}",
        ])

    # Save face crop images
    crop_lines = _save_face_crops(result, run_dir)
    if crop_lines:
        lines.append(f"")
        lines.append(f"--- Face Crops ---")
        lines.extend(crop_lines)

    lines.append(f"{'=' * 50}")

    (run_dir / "result.txt").write_text("\n".join(lines), encoding="utf-8")

    # Also write a README.md for visual reading
    _write_single_readme(run_dir, result, aadhaar_path, selfie_path, config)

    return run_dir


def _write_single_readme(
    run_dir: Path,
    result,
    aadhaar_path: str,
    selfie_path: str,
    config: dict | None,
) -> None:
    """Write a README.md for a single run folder with markdown formatting."""
    now = datetime.now()
    status = "MATCH" if result.match else "NO MATCH"
    if result.error:
        status = "ERROR"

    md = []
    md.append(f"# KYC Face Match — {status}")
    md.append(f"")
    md.append(f"**Timestamp:** {now.strftime('%Y-%m-%d %H:%M:%S')}  ")
    md.append(f"**Aadhaar:** {aadhaar_path}  ")
    md.append(f"**Selfie:** {selfie_path}  ")
    md.append(f"")

    md.append(f"## Result")
    md.append(f"")
    md.append(f"| Metric | Value |")
    md.append(f"|--------|-------|")
    md.append(f"| **Result** | {status} |")
    md.append(f"| **Cosine Score** | {result.cosine_score:.4f} |")
    md.append(f"| **Confidence** | {result.confidence_pct:.1f}% |")
    md.append(f"| **Aadhaar Quality** | {result.aadhaar_quality:.2f} |")
    md.append(f"| **Selfie Quality** | {result.selfie_quality:.2f} |")

    # Multi-metric similarity
    l2_d = getattr(result, 'l2_distance', 0)
    l2_s = getattr(result, 'l2_score', 0)
    ssim_v = getattr(result, 'ssim', 0)
    lmk_s = getattr(result, 'landmark_score', -1)
    pose_d = getattr(result, 'pose_diff', -1)
    fused = getattr(result, 'fused_score', 0)
    md.append(f"| **L2 Distance** | {l2_d:.4f} (score: {l2_s:.4f}) |")
    md.append(f"| **SSIM** | {ssim_v:.4f} |")
    md.append(f"| **Landmark Score** | {lmk_s:.4f}{' (unavailable)' if lmk_s < 0 else ''} |")
    md.append(f"| **Pose Diff** | {pose_d:.1f} deg{' (unavailable)' if pose_d < 0 else ''} |")
    md.append(f"| **Fused Score** | {fused:.4f} |")

    a_age = getattr(result, "aadhaar_age", 0)
    s_age = getattr(result, "selfie_age", 0)
    a_g = getattr(result, "aadhaar_gender", "?")
    s_g = getattr(result, "selfie_gender", "?")
    md.append(f"| **Aadhaar** | {a_g}, age {a_age} |")
    md.append(f"| **Selfie** | {s_g}, age {s_age} |")
    md.append(f"| **Age Gap** | {abs(a_age - s_age)} years |")

    if result.vlm_same_person is not None:
        md.append(f"| **VLM Verdict** | {'Same person' if result.vlm_same_person else 'Different person'} |")
    if result.vlm_reasoning and result.vlm_reasoning not in ("N/A", "VLM guard disabled"):
        md.append(f"| **VLM Reasoning** | {result.vlm_reasoning} |")
    md.append(f"")

    # Decision trace
    if config:
        trace_lines = _build_decision_trace(result, config)
        md.append(f"## Decision Trace")
        md.append(f"```")
        for line in trace_lines:
            md.append(line)
        md.append(f"```")
        md.append(f"")

    # Face crops
    md.append(f"## Face Crops")
    md.append(f"| Aadhaar | Selfie |")
    md.append(f"|---------|--------|")
    md.append(f"| ![Aadhaar](aadhaar_crop.jpg) | ![Selfie](selfie_crop.jpg) |")
    md.append(f"")

    # Timings
    if result.stage_timings:
        total_ms = sum(result.stage_timings.values())
        md.append(f"## Timings ({total_ms:.0f}ms total)")
        md.append(f"| Stage | Time |")
        md.append(f"|-------|------|")
        for stage, ms in result.stage_timings.items():
            md.append(f"| {stage} | {ms:.0f}ms |")
        md.append(f"| **TOTAL** | **{total_ms:.0f}ms** |")
        md.append(f"")

    (run_dir / "README.md").write_text("\n".join(md), encoding="utf-8")


def _save_face_crops(result, run_dir: Path) -> list[str]:
    """Save the 112x112 aligned face crops into the run folder.

    Returns lines to append to the log noting the saved files.
    """
    lines = []

    for label, crop in [("aadhaar", getattr(result, "aadhaar_crop", None)),
                        ("selfie", getattr(result, "selfie_crop", None))]:
        if crop is None:
            continue
        filename = f"{label}_crop.jpg"
        cv2.imwrite(str(run_dir / filename), crop)
        lines.append(f"  {label.title()} crop: {filename}")

    return lines


def _build_decision_trace(result, config: dict | None) -> list[str]:
    """Generate a human-readable narrative of what happened and why.

    Walks through each pipeline stage and explains the decisions made,
    so someone reading the log understands the full reasoning chain.
    """
    trace = []

    # Extract thresholds from config (or use defaults matching config.yaml)
    match_thresh = 0.60
    uncertain_low = 0.40
    quality_thresh = 0.40
    vlm_enabled = True
    if config:
        match_thresh = config.get("similarity", {}).get("match_threshold", 0.60)
        uncertain_low = config.get("similarity", {}).get("uncertain_low", 0.40)
        quality_thresh = config.get("enhancement", {}).get("quality_threshold", 0.40)
        vlm_enabled = config.get("vlm_guard", {}).get("enabled", True)

    # Handle error case early
    if result.error:
        trace.append(f"  Pipeline failed: {result.error}")
        return trace

    # Step 1: Enhancement
    aadhaar_enhanced = result.aadhaar_quality < quality_thresh
    selfie_enhanced = result.selfie_quality < quality_thresh
    if aadhaar_enhanced or selfie_enhanced:
        enhanced_which = []
        if aadhaar_enhanced:
            enhanced_which.append(f"Aadhaar (quality {result.aadhaar_quality:.2f} < {quality_thresh})")
        if selfie_enhanced:
            enhanced_which.append(f"Selfie (quality {result.selfie_quality:.2f} < {quality_thresh})")
        trace.append(f"  1. Enhancement: Applied Real-ESRGAN to {', '.join(enhanced_which)}")
    else:
        trace.append(
            f"  1. Enhancement: Skipped — both images above quality threshold "
            f"(Aadhaar={result.aadhaar_quality:.2f}, Selfie={result.selfie_quality:.2f}, "
            f"threshold={quality_thresh})"
        )

    # Step 2: Cosine similarity zone
    score = result.cosine_score
    if score >= match_thresh:
        zone = "MATCH zone"
        zone_detail = f">= {match_thresh} match threshold"
    elif score >= uncertain_low:
        zone = "UNCERTAIN zone"
        zone_detail = f"between {uncertain_low} and {match_thresh}"
    else:
        zone = "NO MATCH zone"
        zone_detail = f"< {uncertain_low} uncertain threshold"
    trace.append(f"  2. Cosine similarity: {score:.4f} → {zone} ({zone_detail})")

    # Step 2b: Age-gap threshold relaxation (if applicable)
    a_age = getattr(result, "aadhaar_age", 0)
    s_age = getattr(result, "selfie_age", 0)
    age_gap = abs(a_age - s_age)
    age_gap_thresh = config.get("similarity", {}).get("age_gap_threshold", 5) if config else 5
    relax_per_yr = config.get("similarity", {}).get("age_gap_relaxation_per_year", 0.01) if config else 0.01
    max_relax = config.get("similarity", {}).get("max_age_gap_relaxation", 0.10) if config else 0.10

    if age_gap > age_gap_thresh:
        excess = age_gap - age_gap_thresh
        relaxation = min(excess * relax_per_yr, max_relax)
        eff_match = match_thresh - relaxation
        eff_uncertain = uncertain_low - relaxation
        trace.append(
            f"  2b. Age-gap relaxation: {age_gap}yr gap → threshold relaxed by {relaxation:.3f} "
            f"(effective: match={eff_match:.3f}, uncertain={eff_uncertain:.3f})"
        )

    # Step 3: Quality flags
    quality_low = result.aadhaar_quality < quality_thresh or result.selfie_quality < quality_thresh
    if quality_low:
        low_sources = []
        if result.aadhaar_quality < quality_thresh:
            low_sources.append("Aadhaar")
        if result.selfie_quality < quality_thresh:
            low_sources.append("Selfie")
        trace.append(f"  3. Quality flag: LOW ({', '.join(low_sources)} below {quality_thresh} threshold)")
    else:
        trace.append(f"  3. Quality flag: OK (both images above {quality_thresh} threshold)")

    # Step 4: VLM invocation decision
    needs_vlm = (
        (score >= match_thresh and quality_low) or
        (uncertain_low <= score < match_thresh)
    )
    if not vlm_enabled:
        trace.append(f"  4. VLM guard: Disabled in config")
    elif needs_vlm:
        if score >= match_thresh:
            reason = "high cosine score but low image quality → double-checking"
        else:
            reason = "cosine score in uncertain zone → VLM decides"
        trace.append(f"  4. VLM guard: Invoked — {reason}")

        # VLM result
        if result.vlm_same_person is True:
            trace.append(f"     VLM verdict: SAME PERSON")
        elif result.vlm_same_person is False:
            trace.append(f"     VLM verdict: DIFFERENT PERSON")
        else:
            trace.append(f"     VLM verdict: UNAVAILABLE (Ollama timeout or error)")
    else:
        if score >= match_thresh:
            trace.append(f"  4. VLM guard: Not needed — score above threshold with good quality")
        else:
            trace.append(f"  4. VLM guard: Not needed — score below uncertain zone (definite no-match)")

    # Step 5: Final decision reasoning
    trace.append(f"  5. Final decision: {'MATCH' if result.match else 'NO MATCH'} "
                 f"at {result.confidence_pct:.1f}% confidence")

    # Explain the confidence calculation using config values
    ca = config.get("confidence_adjustments", {}) if config else {}
    vlm_bonus = ca.get("vlm_confirmation_bonus", 8.0)
    vlm_reject_high = ca.get("vlm_rejection_above_threshold", -20.0)
    vlm_reject_unc = ca.get("vlm_rejection_uncertain", -10.0)
    q_penalty = ca.get("quality_penalty", -5.0)

    base_conf = score * 100.0
    conf_parts = [f"base {base_conf:.1f}%"]

    if result.vlm_same_person is True:
        conf_parts.append(f"{vlm_bonus:+.0f} VLM confirmation")
    elif result.vlm_same_person is False:
        if score >= match_thresh:
            conf_parts.append(f"{vlm_reject_high:+.0f} VLM rejection (above threshold)")
        else:
            conf_parts.append(f"{vlm_reject_unc:+.0f} VLM rejection (uncertain zone)")

    if quality_low and score >= match_thresh:
        conf_parts.append(f"{q_penalty:+.0f} quality penalty")

    if len(conf_parts) > 1:
        trace.append(f"     Confidence breakdown: {' → '.join(conf_parts)}")

    # Explain why the final decision was made
    if score >= match_thresh:
        if result.vlm_same_person is False:
            trace.append(f"     Reason: Score was above threshold but VLM explicitly rejected the match")
        elif quality_low and result.vlm_same_person is True:
            trace.append(f"     Reason: Score above threshold, VLM confirmed despite low quality images")
        elif quality_low and result.vlm_same_person is None:
            trace.append(f"     Reason: Score above threshold, VLM unavailable — trusting high cosine score")
        else:
            trace.append(f"     Reason: Score above threshold with good quality — confident match")
    elif score >= uncertain_low:
        if result.vlm_same_person is True:
            trace.append(f"     Reason: Score in uncertain zone, but VLM confirmed same person")
        elif result.vlm_same_person is False:
            trace.append(f"     Reason: Score in uncertain zone and VLM says different person")
        else:
            trace.append(f"     Reason: Score in uncertain zone, VLM unavailable — conservative rejection")
    else:
        trace.append(f"     Reason: Score below {uncertain_low} — definite no-match, VLM not needed")

    return trace


# ---------------------------------------------------------------------------
# Batch logging
# ---------------------------------------------------------------------------

def create_batch_dir(log_dir: str = "logs") -> Path:
    """Create a timestamped batch folder and return its path."""
    now = datetime.now()
    batch_dir = Path(log_dir) / f"batch_{now.strftime('%Y-%m-%d_%H-%M-%S')}"
    batch_dir.mkdir(parents=True, exist_ok=True)
    return batch_dir


def log_batch_result(
    result,
    aadhaar_path: str,
    selfie_path: str,
    batch_dir: Path,
    config: dict | None = None,
) -> Path:
    """Log a single result into a named subfolder inside a batch directory.

    Subfolder name: <aadhaar_stem>_vs_<selfie_stem>_<STATUS>
    """
    status = "MATCH" if result.match else "NO_MATCH"
    if result.error:
        status = "ERROR"

    a_stem = Path(aadhaar_path).stem
    s_stem = Path(selfie_path).stem
    pair_name = f"{a_stem}_vs_{s_stem}_{status}"

    run_dir = batch_dir / pair_name
    run_dir.mkdir(parents=True, exist_ok=True)

    # Reuse log_result's core writing, pointing at this subfolder
    now = datetime.now()
    total_ms = sum(result.stage_timings.values()) if result.stage_timings else 0

    lines = [
        f"Aadhaar KYC Face Matching — Run Log",
        f"{'=' * 50}",
        f"Timestamp:      {now.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Aadhaar Image:  {aadhaar_path}",
        f"Selfie Image:   {selfie_path}",
        f"",
        f"--- Result ---",
        f"Match:          {'YES' if result.match else 'NO'}",
        f"Confidence:     {result.confidence_pct:.1f}%",
        f"Cosine Score:   {result.cosine_score:.4f}",
        f"",
        *_metrics_lines(result),
        f"",
        f"--- Quality ---",
        f"Aadhaar Quality: {result.aadhaar_quality:.2f}",
        f"Selfie Quality:  {result.selfie_quality:.2f}",
        f"",
        *_demographics_lines(result),
        f"",
        f"--- VLM Guard ---",
        f"VLM Same Person: {result.vlm_same_person}",
        f"VLM Reasoning:   {result.vlm_reasoning or 'N/A'}",
        f"",
        f"--- Decision Trace ---",
    ]
    lines.extend(_build_decision_trace(result, config))
    lines.append(f"")
    lines.append(f"--- Timings ---")
    for stage, ms in result.stage_timings.items():
        lines.append(f"  {stage:.<30s} {ms:.0f} ms")
    lines.append(f"  {'TOTAL':.<30s} {total_ms:.0f} ms")
    if result.error:
        lines.extend([f"", f"--- Error ---", f"{result.error}"])
    crop_lines = _save_face_crops(result, run_dir)
    if crop_lines:
        lines.append(f"")
        lines.append(f"--- Face Crops ---")
        lines.extend(crop_lines)
    lines.append(f"{'=' * 50}")

    (run_dir / "result.txt").write_text("\n".join(lines), encoding="utf-8")

    # Also write a README.md for visual reading
    _write_single_readme(run_dir, result, aadhaar_path, selfie_path, config)

    return run_dir


def write_batch_summary(
    batch_dir: Path,
    results: list[tuple[str, str, object]],
) -> Path:
    """Write summary.txt in the batch folder with a table of all results.

    Args:
        batch_dir: The batch folder from create_batch_dir().
        results: List of (aadhaar_path, selfie_path, PipelineResult).

    Returns:
        Path to summary.txt.
    """
    now = datetime.now()
    lines = [
        "Aadhaar KYC Face Matching — Batch Summary",
        "=" * 110,
        f"Timestamp: {now.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total pairs: {len(results)}",
        "",
        f"{'Aadhaar':25s} | {'Selfie':15s} | {'Result':10s} | Cosine | Fused  | Conf   "
        f"| {'Aadhaar Demo':16s} | {'Selfie Demo':16s} | Age Note",
        "-" * 160,
    ]

    matches = 0
    for aadhaar_path, selfie_path, result in results:
        a_name = Path(aadhaar_path).name
        s_name = Path(selfie_path).name
        status = "MATCH" if result.match else "NO MATCH"
        if result.error:
            status = "ERROR"
        if result.match:
            matches += 1

        a_g = getattr(result, "aadhaar_gender", "?")
        a_a = getattr(result, "aadhaar_age", 0)
        s_g = getattr(result, "selfie_gender", "?")
        s_a = getattr(result, "selfie_age", 0)
        age_note = _age_comparison(a_a, s_a)
        gender_note = "" if a_g == s_g else " [GENDER MISMATCH]"

        fused = getattr(result, 'fused_score', 0)
        lines.append(
            f"{a_name:25s} | {s_name:15s} | {status:10s} | {result.cosine_score:.4f} "
            f"| {fused:.4f} | {result.confidence_pct:5.1f}% | {a_g} age {a_a:<10d} | {s_g} age {s_a:<10d} "
            f"| {age_note}{gender_note}"
        )

    lines.extend([
        "-" * 160,
        f"Matches: {matches}/{len(results)}",
        "=" * 160,
    ])

    summary_path = batch_dir / "summary.txt"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    return summary_path


def write_batch_readme(
    batch_dir: Path,
    results: list[tuple[str, str, object]],
    config: dict | None = None,
) -> Path:
    """Write a README.md in the batch folder with a visual markdown summary.

    Includes results table, per-pair details with VLM reasoning, decision
    traces, pipeline config, and linked face crop images.

    Args:
        batch_dir: The batch folder from create_batch_dir().
        results: List of (aadhaar_path, selfie_path, PipelineResult).
        config: Pipeline config dict for threshold/config display.

    Returns:
        Path to README.md.
    """
    now = datetime.now()
    matches = sum(1 for _, _, r in results if r.match)
    total = len(results)

    md = []
    md.append(f"# Aadhaar KYC Face Matching — Batch Report")
    md.append(f"")
    md.append(f"**Timestamp:** {now.strftime('%Y-%m-%d %H:%M:%S')}  ")
    md.append(f"**Total pairs:** {total}  ")
    md.append(f"**Matches:** {matches}/{total}  ")
    md.append(f"**Pipeline version:** v2  ")
    md.append(f"")

    # --- Results Table ---
    md.append(f"## Results Summary")
    md.append(f"")
    md.append(f"| # | Aadhaar | Selfie | Result | Cosine | Confidence | Aadhaar Age | Selfie Age | Age Gap | VLM |")
    md.append(f"|---|---------|--------|--------|--------|------------|-------------|------------|---------|-----|")

    for i, (aadhaar_path, selfie_path, result) in enumerate(results, 1):
        a_name = Path(aadhaar_path).name
        s_name = Path(selfie_path).name
        status = "**MATCH**" if result.match else "NO MATCH"
        if result.error:
            status = "ERROR"
        a_age = getattr(result, "aadhaar_age", 0)
        s_age = getattr(result, "selfie_age", 0)
        age_gap = abs(a_age - s_age)
        a_g = getattr(result, "aadhaar_gender", "?")
        s_g = getattr(result, "selfie_gender", "?")
        vlm = "---"
        if result.vlm_same_person is True:
            vlm = "Confirmed"
        elif result.vlm_same_person is False:
            vlm = "Rejected"
        elif result.vlm_same_person is None and getattr(result, "vlm_reasoning", None):
            vlm = "N/A"

        gender_flag = " :warning:" if a_g != s_g and a_g != "unknown" and s_g != "unknown" else ""
        md.append(
            f"| {i} | {a_name} | {s_name} | {status} | {result.cosine_score:.4f} "
            f"| {result.confidence_pct:.1f}% | {a_g} age {a_age} | {s_g} age {s_age} "
            f"| {age_gap}yr | {vlm}{gender_flag} |"
        )

    md.append(f"")

    # --- Per-Pair Details ---
    md.append(f"## Per-Pair Details")
    md.append(f"")

    for i, (aadhaar_path, selfie_path, result) in enumerate(results, 1):
        a_name = Path(aadhaar_path).name
        s_name = Path(selfie_path).name
        a_stem = Path(aadhaar_path).stem
        s_stem = Path(selfie_path).stem
        status_tag = "MATCH" if result.match else "NO_MATCH"
        if result.error:
            status_tag = "ERROR"
        pair_folder = f"{a_stem}_vs_{s_stem}_{status_tag}"

        status_emoji = "+" if result.match else "-"
        md.append(f"### {i}. {a_name} vs {s_name}")
        md.append(f"")

        md.append(f"| Metric | Value |")
        md.append(f"|--------|-------|")
        md.append(f"| **Result** | {'MATCH' if result.match else 'NO MATCH'} |")
        md.append(f"| **Cosine Score** | {result.cosine_score:.4f} |")
        md.append(f"| **Confidence** | {result.confidence_pct:.1f}% |")
        md.append(f"| **Aadhaar Quality** | {result.aadhaar_quality:.2f} |")
        md.append(f"| **Selfie Quality** | {result.selfie_quality:.2f} |")

        # Multi-metric similarity
        l2_d = getattr(result, 'l2_distance', 0)
        l2_s = getattr(result, 'l2_score', 0)
        ssim_v = getattr(result, 'ssim', 0)
        lmk_s = getattr(result, 'landmark_score', -1)
        pose_d = getattr(result, 'pose_diff', -1)
        fused = getattr(result, 'fused_score', 0)
        md.append(f"| **L2 Distance** | {l2_d:.4f} (score: {l2_s:.4f}) |")
        md.append(f"| **SSIM** | {ssim_v:.4f} |")
        md.append(f"| **Landmark Score** | {lmk_s:.4f}{' (unavailable)' if lmk_s < 0 else ''} |")
        md.append(f"| **Pose Diff** | {pose_d:.1f} deg{' (unavailable)' if pose_d < 0 else ''} |")
        md.append(f"| **Fused Score** | {fused:.4f} |")

        a_age = getattr(result, "aadhaar_age", 0)
        s_age = getattr(result, "selfie_age", 0)
        a_g = getattr(result, "aadhaar_gender", "?")
        s_g = getattr(result, "selfie_gender", "?")
        md.append(f"| **Aadhaar Demographics** | {a_g}, age {a_age} |")
        md.append(f"| **Selfie Demographics** | {s_g}, age {s_age} |")
        md.append(f"| **Age Gap** | {abs(a_age - s_age)} years |")

        if a_g != s_g and a_g != "unknown" and s_g != "unknown":
            md.append(f"| **Gender** | MISMATCH |")
        else:
            md.append(f"| **Gender** | Consistent |")

        if result.vlm_same_person is not None:
            md.append(f"| **VLM Verdict** | {'Same person' if result.vlm_same_person else 'Different person'} |")
        if result.vlm_reasoning and result.vlm_reasoning not in ("N/A", "VLM guard disabled"):
            md.append(f"| **VLM Reasoning** | {result.vlm_reasoning} |")

        md.append(f"")

        # Decision trace
        if config:
            trace_lines = _build_decision_trace(result, config)
            md.append(f"<details><summary>Decision Trace</summary>")
            md.append(f"")
            md.append(f"```")
            for line in trace_lines:
                md.append(line)
            md.append(f"```")
            md.append(f"</details>")
            md.append(f"")

        # Timings
        if result.stage_timings:
            total_ms = sum(result.stage_timings.values())
            md.append(f"<details><summary>Timings (total {total_ms:.0f}ms)</summary>")
            md.append(f"")
            md.append(f"| Stage | Time |")
            md.append(f"|-------|------|")
            for stage, ms in result.stage_timings.items():
                md.append(f"| {stage} | {ms:.0f}ms |")
            md.append(f"| **TOTAL** | **{total_ms:.0f}ms** |")
            md.append(f"</details>")
            md.append(f"")

        # Face crop links
        md.append(f"**Face Crops:** [{pair_folder}/aadhaar_crop.jpg]({pair_folder}/aadhaar_crop.jpg) | "
                   f"[{pair_folder}/selfie_crop.jpg]({pair_folder}/selfie_crop.jpg)")
        md.append(f"")
        md.append(f"---")
        md.append(f"")

    # --- Pipeline Config ---
    md.append(f"## Pipeline Configuration")
    md.append(f"")
    if config:
        sim = config.get("similarity", {})
        preproc = config.get("preprocessing", {})
        face = config.get("face", {})
        vlm = config.get("vlm_guard", {})
        ca = config.get("confidence_adjustments", {})

        md.append(f"| Setting | Value |")
        md.append(f"|---------|-------|")
        md.append(f"| Match threshold | {sim.get('match_threshold', 0.60)} |")
        md.append(f"| Uncertain zone | {sim.get('uncertain_low', 0.40)} - {sim.get('match_threshold', 0.60)} |")
        md.append(f"| Age gap threshold | {sim.get('age_gap_threshold', 5)} years |")
        md.append(f"| Max age relaxation | {sim.get('max_age_gap_relaxation', 0.10)} |")
        md.append(f"| CLAHE | {'Enabled' if preproc.get('aadhaar_clahe') else 'Disabled'} (clip={preproc.get('clahe_clip_limit', 2.0)}, tile={preproc.get('clahe_tile_size', 8)}) |")
        md.append(f"| Flip augment (TTA) | {'Enabled' if face.get('flip_augment') else 'Disabled'} |")
        md.append(f"| Dual-path | {'Enabled' if preproc.get('dual_path') else 'Disabled'} |")
        md.append(f"| Grayscale normalize | {'Enabled' if preproc.get('grayscale_normalize') else 'Disabled'} |")
        md.append(f"| VLM model | {vlm.get('model', 'N/A')} |")
        md.append(f"| VLM confirmation bonus | +{ca.get('vlm_confirmation_bonus', 8.0)} |")
        md.append(f"| Age gap VLM bonus | +{ca.get('age_gap_vlm_bonus', 5.0)} |")
    md.append(f"")

    readme_path = batch_dir / "README.md"
    readme_path.write_text("\n".join(md), encoding="utf-8")
    return readme_path
