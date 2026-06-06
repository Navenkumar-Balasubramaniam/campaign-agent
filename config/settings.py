import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    TEXT_MODEL = os.getenv(
        "OPENROUTER_TEXT_MODEL",
        "nvidia/nemotron-3-super-120b-a12b:free",
    )
    IMAGE_MODEL = os.getenv(
        "OPENROUTER_IMAGE_MODEL",
        "black-forest-labs/flux-2-klein",
    )
    MAX_IMAGES_PER_CAMPAIGN = int(os.getenv("MAX_IMAGES_PER_CAMPAIGN", "1"))
    APP_NAME = os.getenv("APP_NAME", "AI Campaign Agent Demo")
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


settings = Settings()