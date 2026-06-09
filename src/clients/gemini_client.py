import base64

from config.settings import settings
from src.utils.json_utils import extract_json


class GeminiClient:
    """Live AI client backed by Google's Gemini API (free tier friendly).

    Uses the unified `google-genai` SDK. JSON mode keeps the structured
    output the agents expect. Get a free API key from https://aistudio.google.com.
    """

    is_live = True

    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing. Add it to your .env file "
                "(get a free key at https://aistudio.google.com)."
            )

        # Imported lazily so offline demo mode never needs the package installed.
        from google import genai

        self._genai = genai
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_MODEL

    def generate_json(self, prompt: str, system: str | None = None):
        """Send a prompt and return parsed JSON as a dict."""
        from google.genai import types

        system_instruction = system or (
            "You are an expert digital marketing strategist for a paid social "
            "advertising team. Ground every recommendation in the brand context and "
            "the historical campaign data you are given. Return ONLY valid JSON, "
            "no markdown, no commentary."
        )

        response = self.client.models.generate_content(
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

    def generate_image(self, prompt: str):
        """Generate one campaign image and return it as a base64 data URL.

        Uses the paid image model, so it only runs when the user opts in.
        Adds a responsible-use framing for age-sensitive (e.g. alcohol) brands.
        """
        from google.genai import types

        safe_prompt = (
            f"{prompt}\n\n"
            "Style: tasteful, premium advertising photography. Do not depict anyone "
            "drinking or anyone who looks under 25. Keep it brand-safe and suitable "
            "for a general audience."
        )

        response = self.client.models.generate_content(
            model=settings.GEMINI_IMAGE_MODEL,
            contents=safe_prompt,
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
