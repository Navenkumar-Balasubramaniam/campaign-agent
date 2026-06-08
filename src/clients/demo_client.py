class DemoClient:
    def generate_copy(self, brief):
        brand = brief.brand
        product = brief.product
        audience = brief.audience
        cta = brief.cta
        goal = brief.goal.lower()

        if "awareness" in goal:
            angle = "discover"
            benefit = "built for people who want something memorable"
        elif "lead" in goal:
            angle = "learn more about"
            benefit = "with a clear next step for interested prospects"
        else:
            angle = "try"
            benefit = "made to turn interest into action"

        return {
            "headlines": [
                f"{angle.title()} {brand}",
                f"{product} for good-vibes nights",
                f"Choose {brand} tonight",
            ],
            "primary_texts": [
                (
                    f"Meet {brand} {product}, {benefit}. This message is shaped for "
                    f"{audience} and designed to support a {brief.goal.lower()} campaign."
                ),
                (
                    f"Give {audience} a direct reason to engage with {brand}. "
                    f"The tone stays {brief.tone.lower()} while keeping the offer simple."
                ),
                (
                    f"Use this creative route to test whether the target audience responds better "
                    f"to product benefits, lifestyle appeal, or a direct {cta} message."
                ),
            ],
            "ctas": [cta, "Learn More"],
        }

    def generate_image(self, prompt: str):
        raise RuntimeError("Image generation requires OpenRouter API mode.")
