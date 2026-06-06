class CopyAgent:
    def __init__(self, client):
        self.client = client

    def generate(self, brief):
        prompt = f"""
Return valid JSON only.

Create ad copy variants for this campaign.

Campaign:
Product: {brief.product}
Audience: {brief.audience}
Goal: {brief.goal}
Channel: {brief.channel}
Tone: {brief.tone}
CTA: {brief.cta}

Return this exact JSON structure:
{{
  "headlines": ["...", "...", "..."],
  "primary_texts": ["...", "...", "..."],
  "ctas": ["...", "..."]
}}
"""
        return self.client.generate_text(prompt)