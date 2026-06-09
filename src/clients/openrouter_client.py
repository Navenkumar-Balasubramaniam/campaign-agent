import requests

from config.settings import settings
from src.utils.json_utils import extract_json


class OpenRouterClient:
    is_live = True

    def __init__(self):
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is missing. Add it to your .env file.")

        self.headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "X-OpenRouter-Title": settings.APP_NAME,
        }

    def generate_json(self, prompt: str, system: str | None = None):
        return self.generate_text(prompt, system=system)

    def generate_text(self, prompt: str, system: str | None = None):
        payload = {
            "model": settings.TEXT_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": system or (
                        "You are an expert digital advertising strategist. "
                        "Return ONLY valid JSON. No markdown. No explanation."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.3,
            "response_format": {"type": "json_object"},
        }

        response = requests.post(
            settings.OPENROUTER_URL,
            headers=self.headers,
            json=payload,
            timeout=60,
        )

        if not response.ok:
            raise RuntimeError(
                f"OpenRouter error {response.status_code}: {response.text}"
            )

        data = response.json()

        if "choices" not in data:
            error = data.get("error", data)
            if isinstance(error, dict):
                error = error.get("message", str(error))
            raise RuntimeError(f"OpenRouter error: {error}")

        message = data["choices"][0]["message"]
        content = message.get("content", "")

        return extract_json(content)

    def generate_image(self, prompt: str):
        payload = {
            "model": settings.IMAGE_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "modalities": ["image"],
        }

        response = requests.post(
            settings.OPENROUTER_URL,
            headers=self.headers,
            json=payload,
            timeout=120,
        )

        if not response.ok:
            raise RuntimeError(
                f"OpenRouter image error {response.status_code}: {response.text}"
            )

        data = response.json()

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