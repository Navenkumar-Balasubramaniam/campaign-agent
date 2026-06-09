import json

from src.brand_profiles import get_brand_profile


class StrategyAgent:
    """Builds the campaign strategy. In live mode it grounds the plan on the
    brand guidelines and the most relevant past campaigns; offline it falls
    back to a deterministic, trigger-aware template."""

    def __init__(self, client=None):
        self.client = client

    def generate(self, brief, context=None):
        context = context or {}
        classification = context.get("classification", {})
        retrieved = context.get("retrieved", [])
        brand_guidelines = context.get("brand_guidelines", "")
        brand_profile = get_brand_profile(brief.brand)
        grounded_on = [c.get("name") for c in retrieved]

        if self.client and getattr(self.client, "is_live", False):
            try:
                ai = self._ai_generate(brief, classification, retrieved, brand_guidelines)
                ai["brand_profile"] = brand_profile
                ai["trigger"] = brief.campaign_trigger
                ai["trigger_theme"] = {"name": classification.get("suggested_angle", "campaign")}
                ai["grounded_on"] = grounded_on
                return ai
            except Exception:
                pass

        return self._fallback(brief, classification, brand_profile, grounded_on, retrieved)

    def _ai_generate(self, brief, classification, retrieved, brand_guidelines):
        examples = [
            {
                "name": c.get("name"),
                "angle": c.get("creative", {}).get("angle"),
                "positioning": c.get("positioning"),
                "headline": c.get("creative", {}).get("headline"),
                "results": c.get("results_summary"),
            }
            for c in retrieved
        ]

        prompt = f"""
Create a paid-social campaign strategy for {brief.brand}, grounded in the brand
guidelines and the brand's most relevant past campaigns.

BRAND GUIDELINES:
{brand_guidelines[:2500]}

NEW BRIEF:
Product: {brief.product}
Trigger: "{brief.campaign_trigger}"
Audience: {brief.audience}
Goal: {brief.goal}
Channel: {brief.channel}
Tone: {brief.tone}
CTA: {brief.cta}

TRIGGER CLASSIFICATION: {json.dumps(classification)}

MOST RELEVANT PAST CAMPAIGNS (learn from what worked):
{json.dumps(examples, indent=2)}

Return JSON with exactly these keys:
{{
  "campaign_name": "short, on-brand campaign name",
  "objective": "1 sentence tying the trigger to the {brief.goal} goal",
  "target_insight": "1 sentence audience insight",
  "positioning": "1 sentence positioning aligned to the brand guidelines",
  "historical_insight": "1 sentence on what the past campaigns suggest for this one",
  "message_pillars": [{{"pillar": "...", "message": "..."}}],
  "content_plan": [{{"phase": "Launch/Engage/Convert", "format": "...", "concept": "...", "purpose": "..."}}],
  "launch_checklist": ["...", "..."]
}}
"""
        result = self.client.generate_json(prompt)
        # Guarantee the keys the UI reads.
        result.setdefault("campaign_name", f"{brief.brand} Campaign")
        result.setdefault("message_pillars", [])
        result.setdefault("content_plan", [])
        result.setdefault("launch_checklist", [])
        result.setdefault("historical_insight", "")
        return result

    def _fallback(self, brief, classification, brand_profile, grounded_on, retrieved):
        brand = brief.brand
        goal = brief.goal
        channel = brief.channel
        tone = brief.tone
        trigger = brief.campaign_trigger
        trigger_theme = self._trigger_theme(trigger)

        historical_insight = ""
        if retrieved:
            top = retrieved[0]
            historical_insight = (
                f"The most comparable past campaign was '{top.get('name')}' "
                f"({top.get('creative', {}).get('angle')} angle), which the strategy builds on."
            )

        return {
            "brand_profile": brand_profile,
            "trigger": trigger,
            "trigger_theme": trigger_theme,
            "grounded_on": grounded_on,
            "historical_insight": historical_insight,
            "campaign_name": f"{brand} {trigger_theme['name']}",
            "objective": (
                f"React to this external trigger: '{trigger}'. Create a {channel} "
                f"campaign that turns the moment into measurable {goal.lower()} outcomes."
            ),
            "target_insight": (
                f"{brief.audience} are more likely to respond when the campaign feels timely, "
                "social, easy to share, and connected to a real-world moment."
            ),
            "positioning": (
                f"Position {brand} as the beer for this moment, using a {tone.lower()} "
                f"tone while staying aligned with the brand profile: {brand_profile['tone']}"
            ),
            "message_pillars": [
                {"pillar": "Moment trigger", "message": trigger_theme["message"]},
                {"pillar": "Brand fit", "message": brand_profile["mission"]},
                {
                    "pillar": "Simple action",
                    "message": f"Use a direct {brief.cta} CTA for conversion-focused variants.",
                },
            ],
            "content_plan": [
                {
                    "phase": "Launch",
                    "format": f"{channel} feed ad",
                    "concept": trigger_theme["feed_concept"],
                    "purpose": "Launch the timely campaign with a clear brand moment.",
                },
                {
                    "phase": "Engage",
                    "format": f"{channel} story",
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
