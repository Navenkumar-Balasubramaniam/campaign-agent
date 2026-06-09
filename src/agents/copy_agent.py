import re


class CopyAgent:
    def __init__(self, client):
        self.client = client

    def generate(self, brief):
        prompt = f"""You are writing ad copy for a campaign. \
Output ONLY the lines below, no extra text.

Brand: {brief.brand}
Product: {brief.product}
Campaign Trigger: {brief.campaign_trigger}
Target Audience: {brief.audience}
Campaign Goal: {brief.goal}
Channel: {brief.channel}
Tone: {brief.tone}
CTA: {brief.cta}

Write three variants. Use exactly this format:

HEADLINE_1: <headline>
HEADLINE_2: <headline>
HEADLINE_3: <headline>
BODY_1: <primary text, 1-2 sentences>
BODY_2: <primary text, 1-2 sentences>
BODY_3: <primary text, 1-2 sentences>
CTA_1: {brief.cta}
CTA_2: <alternative CTA>
"""
        raw = self.client.generate_text(prompt)
        return self._parse(raw, brief.cta)

    @staticmethod
    def _parse(text: str, fallback_cta: str) -> dict:
        def extract(label):
            matches = re.findall(
                rf"^{label}:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE
            )
            return [m.strip() for m in matches]

        headlines = extract("HEADLINE_[123]")
        bodies = extract("BODY_[123]")
        ctas = extract("CTA_[12]")

        if not headlines:
            headlines = extract("HEADLINE")
        if not bodies:
            bodies = extract("BODY")
        if not ctas:
            ctas = [fallback_cta, "Learn More"]

        if not headlines or not bodies:
            raise ValueError(
                f"Could not parse ad copy from model response:\n{text}"
            )

        return {
            "headlines": headlines[:3],
            "primary_texts": bodies[:3],
            "ctas": ctas[:2],
        }
