class VisualAgent:
    def generate_prompts(self, brief):
        prompt_1 = (
            f"Professional {brief.channel} advertising poster for {brief.brand} {brief.product}. "
            f"Target audience: {brief.audience}. Goal: {brief.goal}. "
            f"Tone: {brief.tone}. Clean composition, premium lighting, clear empty space for ad text."
        )

        prompt_2 = (
            f"High-converting lifestyle ad visual for {brief.brand} {brief.product}. "
            f"Designed for {brief.audience}. {brief.tone} brand style. "
            f"Modern commercial photography, emotional appeal, suitable for {brief.channel}."
        )

        prompt_3 = (
            f"Minimal premium product-focused campaign visual for {brief.brand} {brief.product}. "
            f"Audience: {brief.audience}. Campaign goal: {brief.goal}. "
            f"Elegant layout, strong product focus, professional advertising style, no messy background."
        )

        return {
            "image_prompts": [prompt_1, prompt_2, prompt_3]
        }
