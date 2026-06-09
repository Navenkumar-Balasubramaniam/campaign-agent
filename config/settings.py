import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")
    GEMINI_IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    TEXT_MODEL = os.getenv(
        "OPENROUTER_TEXT_MODEL",
        "nvidia/nemotron-3-super-120b-a12b:free",
    )
    IMAGE_MODEL = os.getenv(
        "OPENROUTER_IMAGE_MODEL",
        "black-forest-labs/flux.2-klein-4b",
    )
    MAX_IMAGES_PER_CAMPAIGN = int(os.getenv("MAX_IMAGES_PER_CAMPAIGN", "1"))
    APP_NAME = os.getenv("APP_NAME", "AI Campaign Agent Demo")
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


settings = Settings()