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
        brand_profile = get_brand_profile(brand, brief)
        trigger_theme = self._trigger_theme(trigger, brief)

        return {
            "brand_profile": brand_profile,
            "trigger": trigger,
            "trigger_theme": trigger_theme,
            "campaign_name": f"{brand} — {trigger_theme['name']}",
            "objective": (
                f"React to this external trigger: '{trigger}'. "
                f"Create a {channel} campaign that turns the moment into "
                f"measurable {goal.lower()} outcomes."
            ),
            "target_insight": (
                f"{audience} are more likely to respond when the campaign "
                "feels timely, relevant, and connected to a real-world moment."
            ),
            "positioning": (
                f"Position {brand} {product} as the right choice for this "
                f"moment, using a {tone.lower()} tone aligned with the brand "
                f"profile: {brand_profile['tone']}"
            ),
            "message_pillars": [
                {
                    "pillar": "Moment trigger",
                    "message": trigger_theme["message"],
                },
                {
                    "pillar": f"{brand} fit",
                    "message": brand_profile["mission"],
                },
                {
                    "pillar": "Clear action",
                    "message": (
                        f"Use a direct {brief.cta} CTA for "
                        "conversion-focused variants."
                    ),
                },
            ],
            "content_plan": [
                {
                    "phase": "Launch",
                    "format": f"{channel} feed ad",
                    "concept": trigger_theme["feed_concept"],
                    "purpose": (
                        "Launch the timely campaign with a clear brand moment."
                    ),
                },
                {
                    "phase": "Engage",
                    "format": f"{channel} story",
                    "concept": trigger_theme["story_concept"],
                    "purpose": (
                        "Test whether the trigger creates fast engagement."
                    ),
                },
                {
                    "phase": "Convert",
                    "format": "Retargeting ad",
                    "concept": trigger_theme["retargeting_concept"],
                    "purpose": (
                        "Move interested viewers toward the CTA."
                    ),
                },
            ],
            "launch_checklist": [
                "Confirm all legal and regulatory requirements for the "
                "product category.",
                "Review all copy for accuracy and platform compliance.",
                "Prepare at least three creative variants before launch.",
                "Track CTR during early testing and conversion rate after "
                "the learning period.",
                "Shift budget toward the best-performing creative.",
            ],
        }

    def _trigger_theme(self, trigger, brief):
        brand = brief.brand
        product = brief.product
        cta = brief.cta
        t = trigger.lower()

        if any(w in t for w in [
            "sun", "hot", "weather", "park", "outdoor", "summer",
            "terrace", "beer garden",
        ]):
            return {
                "name": "Summer Moment",
                "message": (
                    f"Connect warm, outdoor moments with {brand} {product} "
                    "— a natural fit for social, feel-good occasions."
                ),
                "feed_concept": (
                    f"A sun-drenched feed ad with {brand} {product} front "
                    f"and centre, warm daylight, and a clear {cta} CTA."
                ),
                "story_concept": (
                    f"A vertical story that starts with the outdoor moment "
                    f"and ends with a clear plan: meet friends and choose "
                    f"{brand}."
                ),
                "retargeting_concept": (
                    f"A product-led reminder ad focused on {brand} {product},"
                    f" outdoor plans, and the {cta} CTA."
                ),
            }

        if any(w in t for w in [
            "event", "concert", "festival", "live", "show", "game",
        ]):
            return {
                "name": "Event Moment",
                "message": (
                    f"Connect {brand} {product} with the energy of live "
                    "events and memorable shared experiences."
                ),
                "feed_concept": (
                    f"A high-energy feed ad positioning {brand} as the brand"
                    f" of choice for event-goers, with a direct {cta} CTA."
                ),
                "story_concept": (
                    f"A fast-paced story creative that mirrors the excitement"
                    f" of the event and drives urgency around {cta}."
                ),
                "retargeting_concept": (
                    f"A follow-up ad reminding audiences why {brand} {product}"
                    f" fits the moment, with a {cta} message."
                ),
            }

        if any(w in t for w in [
            "holiday", "christmas", "new year", "celebration", "festive",
            "seasonal",
        ]):
            return {
                "name": "Celebration Moment",
                "message": (
                    f"Position {brand} {product} as the perfect companion "
                    "for seasonal celebrations and shared moments."
                ),
                "feed_concept": (
                    f"A warm, celebratory feed ad featuring {brand} {product}"
                    f" with a festive feel and a clear {cta} CTA."
                ),
                "story_concept": (
                    f"A seasonal story creative connecting {brand} to the "
                    "joy of the celebration moment."
                ),
                "retargeting_concept": (
                    f"A limited-time reminder ad leveraging seasonal urgency "
                    f"and driving the {cta} action."
                ),
            }

        if any(w in t for w in [
            "launch", "new", "release", "announce", "debut",
        ]):
            return {
                "name": "Launch Moment",
                "message": (
                    f"Introduce {brand} {product} to {brief.audience} with "
                    "a bold, attention-grabbing launch campaign."
                ),
                "feed_concept": (
                    f"A bold product-reveal feed ad that puts {brand} "
                    f"{product} in the spotlight with a clear {cta} CTA."
                ),
                "story_concept": (
                    f"A teaser-to-reveal story sequence that builds curiosity "
                    f"around {brand} and drives {cta} clicks."
                ),
                "retargeting_concept": (
                    f"A reminder ad for users who saw the launch creative but "
                    f"haven't yet taken the {cta} action."
                ),
            }

        # Generic fallback
        return {
            "name": "Moment Maker",
            "message": (
                f"Turn the external trigger into a timely social reason "
                f"to choose {brand} {product}."
            ),
            "feed_concept": (
                f"A feed ad that connects the trigger to a clear "
                f"{brand} product moment with a {cta} CTA."
            ),
            "story_concept": (
                f"A story ad that makes the trigger feel immediate "
                f"and shareable for {brand}."
            ),
            "retargeting_concept": (
                f"A direct reminder ad using {brand}'s strongest campaign "
                f"message and a {cta} CTA."
            ),
        }
