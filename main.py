"""Aadhaar KYC Face Matching — CLI entry point.

Usage:
    python main.py --aadhaar card.jpg --selfie selfie.jpg
    python main.py --aadhaar card.jpg --selfie selfie.jpg --verbose
    python main.py --aadhaar card.jpg --selfie selfie.jpg --json-output
    python main.py --batch pairs.csv --verbose

Exit codes:
    0 = MATCH (or all match in batch)
    1 = NO MATCH (or any no-match in batch)
    2 = ERROR
"""

import argparse
import csv
import json
import logging
import sys
from dataclasses import asdict
from pathlib import Path

from pipeline.orchestrator import KYCPipelineOrchestrator
from utils.config_loader import load_config
from utils.result_logger import (
    log_result,
    create_batch_dir,
    log_batch_result,
    write_batch_summary,
)

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


def _validate_image_path(label: str, path: Path) -> None:
    """Validate an image path exists, is non-empty, and under size limit."""
    if not path.exists():
        print(f"Error: {label} image not found: {path}", file=sys.stderr)
        sys.exit(2)
    if path.stat().st_size > MAX_FILE_SIZE:
        print(f"Error: {label} file too large ({path.stat().st_size // 1024 // 1024}MB > 50MB limit)", file=sys.stderr)
        sys.exit(2)
    if path.stat().st_size == 0:
        print(f"Error: {label} file is empty: {path}", file=sys.stderr)
        sys.exit(2)


def _run_single(args, config: dict, pipeline: KYCPipelineOrchestrator) -> int:
    """Run pipeline for a single Aadhaar-selfie pair. Returns exit code."""
    result = pipeline.run(
        args.aadhaar.read_bytes(),
        args.selfie.read_bytes(),
    )

    log_dir = log_result(result, str(args.aadhaar), str(args.selfie), config=config)
    logging.getLogger(__name__).info("Result saved to %s", log_dir)

    if args.json_output:
        output = asdict(result)
        output.pop("aadhaar_crop", None)
        output.pop("selfie_crop", None)
        print(json.dumps(output, indent=2, default=str))
    else:
        if result.error:
            print(f"\n  ERROR: {result.error}")
            return 2

        status = "MATCH" if result.match else "NO MATCH"
        print(f"\n{'='*44}")
        print(f"  Result:     {status}")
        print(f"  Confidence: {result.confidence_pct:.1f}%")
        print(f"  Cosine:     {result.cosine_score:.4f}")
        if result.vlm_reasoning and result.vlm_reasoning != "VLM guard disabled":
            print(f"  VLM:        {result.vlm_reasoning}")
        if args.verbose:
            from utils.result_logger import _age_comparison, _gender_match_note
            print(f"\n  Aadhaar quality: {result.aadhaar_quality:.2f}  |  Gender: {result.aadhaar_gender}  Age: {result.aadhaar_age}")
            print(f"  Selfie quality:  {result.selfie_quality:.2f}  |  Gender: {result.selfie_gender}  Age: {result.selfie_age}")
            print(f"  {_age_comparison(result.aadhaar_age, result.selfie_age)}")
            print(f"  {_gender_match_note(result.aadhaar_gender, result.selfie_gender)}")
            total = sum(result.stage_timings.values())
            print(f"\n  Timings (total {total:.0f}ms):")
            for stage, ms in result.stage_timings.items():
                print(f"    {stage}: {ms:.0f}ms")
        print(f"{'='*44}\n")

    return 0 if result.match else 1


