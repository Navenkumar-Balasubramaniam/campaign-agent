import base64
import requests

from config.settings import settings
from src.utils.json_utils import extract_json


class OpenRouterClient:
    def __init__(self):
        if not settings.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is missing. Add it to your .env file.")

        self.headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "X-OpenRouter-Title": settings.APP_NAME,
        }

    def generate_text(self, prompt: str):
        payload = {
            "model": settings.TEXT_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert digital advertising strategist. Always return valid JSON only.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": 0.7,
        }

        response = requests.post(
            settings.OPENROUTER_URL,
            headers=self.headers,
            json=payload,
            timeout=60,
        )
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]
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
        response.raise_for_status()

        data = response.json()
        message = data["choices"][0]["message"]

        images = message.get("images", [])
        if images:
            return images[0].get("image_url", {}).get("url")

        content = message.get("content")
        if isinstance(content, list):
            for item in content:
                if item.get("type") == "image_url":
                    return item["image_url"]["url"]

        return None