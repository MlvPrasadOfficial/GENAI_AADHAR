"""Vision LLM guard using Qwen2.5-VL-7B-Instruct for face verification.

Acts as a secondary verification layer invoked only when:
  - Cosine similarity is in the uncertain zone (0.40-0.60), OR
  - Image quality is low even with high cosine score

Uses HuggingFace transformers for local inference (no Ollama).
Degrades gracefully: returns VLMVerdict(same_person=None) if model is unavailable.
"""

import json
import logging
import re
from dataclasses import dataclass
from typing import Literal

import numpy as np

from utils.image_utils import bgr_to_base64_jpeg

logger = logging.getLogger(__name__)

VLM_PROMPT = """You are a biometric face verification assistant for KYC document checking.

You are given two face images:
- Image 1: face crop from an Aadhaar identity card. It is a PRINTED photograph on a plastic card — expect geometric distortion from printing, compression artifacts, blur, colour shift, and uneven lighting.
- Image 2: a live user selfie taken with a phone camera in natural conditions.

The automated embedding system computed a cosine similarity of {score:.3f}
(scale: 0.0 = completely different, 1.0 = identical, threshold for match is 0.60).

HOW TO COMPARE — focus on STABLE identity cues that survive aging AND printing:
  - Overall face shape (oval, round, square, heart)
  - Nose SHAPE (straight / curved / hooked, narrow / wide tip) — NOT exact measurements
  - Eye shape (almond, round, hooded) and relative placement — NOT exact spacing in pixels
  - Eyebrow shape and thickness pattern
  - Moles, scars, or distinctive marks
  - Facial hair pattern (beard/moustache shape, even if fullness differs)
  - Ear shape and lobe type when visible
  - Hairline pattern at the forehead

WHAT YOU MUST IGNORE on the Aadhaar image:
  - Exact inter-pupillary distance in pixels (printing + perspective distort this)
  - Exact eye-socket spacing in pixels (same reason)
  - Pixel-level landmark geometry (unreliable on printed cards)
  - Image quality, lighting, skin tone, colour cast
  - Glasses, makeup, wrinkles, weight changes, hair length / style / colour
  - Age-related changes (softer jawline, greying, minor puffiness)

DECISION RULE:
  - If the STABLE identity cues above are consistent → same_person=true, even if surface appearance differs.
  - Only return same_person=false when you see a FUNDAMENTALLY different face: different face shape AND different nose shape AND different eyebrow pattern, OR obviously different gender / ethnicity.
  - When evidence is ambiguous or mixed, PREFER same_person=true. The embedding system already handles the clear negatives; your job here is to save real users from being rejected on low-quality prints.

Respond ONLY with valid JSON (no other text):
{{"same_person": true, "confidence": "high", "reasoning": "one sentence focusing on stable identity cues (not IPD / landmark measurements)", "quality_issues": "description or null"}}"""

