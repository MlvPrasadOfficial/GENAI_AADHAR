"""Load and validate pipeline configuration from YAML."""

from pathlib import Path

import yaml


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
    return config


def _validate(config: dict) -> None:
    """Minimal validation — ensure required sections exist."""
    required_sections = ["enhancement", "face", "similarity", "vlm_guard"]
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing required config section: '{section}'")

    sim = config["similarity"]
    if sim["uncertain_low"] >= sim["match_threshold"]:
        raise ValueError(
            f"uncertain_low ({sim['uncertain_low']}) must be < "
            f"match_threshold ({sim['match_threshold']})"
        )
