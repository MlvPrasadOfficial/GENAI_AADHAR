"""Vision LLM guard using Ollama + LLaVA for face verification.

Acts as a secondary verification layer invoked only when:
  - Cosine similarity is in the uncertain zone (0.40–0.60), OR
  - Image quality is low even with high cosine score

Uses Ollama's HTTP API (Windows-native, no WSL required).
Degrades gracefully: returns VLMVerdict(same_person=None) if Ollama is unavailable.
"""

import json
import logging
import re
from dataclasses import dataclass

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
IGNORE: image quality differences, lighting, skin tone, age differences up to 10 years, glasses, facial hair, makeup.

Respond ONLY with valid JSON (no other text):
{{"same_person": true, "confidence": "high", "reasoning": "one sentence explaining key matching feature", "quality_issues": "description or null"}}"""


@dataclass
class VLMVerdict:
    """Result from Vision LLM face verification."""

    same_person: bool | None   # None = VLM unavailable or parse failure
    confidence: str            # "high" | "medium" | "low" | "unknown"
    reasoning: str             # human-readable explanation
    quality_issues: str | None
    raw_response: str          # full VLM output for debugging


class VLMGuard:
    """Ollama LLaVA-based face verification guard.

    Usage:
        guard = VLMGuard(config)
        verdict = guard.verify(aadhaar_crop, selfie_crop, cosine_score=0.52)
    """

    def __init__(self, config: dict):
        cfg = config["vlm_guard"]
        self.enabled: bool = cfg["enabled"]
        self.ollama_url: str = cfg["ollama_url"].rstrip("/")
        self.model: str = cfg["model"]
        self.timeout_s: int = cfg["timeout_s"]
        self.temperature: float = cfg.get("temperature", 0.1)

    def verify(
        self,
        aadhaar_crop: np.ndarray,
        selfie_crop: np.ndarray,
        cosine_score: float,
    ) -> VLMVerdict:
        """Send both face crops to Ollama LLaVA for biometric verification.

        Args:
            aadhaar_crop: Aligned 112x112 BGR face crop from Aadhaar card.
            selfie_crop: Aligned 112x112 BGR face crop from user selfie.
            cosine_score: The cosine similarity score for context.

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
        """Parse VLM JSON response with fallback to regex matching."""
        # Strategy 1: direct JSON parse
        try:
            # Strip markdown code fences if present
            cleaned = raw_text.strip()
            if cleaned.startswith("```"):
                cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
                cleaned = re.sub(r"\s*```$", "", cleaned)

            data = json.loads(cleaned)
            raw_same = data.get("same_person")
            # Strict boolean check — reject string "true"/"false" or int 0/1
            if isinstance(raw_same, bool):
                same_person = raw_same
            elif isinstance(raw_same, str):
                same_person = raw_same.lower() == "true"
            else:
                same_person = None
            return VLMVerdict(
                same_person=same_person,
                confidence=str(data.get("confidence", "unknown")),
                reasoning=str(data.get("reasoning", "")),
                quality_issues=data.get("quality_issues"),
                raw_response=raw_text,
            )
        except (json.JSONDecodeError, AttributeError):
            pass

        # Strategy 2: regex fallback
        logger.warning("VLM returned non-JSON, attempting regex parse")
        same_match = re.search(r'"same_person"\s*:\s*(true|false)', raw_text, re.IGNORECASE)
        if same_match:
            same_person = same_match.group(1).lower() == "true"
            conf_match = re.search(r'"confidence"\s*:\s*"(\w+)"', raw_text)
            confidence = conf_match.group(1) if conf_match else "unknown"
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
