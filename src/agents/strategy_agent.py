from src.brand_profiles import get_brand_profile


class StrategyAgent:
    def generate(self, brief):
        brand = brief.brand
        product = brief.product
        audience = brief.audience
        goal = brief.goal
        channel = brief.channel
        tone = brief.tone
        trigger = brief.campaign_trigger
        brand_profile = get_brand_profile(brand)
        trigger_theme = self._trigger_theme(trigger)

        return {
            "brand_profile": brand_profile,
            "trigger": trigger,
            "trigger_theme": trigger_theme,
            "campaign_name": f"{brand} {trigger_theme['name']}",
            "objective": (
                f"React to this external trigger: '{trigger}'. Create a {channel} "
                f"campaign that turns the moment into measurable {goal.lower()} outcomes."
            ),
            "target_insight": (
                f"{audience} are more likely to respond when the campaign feels timely, "
                "social, easy to share, and connected to a real-world moment."
            ),
            "positioning": (
                f"Position {brand} as the beer for this moment, using a {tone.lower()} "
                f"tone while staying aligned with the brand profile: {brand_profile['tone']}"
            ),
            "message_pillars": [
                {
                    "pillar": "Moment trigger",
                    "message": trigger_theme["message"],
                },
                {
                    "pillar": "Estrella fit",
                    "message": brand_profile["mission"],
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
                    "concept": trigger_theme["feed_concept"],
                    "purpose": "Launch the timely campaign with a clear brand moment.",
                },
                {
                    "phase": "Engage",
                    "format": "Instagram story",
                    "concept": trigger_theme["story_concept"],
                    "purpose": "Test whether the trigger creates fast social engagement.",
                },
                {
                    "phase": "Convert",
                    "format": "Retargeting ad",
                    "concept": trigger_theme["retargeting_concept"],
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

    def _trigger_theme(self, trigger):
        trigger_lower = trigger.lower()

        if any(word in trigger_lower for word in ["sun", "hot", "weather", "park"]):
            return {
                "name": "Sun's Out Sessions",
                "message": (
                    "Connect sunny weather with responsible outdoor social moments: "
                    "beer gardens, parks, terraces, and cold refreshment."
                ),
                "feed_concept": (
                    "A sunny beer garden or park-inspired feed ad with a cold Estrella, "
                    "warm daylight, and a simple sales CTA."
                ),
                "story_concept": (
                    "A vertical story creative that starts with sunshine and ends with "
                    "a clear plan: meet friends, choose a spot, enjoy an Estrella responsibly."
                ),
                "retargeting_concept": (
                    "A product-led reminder ad focused on cold beer, outdoor plans, "
                    "and the Shop Now CTA."
                ),
            }

        return {
            "name": "Moment Maker",
            "message": "Turn the external trigger into a timely social reason to choose the brand.",
            "feed_concept": "A feed ad that connects the trigger to a clear product moment.",
            "story_concept": "A story ad that makes the trigger feel immediate and shareable.",
            "retargeting_concept": "A direct reminder ad using the strongest campaign message.",
        }
