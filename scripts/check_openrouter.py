"""Quick connectivity check for the free OpenRouter tier.

Usage:
    1. Add OPENROUTER_API_KEY to your .env file (https://openrouter.ai/keys).
    2. python scripts/check_openrouter.py

Confirms the free text model returns valid JSON (what the grounded pipeline
needs). Kept outside the test suite because it makes a real API call.
Image generation is NOT checked here because it costs money (~$0.014/image).
"""
import sys
from pathlib import Path

# Make the project importable when run as a script.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config.settings import settings  # noqa: E402


def main():
    if not settings.OPENROUTER_API_KEY:
        raise SystemExit(
            "OPENROUTER_API_KEY is missing. Add it to your .env file "
            "(create a key at https://openrouter.ai/keys)."
        )

    if "your_openrouter_api_key_here" in settings.OPENROUTER_API_KEY:
        raise SystemExit(
            "OPENROUTER_API_KEY is still the placeholder. Open .env and replace "
            "'your_openrouter_api_key_here' with your real key, then save the file."
        )

    print(f"Key found (ends with ...{settings.OPENROUTER_API_KEY[-4:]}).")
    print(f"Text model: {settings.TEXT_MODEL}")

    from src.clients.openrouter_client import OpenRouterClient

    client = OpenRouterClient()

    prompt = (
        'Return JSON only: {"status": "ok", "brand": "Estrella Damm", '
        '"angle": "one short suggested ad angle for a sunny summer day"}'
    )
    print("\nCalling OpenRouter free text model in JSON mode...")
    result = client.generate_json(prompt)

    print("Parsed response:")
    print(result)

    if isinstance(result, dict) and result.get("status"):
        print("\nSUCCESS: free OpenRouter text works and JSON parsed correctly.")
    else:
        print("\nGot a response but not the expected JSON shape. Key works though.")


if __name__ == "__main__":
    main()
