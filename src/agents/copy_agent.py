import json


class CopyAgent:
    """Generates ad copy variants. In live mode it grounds the copy on the
    brand voice and the headlines/text of the most relevant past campaigns;
    offline it uses the deterministic DemoClient copy."""

    def __init__(self, client):
        self.client = client

    def generate(self, brief, context=None):
        context = context or {}

        if self.client and getattr(self.client, "is_live", False):
            try:
                return self._ai_generate(brief, context)
            except Exception:
                pass

        # Offline / fallback path.
        if hasattr(self.client, "generate_copy"):
            return self.client.generate_copy(brief)

        return self._minimal_fallback(brief)

    def _ai_generate(self, brief, context):
        classification = context.get("classification", {})
        retrieved = context.get("retrieved", [])
        brand_guidelines = context.get("brand_guidelines", "")
        recommended_angle = context.get("recommended_angle") or classification.get("suggested_angle")

        examples = [
            {
                "angle": c.get("creative", {}).get("angle"),
                "headline": c.get("creative", {}).get("headline"),
                "primary_text": c.get("creative", {}).get("primary_text"),
                "ctr": c.get("results_summary", {}).get("ctr"),
            }
            for c in retrieved
        ]

        prompt = f"""
Write ad copy for a {brief.channel} campaign for {brief.brand}, in the brand voice.

BRAND VOICE / GUIDELINES:
{brand_guidelines[:1800]}

BRIEF:
Product: {brief.product}
Trigger: "{brief.campaign_trigger}"
Audience: {brief.audience}
Goal: {brief.goal}
Tone: {brief.tone}
CTA: {brief.cta}
Recommended creative angle (from historical data): {recommended_angle}

PAST CAMPAIGN COPY THAT PERFORMED WELL (match the voice, do not copy):
{json.dumps(examples, indent=2)}

Write 3 distinct variants. Return JSON with exactly these keys:
{{
  "headlines": ["3 short headlines"],
  "primary_texts": ["3 primary texts, 1-2 sentences each, on-brand"],
  "ctas": ["2 call-to-action options including '{brief.cta}'"]
}}
"""
        result = self.client.generate_json(prompt)
        result.setdefault("headlines", [])
        result.setdefault("primary_texts", [])
        result.setdefault("ctas", [brief.cta])
        return result

    def _minimal_fallback(self, brief):
        return {
            "headlines": [
                f"Discover {brief.brand}",
                f"{brief.product} for the moment",
                f"Choose {brief.brand}",
            ],
            "primary_texts": [
                f"Meet {brief.brand} {brief.product}, made for {brief.audience}.",
                f"A {brief.tone.lower()} reason to choose {brief.brand} right now.",
                f"Test which message lands best with a clear {brief.cta} step.",
            ],
            "ctas": [brief.cta, "Learn More"],
        }
