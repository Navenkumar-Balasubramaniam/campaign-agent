import base64
import time

from config.settings import settings
from src.utils.json_utils import extract_json

_MAX_RETRIES = 4
_BACKOFFS = [5, 15, 30]  # seconds to wait before each retry


def _is_rate_limit(exc: Exception) -> bool:
    """True if the error is a 429 / quota-exhausted that's worth retrying."""
    code = getattr(exc, "code", None)
    text = f"{code} {exc}".upper()
    return code == 429 or "429" in text or "RESOURCE_EXHAUSTED" in text


class GeminiClient:
    """AI client backed by Google's Gemini API.

    Uses the unified `google-genai` SDK. JSON mode keeps the structured
    output the agents expect. Works with an API key or with Vertex AI
    (selected via .env).
    """

    is_live = True

    def __init__(self):
        # Imported lazily so offline demo mode never needs the package installed.
        from google import genai

        self._genai = genai

        if settings.USE_VERTEX:
            # Vertex mode authenticates via Application Default Credentials
            # (no API key). Requires `gcloud auth application-default login`
            # and the Vertex AI API enabled on the project.
            if not settings.GOOGLE_CLOUD_PROJECT:
                raise ValueError(
                    "GOOGLE_GENAI_USE_VERTEXAI is on but GOOGLE_CLOUD_PROJECT is "
                    "missing. Set it in .env to your Google Cloud project ID."
                )
            self.client = genai.Client(
                vertexai=True,
                project=settings.GOOGLE_CLOUD_PROJECT,
                location=settings.GOOGLE_CLOUD_LOCATION,
            )
        else:
            if not settings.GEMINI_API_KEY:
                raise ValueError(
                    "GEMINI_API_KEY is missing. Add it to your .env file "
                    "(get a key at https://aistudio.google.com), or switch to "
                    "Vertex mode with GOOGLE_GENAI_USE_VERTEXAI=true."
                )
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

        self.model = settings.GEMINI_MODEL

    def _generate(self, **kwargs):
        """Call generate_content, backing off and retrying on 429/quota errors.

        The pipeline fires several calls in quick succession (and up to a few
        images), which can briefly exceed the per-minute quota. Retrying with
        backoff recovers instead of failing the whole run.
        """
        for attempt in range(_MAX_RETRIES):
            try:
                return self.client.models.generate_content(**kwargs)
            except Exception as exc:  # noqa: BLE001
                if not _is_rate_limit(exc) or attempt == _MAX_RETRIES - 1:
                    raise
                time.sleep(_BACKOFFS[min(attempt, len(_BACKOFFS) - 1)])

    def generate_json(self, prompt: str, system: str | None = None):
        """Send a prompt and return parsed JSON as a dict."""
        from google.genai import types

        system_instruction = system or (
            "You are an expert digital marketing strategist for a paid social "
            "advertising team. Ground every recommendation in the brand context and "
            "the historical campaign data you are given. Return ONLY valid JSON, "
            "no markdown, no commentary."
        )

        response = self._generate(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.4,
                response_mime_type="application/json",
            ),
        )

        return extract_json(response.text)

    def generate_text(self, prompt: str):
        # Backwards-compatible alias used by the older CopyAgent path.
        return self.generate_json(prompt)

    def generate_image(self, prompt: str, reference_images=None):
        """Generate one campaign image and return it as a base64 data URL.

        Uses the image model, so it only runs when the user opts in.
        Adds a responsible-use framing for age-sensitive (e.g. alcohol) brands.
        When ``reference_images`` are supplied (a list of
        ``{"data": bytes, "mime_type": str}`` dicts), they are passed to the
        model so the generated visual matches the real product/brand.
        """
        from google.genai import types

        if reference_images:
            safe_prompt = (
                f"{prompt}\n\n"
                "Use the attached reference image(s) as the visual ground truth for "
                "the product and brand. Keep the product's real appearance, "
                "packaging, and logo consistent with the references.\n\n"
                "Style: tasteful, premium advertising photography. Do not depict "
                "anyone drinking or anyone who looks under 25. Keep it brand-safe "
                "and suitable for a general audience."
            )
            contents = [
                types.Part.from_bytes(data=ref["data"], mime_type=ref["mime_type"])
                for ref in reference_images
            ]
            contents.append(safe_prompt)
        else:
            safe_prompt = (
                f"{prompt}\n\n"
                "Style: tasteful, premium advertising photography. Do not depict anyone "
                "drinking or anyone who looks under 25. Keep it brand-safe and suitable "
                "for a general audience."
            )
            contents = safe_prompt

        response = self._generate(
            model=settings.GEMINI_IMAGE_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
        )

        candidates = getattr(response, "candidates", None) or []
        for candidate in candidates:
            content = getattr(candidate, "content", None)
            for part in getattr(content, "parts", None) or []:
                inline = getattr(part, "inline_data", None)
                if inline and getattr(inline, "data", None):
                    data = inline.data
                    mime = getattr(inline, "mime_type", "image/png")
                    if isinstance(data, bytes):
                        encoded = base64.b64encode(data).decode("ascii")
                    else:
                        encoded = data  # already a base64 string
                    return f"data:{mime};base64,{encoded}"

        raise RuntimeError(
            "Gemini returned no image (the prompt may have been refused by safety filters)."
        )
