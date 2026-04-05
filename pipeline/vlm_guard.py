"""Vision LLM guard using Ollama for face verification.

Acts as a secondary verification layer invoked only when:
  - Cosine similarity is in the uncertain zone (0.40–0.60), OR
  - Image quality is low even with high cosine score

The VLM model is configurable (default: Qwen2.5-VL-7B).
Uses Ollama's HTTP API (Windows-native, no WSL required).
Degrades gracefully: returns VLMVerdict(same_person=None) if Ollama is unavailable.
"""

import json
import logging
import re
from dataclasses import dataclass
from typing import Literal
from urllib.parse import urlparse

import numpy as np
import requests

from utils.image_utils import bgr_to_base64_jpeg

logger = logging.getLogger(__name__)

VLM_PROMPT = """You are a biometric face verification assistant for KYC document checking.

You are given two face images:
- Image 1: face crop from an Aadhaar identity card (may be printed, low quality, grainy).
- Image 2: a live user selfie.

The automated embedding system computed a cosine similarity of {score:.3f}
(scale: 0.0 = completely different, 1.0 = identical, threshold for match is 0.60).

Compare ONLY structural facial features: eye spacing, nose bridge width, jawline shape, cheekbone structure, ear position.
IGNORE: image quality differences, lighting, skin tone, glasses, facial hair, makeup.

Respond ONLY with valid JSON (no other text):
{{"same_person": true, "confidence": "high", "reasoning": "one sentence explaining key matching feature", "quality_issues": "description or null"}}"""

AGE_GAP_PROMPT_SUPPLEMENT = """
IMPORTANT AGE CONTEXT: The Aadhaar face is estimated at age {aadhaar_age}, the selfie at age {selfie_age} (~{age_gap} year gap).
The Aadhaar photo was likely taken years ago and printed on the card.
Focus on AGE-STABLE structural features: eye socket shape, nose bridge profile, ear shape/position, inter-pupillary distance, forehead height ratio.
DISCOUNT age-VARIANT features: skin texture, wrinkle patterns, jawline definition, cheek fullness, hair changes."""

# Required keys in a valid VLM JSON response
_REQUIRED_VLM_KEYS = {"same_person", "confidence", "reasoning"}


@dataclass
class VLMVerdict:
    """Result from Vision LLM face verification."""

    same_person: bool | None   # None = VLM unavailable or parse failure
    confidence: Literal["high", "medium", "low", "unknown"]
    reasoning: str             # human-readable explanation
    quality_issues: str | None
    raw_response: str          # full VLM output for debugging

_VALID_CONFIDENCES = {"high", "medium", "low", "unknown"}


