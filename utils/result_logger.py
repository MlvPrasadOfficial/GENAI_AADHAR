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
    return run_dir


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
        f"{'Aadhaar':25s} | {'Selfie':15s} | {'Result':10s} | Cosine | Conf   "
        f"| {'Aadhaar Demo':16s} | {'Selfie Demo':16s} | Age Note",
        "-" * 145,
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

        lines.append(
            f"{a_name:25s} | {s_name:15s} | {status:10s} | {result.cosine_score:.4f} "
            f"| {result.confidence_pct:5.1f}% | {a_g} age {a_a:<10d} | {s_g} age {s_a:<10d} "
            f"| {age_note}{gender_note}"
        )

    lines.extend([
        "-" * 145,
        f"Matches: {matches}/{len(results)}",
        "=" * 145,
    ])

    summary_path = batch_dir / "summary.txt"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    return summary_path
