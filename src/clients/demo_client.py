class DemoClient:
    """Offline, deterministic fallback. No API key or network needed.

    Used as the safe demo path and whenever a live model is unavailable.
    Agents check `is_live` to decide between AI generation and templates.
    """

    is_live = False

    def generate_copy(self, brief):
        brand = brief.brand
        product = brief.product
        audience = brief.audience
        cta = brief.cta
        goal = brief.goal.lower()
        trigger = brief.campaign_trigger.lower()

        if "awareness" in goal:
            angle = "discover"
            benefit = "built for people who want something memorable"
        elif "lead" in goal:
            angle = "learn more about"
            benefit = "with a clear next step for interested prospects"
        else:
            angle = "try"
            benefit = "made to turn interest into action"

        if any(word in trigger for word in ["sun", "park", "beer garden", "hot"]):
            headlines = [
                "Sun's Out. Estrella Out.",
                "Cold Estrella, Warm Days",
                "Meet Where The Sun Is",
            ]
            primary_texts = [
                (
                    "The sun is out, so the plan is simple: find a terrace, beer garden, "
                    "or park spot and enjoy a cold Estrella responsibly."
                ),
                (
                    f"Turn good weather into a social moment for {audience}. "
                    "This route keeps the tone bright, Mediterranean, and easy to act on."
                ),
                (
                    f"A direct {cta} version for people already thinking about outdoor plans, "
                    "cold drinks, and meeting friends."
                ),
            ]
            return {"headlines": headlines, "primary_texts": primary_texts, "ctas": [cta, "Find Your Spot"]}

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

    def generate_image(self, prompt: str, reference_images=None):
        raise RuntimeError("Image generation requires OpenRouter API mode.")
