ESTRELLA_PROFILE = {
    "brand": "Estrella",
    "brand_context": "Barcelona-born Mediterranean beer brand.",
    "tone": "Warm, Mediterranean, social, summery, relaxed, responsible.",
    "mission": (
        "Celebrate Mediterranean lifestyle moments while keeping the message "
        "responsible, social, and respectful of the environment."
    ),
    "must_include": [
        "Mediterranean lifestyle",
        "social moments",
        "sunlight or outdoor atmosphere when relevant",
        "clear product presence",
        "responsible alcohol messaging",
    ],
    "avoid": [
        "excessive drinking",
        "underage targeting",
        "unsafe behavior",
        "claims that imply health benefits",
    ],
    "source_notes": [
        "Damm corporate campaign pages reference Mediterranean lifestyle.",
        "Estrella Damm is positioned as a Barcelona/Mediterranean beer brand.",
    ],
}


def get_brand_profile(brand, brief=None):
    if brand.strip().lower() == "estrella":
        return ESTRELLA_PROFILE

    tone = brief.tone if brief else "authentic and engaging"
    product = brief.product if brief else f"{brand} product"
    audience = brief.audience if brief else "target consumers"
    goal = brief.goal if brief else "brand growth"
    channel = brief.channel if brief else "social media"

    return {
        "brand": brand,
        "brand_context": (
            f"{brand} — offering {product} to {audience} via {channel}."
        ),
        "tone": tone,
        "mission": (
            f"Drive {goal.lower()} by connecting {brand} with {audience} "
            "through honest, compelling campaigns."
        ),
        "must_include": [
            "clear product presence",
            "clear CTA",
            "brand name visibility",
            "audience-relevant messaging",
        ],
        "avoid": [
            "misleading claims",
            "unsafe or irresponsible behaviour",
            "generic filler copy that ignores the brief",
        ],
        "source_notes": [
            f"Profile derived from the campaign brief for {brand}."
        ],
    }
