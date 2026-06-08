import os

import requests
from dotenv import load_dotenv


def main():
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise SystemExit("OPENROUTER_API_KEY is missing.")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "nvidia/nemotron-3-super-120b-a12b:free",
            "messages": [
                {
                    "role": "user",
                    "content": "Say hello",
                }
            ],
        },
        timeout=30,
    )

    print(response.status_code)
    print(response.text)


if __name__ == "__main__":
    main()