class VLMGuard:
    """Ollama-based face verification guard (model-agnostic).

    Usage:
        guard = VLMGuard(config)
        verdict = guard.verify(aadhaar_crop, selfie_crop, cosine_score=0.52)
    """

    def __init__(self, config: dict):
        cfg = config["vlm_guard"]
        self.enabled: bool = cfg["enabled"]
        self.model: str = cfg["model"]
        self.timeout_s: int = cfg["timeout_s"]
        self.temperature: float = cfg.get("temperature", 0.1)

        # Validate Ollama URL
        url = cfg["ollama_url"].rstrip("/")
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"Invalid Ollama URL scheme: {parsed.scheme!r} (expected http/https)")
        if not parsed.hostname:
            raise ValueError(f"Invalid Ollama URL: missing host in {url!r}")
        self.ollama_url: str = url

    def verify(
        self,
        aadhaar_crop: np.ndarray,
        selfie_crop: np.ndarray,
        cosine_score: float,
        aadhaar_age: int = 0,
        selfie_age: int = 0,
    ) -> VLMVerdict:
        """Send both face crops to Ollama LLaVA for biometric verification.

        Args:
            aadhaar_crop: Aligned 112x112 BGR face crop from Aadhaar card.
            selfie_crop: Aligned 112x112 BGR face crop from user selfie.
            cosine_score: The cosine similarity score for context.
            aadhaar_age: Estimated age from Aadhaar face (0 if unknown).
            selfie_age: Estimated age from selfie face (0 if unknown).

        Returns:
            VLMVerdict. same_person is None if Ollama is unreachable.
        """
        if not self.enabled:
            return VLMVerdict(
                same_person=None, confidence="unknown",
                reasoning="VLM guard disabled", quality_issues=None, raw_response=""
            )

        b64_aadhaar = bgr_to_base64_jpeg(aadhaar_crop)
        b64_selfie = bgr_to_base64_jpeg(selfie_crop)

        prompt = VLM_PROMPT.format(score=cosine_score)
        age_gap = abs(aadhaar_age - selfie_age)
        if age_gap > 3 and aadhaar_age > 0 and selfie_age > 0:
            prompt += AGE_GAP_PROMPT_SUPPLEMENT.format(
                aadhaar_age=aadhaar_age, selfie_age=selfie_age, age_gap=age_gap,
            )

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                    "images": [b64_aadhaar, b64_selfie],
                }
            ],
            "stream": False,
            "options": {"temperature": self.temperature},
        }

        # Free base64 strings before blocking on HTTP (can be several MB each)
        del b64_aadhaar, b64_selfie

        try:
            resp = requests.post(
                f"{self.ollama_url}/api/chat",
                json=payload,
                timeout=self.timeout_s,
            )
            resp.raise_for_status()
            raw_text = resp.json()["message"]["content"]
        except requests.ConnectionError:
            logger.warning("Ollama not reachable at %s", self.ollama_url)
            return VLMVerdict(
                same_person=None, confidence="unknown",
                reasoning="Ollama server unreachable",
                quality_issues=None, raw_response="",
            )
        except (requests.Timeout, requests.HTTPError) as e:
            logger.warning("Ollama HTTP error: %s", e)
            return VLMVerdict(
                same_person=None, confidence="unknown",
                reasoning="Ollama request failed (timeout or HTTP error)",
                quality_issues=None, raw_response="",
            )
        except (KeyError, ValueError) as e:
            logger.warning("Ollama response malformed: %s", e)
            return VLMVerdict(
                same_person=None, confidence="unknown",
                reasoning="Ollama returned unexpected response format",
                quality_issues=None, raw_response="",
            )

        return self._parse_response(raw_text)

    def _parse_response(self, raw_text: str) -> VLMVerdict:
        """Parse VLM JSON response with validated schema.

        Strategy 1: Direct JSON parse with required-key validation.
        Strategy 2: Regex fallback (only for same_person + confidence).
        Strategy 3: Give up → same_person=None.
        """
        # Strategy 1: direct JSON parse
        try:
            cleaned = raw_text.strip()
            if cleaned.startswith("```"):
                cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
                cleaned = re.sub(r"\s*```$", "", cleaned)

            data = json.loads(cleaned)

            # Validate required keys are present
            missing = _REQUIRED_VLM_KEYS - set(data.keys())
            if missing:
                logger.warning("VLM JSON missing required keys: %s", missing)

            raw_same = data.get("same_person")
            if isinstance(raw_same, bool):
                same_person = raw_same
            elif isinstance(raw_same, str):
                same_person = raw_same.lower() == "true"
            else:
                same_person = None

            # Normalize confidence to known values
            raw_conf = str(data.get("confidence", "unknown")).lower()
            confidence = raw_conf if raw_conf in _VALID_CONFIDENCES else "unknown"

            return VLMVerdict(
                same_person=same_person,
                confidence=confidence,
                reasoning=str(data.get("reasoning", "")),
                quality_issues=data.get("quality_issues"),
                raw_response=raw_text,
            )
        except (json.JSONDecodeError, AttributeError):
            pass

        # Strategy 2: regex fallback (strict — must find same_person field)
        logger.warning("VLM returned non-JSON, attempting regex parse")
        same_match = re.search(r'"same_person"\s*:\s*(true|false)', raw_text, re.IGNORECASE)
        if same_match:
            same_person = same_match.group(1).lower() == "true"
            conf_match = re.search(r'"confidence"\s*:\s*"(\w+)"', raw_text)
            raw_conf = conf_match.group(1).lower() if conf_match else "unknown"
            confidence = raw_conf if raw_conf in _VALID_CONFIDENCES else "unknown"
            return VLMVerdict(
                same_person=same_person, confidence=confidence,
                reasoning="(parsed via regex fallback)",
                quality_issues=None, raw_response=raw_text,
            )

        # Strategy 3: give up
        logger.warning("Could not parse VLM response: %s", raw_text[:200])
        return VLMVerdict(
            same_person=None, confidence="unknown",
            reasoning="Failed to parse VLM response",
            quality_issues=None, raw_response=raw_text,
        )
