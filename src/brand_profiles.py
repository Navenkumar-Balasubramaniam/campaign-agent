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
        "Damm corporate campaign pages reference Mediterranean lifestyle and environmental protection.",
        "Estrella Damm is commonly positioned as a Barcelona/Mediterranean beer brand.",
    ],
}


def get_brand_profile(brand):
    if brand.strip().lower() == "estrella":
        return ESTRELLA_PROFILE

    return {
        "brand": brand,
        "brand_context": "Custom campaign brand.",
        "tone": "Use the tone supplied in the brief.",
        "mission": "Create a clear, responsible campaign aligned with the brief.",
        "must_include": ["clear product presence", "clear CTA", "responsible messaging"],
        "avoid": ["misleading claims", "unsafe behavior"],
        "source_notes": [],
    }