def _run_batch(args, config: dict, pipeline: KYCPipelineOrchestrator) -> int:
    """Run pipeline for all pairs in a CSV file. Returns exit code."""
    csv_path = args.batch

    # Read and validate CSV
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                print("Error: CSV file is empty", file=sys.stderr)
                return 2
            # Normalize headers to lowercase for case-insensitive matching
            header_map = {h.strip().lower(): h for h in reader.fieldnames}
            if "aadhaar" not in header_map or "selfie" not in header_map:
                print(
                    f"Error: CSV must have 'aadhaar' and 'selfie' columns, got: {list(reader.fieldnames)}",
                    file=sys.stderr,
                )
                return 2
            pairs = []
            for row in reader:
                a_path = Path(row[header_map["aadhaar"]].strip())
                s_path = Path(row[header_map["selfie"]].strip())
                pairs.append((a_path, s_path))
    except FileNotFoundError:
        print(f"Error: CSV file not found: {csv_path}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Error reading CSV: {e}", file=sys.stderr)
        return 2

    if not pairs:
        print("Error: CSV contains no data rows", file=sys.stderr)
        return 2

    # Validate all paths before loading models
    for a_path, s_path in pairs:
        _validate_image_path("Aadhaar", a_path)
        _validate_image_path("Selfie", s_path)

    print(f"Batch mode: {len(pairs)} pairs to process")

    batch_dir = create_batch_dir()
    results = []
    any_error = False
    any_no_match = False

    for i, (a_path, s_path) in enumerate(pairs, 1):
        print(f"  [{i}/{len(pairs)}] {a_path.name} vs {s_path.name} ... ", end="", flush=True)
        result = pipeline.run(a_path.read_bytes(), s_path.read_bytes())
        log_batch_result(result, str(a_path), str(s_path), batch_dir, config=config)
        results.append((str(a_path), str(s_path), result))

        if result.error:
            print(f"ERROR: {result.error}")
            any_error = True
        elif result.match:
            print(f"MATCH (cosine={result.cosine_score:.4f}, conf={result.confidence_pct:.1f}%)")
        else:
            print(f"NO MATCH (cosine={result.cosine_score:.4f}, conf={result.confidence_pct:.1f}%)")
            any_no_match = True

    summary_path = write_batch_summary(batch_dir, results)
    print(f"\nBatch complete. Summary: {summary_path}")
    print(f"Logs: {batch_dir}")

    matches = sum(1 for _, _, r in results if r.match)
    print(f"Results: {matches}/{len(results)} matches")

    if any_error:
        return 2
    return 0 if not any_no_match else 1


def main():
    parser = argparse.ArgumentParser(
        description="Aadhaar KYC Face Matching Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exit codes: 0=MATCH, 1=NO MATCH, 2=ERROR",
    )

    # Mutually exclusive: single pair vs batch
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument(
        "--aadhaar", type=Path,
        help="Path to Aadhaar card image (JPEG/PNG)",
    )
    mode.add_argument(
        "--batch", type=Path,
        help="CSV file with 'aadhaar,selfie' columns for batch processing",
    )

    parser.add_argument(
        "--selfie", type=Path,
        help="Path to user selfie image (JPEG/PNG) — required with --aadhaar",
    )
    parser.add_argument(
        "--config", default="config.yaml", type=Path,
        help="Path to config.yaml (default: config.yaml)",
    )
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    parser.add_argument("--json-output", action="store_true", help="Output as JSON (single mode only)")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    # Validate that --selfie is provided when using --aadhaar
    if args.aadhaar and not args.selfie:
        parser.error("--selfie is required when using --aadhaar")

    # Configure logging
    level = logging.DEBUG if args.debug else (logging.INFO if args.verbose else logging.WARNING)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Load config
    try:
        config = load_config(args.config)
    except (FileNotFoundError, ValueError) as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(2)

    # Build and load pipeline
    pipeline = KYCPipelineOrchestrator(config)

    if args.aadhaar:
        # Single mode — validate inputs
        _validate_image_path("Aadhaar", args.aadhaar)
        _validate_image_path("Selfie", args.selfie)
        pipeline.load()
        exit_code = _run_single(args, config, pipeline)
    else:
        # Batch mode — validation happens inside _run_batch before pipeline.load()
        pipeline.load()
        exit_code = _run_batch(args, config, pipeline)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
