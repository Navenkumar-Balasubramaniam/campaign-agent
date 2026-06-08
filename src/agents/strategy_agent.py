class StrategyAgent:
    def generate(self, brief):
        brand = brief.brand
        product = brief.product
        audience = brief.audience
        goal = brief.goal
        channel = brief.channel
        tone = brief.tone

        return {
            "campaign_name": f"{brand} Social Pour",
            "objective": (
                f"Create a {channel} campaign that turns interest in {product} "
                f"into measurable {goal.lower()} outcomes."
            ),
            "target_insight": (
                f"{audience} are more likely to respond to beer advertising when "
                "the message feels social, easy to share, and connected to real moments."
            ),
            "positioning": (
                f"Position {brand} as a beer for relaxed social occasions, using a "
                f"{tone.lower()} tone while keeping the campaign responsible and age-aware."
            ),
            "message_pillars": [
                {
                    "pillar": "Social energy",
                    "message": "Show the beer as part of shared moments with friends.",
                },
                {
                    "pillar": "Product appeal",
                    "message": "Keep the bottle, glass, or pour visually clear in every concept.",
                },
                {
                    "pillar": "Simple action",
                    "message": f"Use a direct {brief.cta} CTA for conversion-focused variants.",
                },
            ],
            "content_plan": [
                {
                    "phase": "Launch",
                    "format": "Instagram feed ad",
                    "concept": "Hero product shot with clear CTA and clean brand framing.",
                    "purpose": "Establish the campaign and test product-led response.",
                },
                {
                    "phase": "Engage",
                    "format": "Instagram story",
                    "concept": "Lifestyle scene with friends, warm light, and short copy.",
                    "purpose": "Test social/lifestyle relevance with the target audience.",
                },
                {
                    "phase": "Convert",
                    "format": "Retargeting ad",
                    "concept": "Direct offer-style creative using the strongest headline.",
                    "purpose": "Move interested viewers toward the sales CTA.",
                },
            ],
            "launch_checklist": [
                "Confirm legal drinking age targeting for the market.",
                "Review all copy for responsible alcohol messaging.",
                "Prepare at least three creative variants before launch.",
                "Track CTR during early testing and conversion rate after learning period.",
                "Shift budget toward the best-performing creative.",
            ],
        }
