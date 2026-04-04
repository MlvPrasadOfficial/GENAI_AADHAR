"""Aadhaar KYC Face Matching — CLI entry point.

Usage:
    python main.py --aadhaar card.jpg --selfie selfie.jpg
    python main.py --aadhaar card.jpg --selfie selfie.jpg --verbose
    python main.py --aadhaar card.jpg --selfie selfie.jpg --json-output

Exit codes:
    0 = MATCH
    1 = NO MATCH
    2 = ERROR
"""

import argparse
import json
import logging
import sys
from dataclasses import asdict
from pathlib import Path

from pipeline.orchestrator import KYCPipelineOrchestrator
from utils.config_loader import load_config


def main():
    parser = argparse.ArgumentParser(
        description="Aadhaar KYC Face Matching Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Exit codes: 0=MATCH, 1=NO MATCH, 2=ERROR",
    )
    parser.add_argument(
        "--aadhaar", required=True, type=Path,
        help="Path to Aadhaar card image (JPEG/PNG)",
    )
    parser.add_argument(
        "--selfie", required=True, type=Path,
        help="Path to user selfie image (JPEG/PNG)",
    )
    parser.add_argument(
        "--config", default="config.yaml", type=Path,
        help="Path to config.yaml (default: config.yaml)",
    )
    parser.add_argument("--verbose", action="store_true", help="Show detailed output")
    parser.add_argument("--json-output", action="store_true", help="Output as JSON")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    # Configure logging
    level = logging.DEBUG if args.debug else (logging.INFO if args.verbose else logging.WARNING)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    # Validate inputs
    if not args.aadhaar.exists():
        print(f"Error: Aadhaar image not found: {args.aadhaar}", file=sys.stderr)
        sys.exit(2)
    if not args.selfie.exists():
        print(f"Error: Selfie image not found: {args.selfie}", file=sys.stderr)
        sys.exit(2)

    # Load config and build pipeline
    try:
        config = load_config(args.config)
    except (FileNotFoundError, ValueError) as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(2)

    pipeline = KYCPipelineOrchestrator(config)
    pipeline.load()

    # Run pipeline
    result = pipeline.run(
        args.aadhaar.read_bytes(),
        args.selfie.read_bytes(),
    )

    # Output
    if args.json_output:
        output = asdict(result)
        print(json.dumps(output, indent=2, default=str))
    else:
        if result.error:
            print(f"\n  ERROR: {result.error}")
            sys.exit(2)

        status = "MATCH" if result.match else "NO MATCH"
        print(f"\n{'='*44}")
        print(f"  Result:     {status}")
        print(f"  Confidence: {result.confidence_pct:.1f}%")
        print(f"  Cosine:     {result.cosine_score:.4f}")
        if result.vlm_reasoning and result.vlm_reasoning != "VLM guard disabled":
            print(f"  VLM:        {result.vlm_reasoning}")
        if args.verbose:
            print(f"\n  Aadhaar quality: {result.aadhaar_quality:.2f}")
            print(f"  Selfie quality:  {result.selfie_quality:.2f}")
            total = sum(result.stage_timings.values())
            print(f"\n  Timings (total {total:.0f}ms):")
            for stage, ms in result.stage_timings.items():
                print(f"    {stage}: {ms:.0f}ms")
        print(f"{'='*44}\n")

    sys.exit(0 if result.match else 1)


if __name__ == "__main__":
    main()
