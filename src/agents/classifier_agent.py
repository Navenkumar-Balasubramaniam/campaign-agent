VALID_ANGLES = [
    "emotional-narrative",
    "lifestyle",
    "product-led",
    "purpose-sustainability",
    "music-culture",
]

VALID_SEASONS = ["summer", "autumn", "winter", "spring", "year-round"]


class ClassifierAgent:
    """Reads the free-text campaign trigger and turns it into structured tags
    the rest of the pipeline can route on (theme, season, urgency, angle, risk).
    Uses the live model when available, otherwise deterministic keyword rules."""

    def __init__(self, client=None):
        self.client = client

    def classify(self, brief):
        if self.client and getattr(self.client, "is_live", False):
            try:
                return self._ai_classify(brief)
            except Exception:
                # Never break the demo on a model/quota error.
                return self._rule_classify(brief)
        return self._rule_classify(brief)

    def _ai_classify(self, brief):
        prompt = f"""
Classify this marketing campaign trigger into structured tags.

Brand: {brief.brand}
Product: {brief.product}
Campaign trigger: "{brief.campaign_trigger}"
Goal: {brief.goal}
Audience: {brief.audience}

Return JSON with exactly these keys:
{{
  "themes": ["3-5 short lowercase theme tags, e.g. summer, friendship, nostalgia"],
  "season": "one of: summer, autumn, winter, spring, year-round",
  "urgency": "one of: high, medium, low",
  "suggested_angle": "one of: emotional-narrative, lifestyle, product-led, purpose-sustainability, music-culture",
  "risk_flags": ["compliance risks, e.g. alcohol, age-sensitive"],
  "rationale": "one sentence explaining the classification"
}}
"""
        result = self.client.generate_json(prompt)
        return self._normalise(result, brief)

    def _normalise(self, result, brief):
        season = str(result.get("season", "")).lower()
        if season not in VALID_SEASONS:
            season = self._rule_classify(brief)["season"]

        angle = str(result.get("suggested_angle", "")).lower()
        if angle not in VALID_ANGLES:
            angle = "lifestyle"

        themes = [str(t).lower() for t in result.get("themes", []) if str(t).strip()]
        risk_flags = [str(r).lower() for r in result.get("risk_flags", []) if str(r).strip()]
        if self._is_alcohol(brief) and "alcohol" not in risk_flags:
            risk_flags.append("alcohol")

        return {
            "themes": themes or self._rule_classify(brief)["themes"],
            "season": season,
            "urgency": str(result.get("urgency", "medium")).lower(),
            "suggested_angle": angle,
            "risk_flags": risk_flags,
            "rationale": result.get("rationale", ""),
            "method": "ai",
        }

    def _rule_classify(self, brief):
        trigger = brief.campaign_trigger.lower()
        product = brief.product.lower()
        goal = brief.goal.lower()

        season = "year-round"
        themes = []
        if any(w in trigger for w in ["sun", "hot", "summer", "beach", "park", "terrace", "heatwave"]):
            season = "summer"
            themes += ["summer", "outdoor", "social"]
        elif any(w in trigger for w in ["winter", "cold", "christmas", "festive", "snow"]):
            season = "winter"
            themes += ["winter", "festive"]
        elif any(w in trigger for w in ["spring", "easter"]):
            season = "spring"
            themes += ["spring"]
        elif any(w in trigger for w in ["autumn", "fall", "back to"]):
            season = "autumn"
            themes += ["autumn"]

        if any(w in trigger for w in ["friend", "together", "social", "party", "reunion"]):
            themes.append("friendship")
        if any(w in trigger for w in ["music", "festival", "concert", "song"]):
            themes.append("music")
        if any(w in trigger for w in ["sea", "ocean", "environment", "plastic", "sustainab", "planet"]):
            themes.append("sustainability")

        if "sustainability" in themes:
            angle = "purpose-sustainability"
        elif goal in ("sales", "lead generation"):
            angle = "product-led"
        else:
            angle = "emotional-narrative"

        risk_flags = []
        if self._is_alcohol(brief):
            risk_flags.append("alcohol")

        return {
            "themes": themes or ["social", "lifestyle"],
            "season": season,
            "urgency": "high" if season == "summer" else "medium",
            "suggested_angle": angle,
            "risk_flags": risk_flags,
            "rationale": "Keyword-based classification of the campaign trigger.",
            "method": "rules",
        }

    def _is_alcohol(self, brief):
        text = f"{brief.brand} {brief.product}".lower()
        return any(w in text for w in ["beer", "estrella", "lager", "wine", "spirit", "alcohol", "cerveza"])
