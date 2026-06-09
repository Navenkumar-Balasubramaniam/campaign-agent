"""Quick connectivity check for the Gemini API key.

Usage:
    1. Add GEMINI_API_KEY to your .env file.
    2. python scripts/check_gemini.py

Prints whether the key works, the model used, and a small JSON-mode response.
Kept outside the normal test suite because it makes a real (free-tier) API call.
"""
import sys
from pathlib import Path

# Make the project importable when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config.settings import settings  # noqa: E402


def main():
    if not settings.GEMINI_API_KEY:
        raise SystemExit(
            "GEMINI_API_KEY is missing. Add it to your .env file "
            "(free key at https://aistudio.google.com)."
        )

    if "your_gemini_api_key_here" in settings.GEMINI_API_KEY:
        raise SystemExit(
            "GEMINI_API_KEY is still the placeholder. Open .env and replace "
            "'your_gemini_api_key_here' with your real key, then save the file."
        )

    print(f"Key found (ends with ...{settings.GEMINI_API_KEY[-4:]}).")
    print(f"Model: {settings.GEMINI_MODEL}")

    try:
        from src.clients.gemini_client import GeminiClient
    except ImportError:
        raise SystemExit(
            "google-genai is not installed. Run: pip install -r requirements.txt"
        )

    client = GeminiClient()

    prompt = (
        'Return JSON only: {"status": "ok", "brand": "Estrella Damm", '
        '"angle": "one short suggested ad angle for a sunny summer day"}'
    )
    print("\nCalling Gemini in JSON mode...")
    result = client.generate_json(prompt)

    print("Parsed response:")
    print(result)

    if isinstance(result, dict) and result.get("status"):
        print("\nSUCCESS: Gemini key works and JSON mode parsed correctly.")
    else:
        print("\nGot a response but it was not the expected JSON shape. Key works though.")


if __name__ == "__main__":
    main()
