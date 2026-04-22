"""Download model weights for the Aadhaar KYC Face Matching Pipeline.

Downloads:
  1. RealESRGAN_x4plus.pth → models/realesrgan/
  2. InsightFace buffalo_l  → models/insightface/ (auto-downloaded on first use)

Usage:
    python scripts/download_models.py
    python scripts/download_models.py --realesrgan-only
    python scripts/download_models.py --insightface-only
"""

# Must be set before any import that touches matplotlib (e.g. InsightFace)
import os as _os
_os.environ.setdefault("MPLBACKEND", "Agg")

import argparse
import os
import sys
from pathlib import Path

import requests
from tqdm import tqdm

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

REALESRGAN_URL = (
    "https://github.com/xinntao/Real-ESRGAN/releases/download/"
    "v0.1.0/RealESRGAN_x4plus.pth"
)
REALESRGAN_PATH = MODELS_DIR / "realesrgan" / "RealESRGAN_x4plus.pth"


def download_file(url: str, dest: Path) -> None:
    """Download a file with progress bar."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        print(f"  Already exists: {dest}")
        return

    print(f"  Downloading: {url}")
    print(f"  Saving to:   {dest}")

    resp = requests.get(url, stream=True, timeout=60)
    resp.raise_for_status()
    total = int(resp.headers.get("content-length", 0))

    with open(dest, "wb") as f, tqdm(
        total=total, unit="B", unit_scale=True, desc=dest.name
    ) as bar:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
            bar.update(len(chunk))

    print(f"  Done: {dest} ({dest.stat().st_size / 1e6:.1f} MB)")


def download_realesrgan() -> None:
    """Download Real-ESRGAN x4plus weights."""
    print("\n[1/2] Real-ESRGAN x4plus")
    download_file(REALESRGAN_URL, REALESRGAN_PATH)


def _download_insightface_pack(name: str, label: str) -> None:
    """Trigger an InsightFace model pack auto-download via FaceAnalysis."""
    print(f"\n{label}")
    root = MODELS_DIR / "insightface"
    root.mkdir(parents=True, exist_ok=True)
    os.environ["INSIGHTFACE_ROOT"] = str(root)

    pack_dir = root / "models" / name
    if pack_dir.exists() and any(pack_dir.glob("*.onnx")):
        print(f"  Already exists: {pack_dir}")
        return

    print(f"  Triggering auto-download for pack '{name}' via FaceAnalysis.prepare()...")
    import insightface

    app = insightface.app.FaceAnalysis(
        name=name,
        root=str(root),
        providers=["CPUExecutionProvider"],
    )
    app.prepare(ctx_id=-1, det_size=(160, 160))
    print(f"  Done: {pack_dir}")


def download_insightface() -> None:
    """Trigger InsightFace buffalo_l auto-download (primary recognition pack)."""
    _download_insightface_pack("buffalo_l", "[2/3] InsightFace buffalo_l (primary)")


def download_antelopev2() -> None:
    """Trigger InsightFace antelopev2 auto-download (secondary ensemble pack)."""
    _download_insightface_pack("antelopev2", "[3/3] InsightFace antelopev2 (secondary ensemble)")


def main():
    parser = argparse.ArgumentParser(description="Download model weights")
    parser.add_argument("--realesrgan-only", action="store_true")
    parser.add_argument("--insightface-only", action="store_true")
    parser.add_argument(
        "--skip-secondary", action="store_true",
        help="Skip antelopev2 (ensemble second model) download",
    )
    args = parser.parse_args()

    print(f"Models directory: {MODELS_DIR}")

    if args.realesrgan_only:
        download_realesrgan()
    elif args.insightface_only:
        download_insightface()
        if not args.skip_secondary:
            download_antelopev2()
    else:
        download_realesrgan()
        download_insightface()
        if not args.skip_secondary:
            download_antelopev2()

    print("\nAll models ready.")


if __name__ == "__main__":
    main()
