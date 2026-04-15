"""Load and validate pipeline configuration from YAML."""

from pathlib import Path

import yaml

# Defaults for confidence_adjustments (used when section is absent in config)
DEFAULT_CONFIDENCE_ADJUSTMENTS = {
    "vlm_confirmation_bonus": 8.0,
    "vlm_rejection_above_threshold": -20.0,
    "vlm_rejection_uncertain": -10.0,
    "quality_penalty": -5.0,
}


def load_config(config_path: str | Path = "config.yaml") -> dict:
    """Load config.yaml and return as a dictionary.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Configuration dictionary.

    Raises:
        FileNotFoundError: If the config file doesn't exist.
        yaml.YAMLError: If the YAML is malformed.
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    _validate(config)

    # Merge confidence_adjustments defaults for any missing keys
    ca = config.setdefault("confidence_adjustments", {})
    for key, default in DEFAULT_CONFIDENCE_ADJUSTMENTS.items():
        ca.setdefault(key, default)

    return config


def _validate(config: dict) -> None:
    """Validate config: required sections, threshold ranges, and constraint relationships."""
    required_sections = ["enhancement", "face", "similarity", "vlm_guard"]
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required config section: '{section}'")

    # --- similarity thresholds ---
    sim = config["similarity"]
    for key in ("match_threshold", "uncertain_low"):
        val = sim[key]
        if not (0.0 <= val <= 1.0):
            raise ValueError(f"similarity.{key} must be in [0.0, 1.0], got {val}")
    if sim["uncertain_low"] >= sim["match_threshold"]:
        raise ValueError(
            f"uncertain_low ({sim['uncertain_low']}) must be < "
            f"match_threshold ({sim['match_threshold']})"
        )

    # --- age-gap relaxation (optional) ---
    if "age_gap_threshold" in sim:
        agt = sim["age_gap_threshold"]
        if not isinstance(agt, (int, float)) or agt < 0:
            raise ValueError(f"similarity.age_gap_threshold must be non-negative, got {agt}")
    if "age_gap_relaxation_per_year" in sim:
        rpy = sim["age_gap_relaxation_per_year"]
        if not isinstance(rpy, (int, float)) or rpy < 0:
            raise ValueError(f"similarity.age_gap_relaxation_per_year must be non-negative, got {rpy}")
    if "max_age_gap_relaxation" in sim:
        mar = sim["max_age_gap_relaxation"]
        if not isinstance(mar, (int, float)) or mar < 0:
            raise ValueError(f"similarity.max_age_gap_relaxation must be non-negative, got {mar}")
        # Ensure relaxation won't push threshold below uncertain_low
        effective_min = sim["match_threshold"] - mar
        if effective_min < sim["uncertain_low"]:
            raise ValueError(
                f"max_age_gap_relaxation ({mar}) would push threshold below "
                f"uncertain_low ({sim['uncertain_low']})"
            )

    # --- face detection ---
    det = config["face"]
    if not (0.0 <= det["det_thresh"] <= 1.0):
        raise ValueError(f"face.det_thresh must be in [0.0, 1.0], got {det['det_thresh']}")
    if "det_thresh_fallback" in det:
        fb = det["det_thresh_fallback"]
        if not (0.0 <= fb <= 1.0):
            raise ValueError(f"face.det_thresh_fallback must be in [0.0, 1.0], got {fb}")
        if fb >= det["det_thresh"]:
            raise ValueError("face.det_thresh_fallback must be < face.det_thresh")

    # det_size must be a 2-element list of positive integers
    ds = det.get("det_size")
    if ds is not None:
        if not isinstance(ds, (list, tuple)) or len(ds) != 2:
            raise ValueError("face.det_size must be [width, height]")
        if ds[0] <= 0 or ds[1] <= 0:
            raise ValueError("face.det_size dimensions must be positive")

    # --- enhancement ---
    enh = config["enhancement"]
    if "upscale" in enh and enh["upscale"] <= 0:
        raise ValueError(f"enhancement.upscale must be positive, got {enh['upscale']}")
    if "quality_threshold" in enh:
        qt = enh["quality_threshold"]
        if not (0.0 <= qt <= 1.0):
            raise ValueError(f"enhancement.quality_threshold must be in [0.0, 1.0], got {qt}")

    # --- vlm_guard ---
    vlm = config["vlm_guard"]
    if "max_new_tokens" in vlm:
        mnt = vlm["max_new_tokens"]
        if not isinstance(mnt, int) or mnt <= 0:
            raise ValueError(f"vlm_guard.max_new_tokens must be a positive integer, got {mnt}")

    # --- preprocessing (optional section) ---
    if "preprocessing" in config:
        preproc = config["preprocessing"]
        if "clahe_clip_limit" in preproc:
            cl = preproc["clahe_clip_limit"]
            if not isinstance(cl, (int, float)) or cl <= 0:
                raise ValueError(f"preprocessing.clahe_clip_limit must be positive, got {cl}")
        if "clahe_tile_size" in preproc:
            ts = preproc["clahe_tile_size"]
            if not isinstance(ts, int) or ts <= 0:
                raise ValueError(f"preprocessing.clahe_tile_size must be a positive integer, got {ts}")

    # --- confidence_adjustments (optional section) ---
    if "confidence_adjustments" in config:
        ca = config["confidence_adjustments"]
        for key in ("vlm_confirmation_bonus", "vlm_rejection_above_threshold",
                     "vlm_rejection_uncertain", "quality_penalty"):
            if key in ca and not isinstance(ca[key], (int, float)):
                raise ValueError(f"confidence_adjustments.{key} must be numeric")
