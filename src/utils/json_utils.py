import json
import re


def extract_json(text: str):
    if isinstance(text, dict):
        return text

    if not text:
        raise ValueError("Model returned empty content.")

    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError(f"No valid JSON found in model response: {text}")

    return json.loads(match.group(0))