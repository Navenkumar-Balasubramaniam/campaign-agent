class VisualAgent:
    def generate_prompts(self, brief):
        prompt_1 = (
            f"Professional {brief.channel} advertising poster for {brief.product}. "
            f"Target audience: {brief.audience}. Goal: {brief.goal}. "
            f"Tone: {brief.tone}. Clean composition, premium lighting, clear empty space for ad text."
        )

        prompt_2 = (
            f"High-converting social media campaign visual for {brief.product}. "
            f"Designed for {brief.audience}. {brief.tone} brand style. "
            f"Modern commercial photography, strong product focus, suitable for {brief.channel}."
        )

        return {
            "image_prompts": [prompt_1, prompt_2]
        }