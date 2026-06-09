"""Generate ONE Gemini image to verify image generation works.

Usage:
    python scripts/check_gemini_image.py

Makes a single paid image call (a few cents) and saves the result to
scripts/_gemini_test_image.png so you can open and inspect it. Kept out of the
test suite because it costs money.
"""
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config.settings import settings  # noqa: E402


def main():
    if not settings.GEMINI_API_KEY or "your_gemini_api_key_here" in settings.GEMINI_API_KEY:
        raise SystemExit("Set a real GEMINI_API_KEY in .env first.")

    from src.clients.gemini_client import GeminiClient

    client = GeminiClient()
    print(f"Image model: {settings.GEMINI_IMAGE_MODEL}")
    print("Generating one test image (this is a paid call)...")

    prompt = (
        "Professional Instagram advertising poster for Estrella Damm Mediterranean beer. "
        "A sunny terrace by the sea, warm golden-hour light, a cold beer bottle on a table, "
        "clean empty space at the top for ad text. Premium commercial photography."
    )

    data_url = client.generate_image(prompt)

    header, _, b64 = data_url.partition(",")
    out = Path(__file__).resolve().parent / "_gemini_test_image.png"
    out.write_bytes(base64.b64decode(b64))

    print(f"SUCCESS: image saved to {out}")
    print(f"Data URL header: {header}")


if __name__ == "__main__":
    main()
