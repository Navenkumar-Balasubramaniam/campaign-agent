import base64
import time

import requests

from config.settings import settings
from src.utils.json_utils import extract_json

_MAX_RETRIES = 3


def _retry_after(data: dict) -> float:
    """Pull the suggested wait (seconds) out of a 429 body, default 15s."""
    try:
        return float(data["error"]["metadata"].get("retry_after_seconds", 15))
    except (KeyError, TypeError, ValueError):
        return 15.0


class OpenRouterClient:
    """AI client backed by OpenRouter.

    The retry/backoff in ``_post`` keeps the multi-step pipeline reliable —
    shared models can rate-limit (429), and the pipeline fires several calls
    in a row.
    """

    is_live = True

    def __init__(self):
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is missing. Add it to your .env file.")

        self.headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "X-OpenRouter-Title": settings.APP_NAME,
        }

    def _post(self, payload: dict, timeout: int) -> dict:
        """POST with retries for 429 rate limits and dropped connections.

        Free models throttle aggressively, so this backs off and retries
        instead of failing the whole campaign run on the first 429.
        """
        # Force non-streaming so we always get one complete JSON response.
        payload = {**payload, "stream": False}

        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                response = requests.post(
                    settings.OPENROUTER_URL,
                    headers=self.headers,
                    json=payload,
                    timeout=timeout,
                )
            except requests.exceptions.ChunkedEncodingError:
                if attempt < _MAX_RETRIES:
                    time.sleep(3)
                    continue
                raise RuntimeError(
                    f"OpenRouter connection dropped after {_MAX_RETRIES} retries. "
                    "Check your network."
                )

            if response.status_code == 429:
                data = response.json()
                wait = _retry_after(data)
                if attempt < _MAX_RETRIES:
                    time.sleep(wait)
                    continue
                raise RuntimeError(
                    f"OpenRouter rate limit — still failing after {_MAX_RETRIES} "
                    f"retries. Try again in {int(wait)}s."
                )

            if not response.ok:
                raise RuntimeError(
                    f"OpenRouter error {response.status_code}: {response.text}"
                )

            return response.json()

        raise RuntimeError("Unexpected state in _post retry loop.")

    def generate_json(self, prompt: str, system: str | None = None):
        """Send a prompt and return parsed JSON (what every grounded agent needs)."""
        payload = {
            "model": settings.TEXT_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": system
                    or (
                        "You are an expert digital advertising strategist. "
                        "Return ONLY valid JSON. No markdown. No explanation."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
            "response_format": {"type": "json_object"},
        }

        data = self._post(payload, timeout=60)

        if "choices" not in data:
            error = data.get("error", data)
            if isinstance(error, dict):
                error = error.get("message", str(error))
            raise RuntimeError(f"OpenRouter error: {error}")

        content = data["choices"][0]["message"].get("content", "")
        return extract_json(content)

    def generate_text(self, prompt: str, system: str | None = None):
        # Backwards-compatible alias used by the older CopyAgent path.
        return self.generate_json(prompt, system=system)

    def generate_image(self, prompt: str, reference_images=None):
        """Generate an image, optionally grounded on uploaded reference images.

        When ``reference_images`` are supplied (``{"data": bytes,
        "mime_type": str}`` dicts) they are attached as multimodal input so the
        model can match the real product.
        """
        if reference_images:
            content = [{"type": "text", "text": prompt}]
            for ref in reference_images:
                encoded = base64.b64encode(ref["data"]).decode("ascii")
                content.append(
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{ref['mime_type']};base64,{encoded}"},
                    }
                )
        else:
            content = prompt

        payload = {
            "model": settings.IMAGE_MODEL,
            "messages": [{"role": "user", "content": content}],
            "modalities": ["image"],
        }

        data = self._post(payload, timeout=120)

        if "choices" not in data:
            raise RuntimeError(f"Unexpected OpenRouter image response: {data}")

        message = data["choices"][0]["message"]

        images = message.get("images", [])
        if images:
            return images[0].get("image_url", {}).get("url")

        content = message.get("content")
        if isinstance(content, list):
            for item in content:
                if item.get("type") == "image_url":
                    return item["image_url"]["url"]

        raise RuntimeError(f"No image found in OpenRouter response: {data}")
