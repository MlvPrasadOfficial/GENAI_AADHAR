"""Custom exceptions for the Aadhaar KYC face matching pipeline."""


class PipelineError(Exception):
    """Base exception for all pipeline errors."""


class NoFaceDetectedError(PipelineError):
    """Raised when no face is found in an image."""

    def __init__(self, source: str, detail: str = ""):
        self.source = source  # "aadhaar" or "selfie"
        self.detail = detail
        msg = f"No face detected in {source} image"
        if detail:
            msg += f": {detail}"
        super().__init__(msg)


class EnhancementError(PipelineError):
    """Raised when image enhancement fails."""


class VLMUnavailableError(PipelineError):
    """Raised when Ollama / VLM server is unreachable."""