AGE_GAP_PROMPT_SUPPLEMENT = """
CRITICAL AGE CONTEXT: The Aadhaar face is estimated at age {aadhaar_age}, the selfie at age {selfie_age} (~{age_gap} year gap).
The Aadhaar photo was taken YEARS AGO and printed on a card — expect significant appearance changes.
This is NORMAL for KYC verification. A {age_gap}-year gap WILL cause visible aging differences.
You MUST focus ONLY on age-invariant bone geometry: eye socket shape, nose bridge, ear shape, inter-pupillary distance.
You MUST IGNORE all age-variant features: skin texture, wrinkles, jawline softening, cheek fullness, hair.
If bone structure matches, answer same_person=true — appearance changes from aging are EXPECTED, not evidence of a different person."""

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
    """HuggingFace Qwen2.5-VL-7B-Instruct face verification guard.

    Usage:
        guard = VLMGuard(config)
        verdict = guard.verify(aadhaar_crop, selfie_crop, cosine_score=0.52)
    """

    def __init__(self, config: dict):
        cfg = config["vlm_guard"]
        self.enabled: bool = cfg["enabled"]
        self.model_path: str = cfg.get("model_path", "Qwen/Qwen2.5-VL-7B-Instruct")
        self.temperature: float = cfg.get("temperature", 0.1)
        self.max_new_tokens: int = cfg.get("max_new_tokens", 256)
        self._model = None
        self._processor = None

    def load(self):
        """Load the Qwen2.5-VL model and processor from local path or HuggingFace."""
        if not self.enabled:
            logger.info("VLM guard disabled, skipping model load")
            return

        try:
            from transformers import Qwen2_5_VLForConditionalGeneration, AutoProcessor
            import torch

            logger.info("Loading VLM model from %s ...", self.model_path)

            self._processor = AutoProcessor.from_pretrained(
                self.model_path,
                trust_remote_code=True,
            )

            device = "cuda" if torch.cuda.is_available() else "cpu"
            dtype = torch.float16 if device == "cuda" else torch.float32

            self._model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
                self.model_path,
                torch_dtype=dtype,
                device_map="auto" if device == "cuda" else None,
                trust_remote_code=True,
            )

            if device == "cpu":
                self._model = self._model.to(device)

            self._model.eval()
            logger.info("VLM model loaded on %s (%s)", device, dtype)

        except ImportError:
            logger.warning("transformers or qwen-vl-utils not installed. VLM guard disabled.")
            self.enabled = False
        except Exception as e:
            logger.warning("Failed to load VLM model: %s. VLM guard disabled.", e)
            self.enabled = False

    def verify(
        self,
        aadhaar_crop: np.ndarray,
        selfie_crop: np.ndarray,
        cosine_score: float,
        aadhaar_age: int = 0,
        selfie_age: int = 0,
    ) -> VLMVerdict:
        """Send both face crops to local VLM for biometric verification.

        Args:
            aadhaar_crop: Aligned 112x112 BGR face crop from Aadhaar card.
            selfie_crop: Aligned 112x112 BGR face crop from user selfie.
            cosine_score: The cosine similarity score for context.
            aadhaar_age: Estimated age from Aadhaar face (0 if unknown).
            selfie_age: Estimated age from selfie face (0 if unknown).

        Returns:
            VLMVerdict. same_person is None if model is unavailable.
        """
        if not self.enabled:
            return VLMVerdict(
                same_person=None, confidence="unknown",
                reasoning="VLM guard disabled", quality_issues=None, raw_response=""
            )

        if self._model is None or self._processor is None:
            return VLMVerdict(
                same_person=None, confidence="unknown",
                reasoning="VLM model not loaded",
                quality_issues=None, raw_response="",
            )

        prompt = VLM_PROMPT.format(score=cosine_score)
        age_gap = abs(aadhaar_age - selfie_age)
        if age_gap > 2 and aadhaar_age > 0 and selfie_age > 0:
            prompt += AGE_GAP_PROMPT_SUPPLEMENT.format(
                aadhaar_age=aadhaar_age, selfie_age=selfie_age, age_gap=age_gap,
            )

        try:
            import torch
            import cv2
            from PIL import Image
            import io

            # Convert BGR crops to PIL Images
            aadhaar_rgb = cv2.cvtColor(aadhaar_crop, cv2.COLOR_BGR2RGB)
            selfie_rgb = cv2.cvtColor(selfie_crop, cv2.COLOR_BGR2RGB)
            pil_aadhaar = Image.fromarray(aadhaar_rgb)
            pil_selfie = Image.fromarray(selfie_rgb)

            # Build messages in Qwen2.5-VL chat format
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": pil_aadhaar},
                        {"type": "image", "image": pil_selfie},
                        {"type": "text", "text": prompt},
                    ],
                }
            ]

            # Process inputs
            text = self._processor.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
            inputs = self._processor(
                text=[text],
                images=[pil_aadhaar, pil_selfie],
                padding=True,
                return_tensors="pt",
            )
            inputs = inputs.to(self._model.device)

            # Generate
            with torch.no_grad():
                output_ids = self._model.generate(
                    **inputs,
                    max_new_tokens=self.max_new_tokens,
                    temperature=self.temperature,
                    do_sample=self.temperature > 0,
                )

            # Decode only generated tokens
            generated_ids = output_ids[0][inputs.input_ids.shape[1]:]
            raw_text = self._processor.decode(generated_ids, skip_special_tokens=True)

        except Exception as e:
            logger.warning("VLM inference failed: %s", e)
            return VLMVerdict(
                same_person=None, confidence="unknown",
                reasoning=f"VLM inference error: {e}",
                quality_issues=None, raw_response="",
            )

        return self._parse_response(raw_text)

    def _parse_response(self, raw_text: str) -> VLMVerdict:
        """Parse VLM JSON response with validated schema.

        Strategy 1: Direct JSON parse with required-key validation.
        Strategy 2: Regex fallback (only for same_person + confidence).
        Strategy 3: Give up -> same_person=None.
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
