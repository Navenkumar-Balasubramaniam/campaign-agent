import time

import requests

from config.settings import settings

_MAX_RETRIES = 3


def _retry_after(data: dict) -> float:
    try:
        return float(
            data["error"]["metadata"].get("retry_after_seconds", 15)
        )
    except (KeyError, TypeError, ValueError):
        return 15.0


class OpenRouterClient:
    def __init__(self):
        if not settings.OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY is missing. "
                "Add it to your .env file."
            )

        self.headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "X-OpenRouter-Title": settings.APP_NAME,
        }

    def _post(self, payload: dict, timeout: int) -> dict:
        # Force non-streaming so we always get a complete JSON response
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
                    "OpenRouter connection dropped after "
                    f"{_MAX_RETRIES} retries. Check your network."
                )

            if response.status_code == 429:
                data = response.json()
                wait = _retry_after(data)
                if attempt < _MAX_RETRIES:
                    time.sleep(wait)
                    continue
                raise RuntimeError(
                    f"OpenRouter rate limit — still failing after "
                    f"{_MAX_RETRIES} retries. "
                    f"Try again in {int(wait)}s or use a paid key."
                )

            if not response.ok:
                raise RuntimeError(
                    f"OpenRouter error {response.status_code}: "
                    f"{response.text}"
                )

            return response.json()

        raise RuntimeError("Unexpected state in _post retry loop.")

    def generate_text(self, prompt: str) -> str:
        payload = {
            "model": settings.TEXT_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an expert digital advertising strategist. "
                        "Follow the output format in the user message exactly."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }

        data = self._post(payload, timeout=60)

        if "choices" not in data:
            error = data.get("error", data)
            if isinstance(error, dict):
                error = error.get("message", str(error))
            raise RuntimeError(f"OpenRouter error: {error}")

        return data["choices"][0]["message"].get("content", "")

    def generate_image(self, prompt: str):
        payload = {
            "model": settings.IMAGE_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "modalities": ["image"],
        }

        data = self._post(payload, timeout=120)

        if "choices" not in data:
            raise RuntimeError(
                f"Unexpected OpenRouter image response: {data}"
            )

        message = data["choices"][0]["message"]

        images = message.get("images", [])
        if images:
            return images[0].get("image_url", {}).get("url")

        content = message.get("content")
        if isinstance(content, list):
            for item in content:
                if item.get("type") == "image_url":
                    return item["image_url"]["url"]

        raise RuntimeError(
            f"No image found in OpenRouter response: {data}"
        )
