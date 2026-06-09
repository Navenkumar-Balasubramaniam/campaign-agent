_ALCOHOL_KEYWORDS = {
    "beer", "wine", "spirits", "alcohol", "lager", "ale",
    "whiskey", "whisky", "vodka", "gin", "rum", "cocktail",
    "liquor", "brew", "cider", "champagne", "prosecco",
}

_LIFESTYLE_SOURCES = [
    {
        "source": "Unsplash",
        "source_url": "https://unsplash.com",
        "license": "Free to use under the Unsplash License",
        "note": (
            "Search for images matching your campaign tone and audience. "
            "Avoid implying people in photos endorse the brand."
        ),
    },
    {
        "source": "Pexels",
        "source_url": "https://www.pexels.com",
        "license": "Free to use under the Pexels License",
        "note": (
            "Review licensing before real publishing. "
            "Check for model releases if faces are visible."
        ),
    },
]


def _is_alcohol(product):
    return any(kw in product.lower() for kw in _ALCOHOL_KEYWORDS)


class AssetAgent:
    def generate(self, brief):
        brand = brief.brand
        product = brief.product
        channel = brief.channel
        audience = brief.audience

        # Audience context for search suggestions
        audience_short = (
            audience.split(",")[0].strip() if audience else "target audience"
        )

        assets = [
            {
                "title": f"{brand} official product imagery",
                "asset_type": "Product reference",
                "source": f"{brand} press kit / brand team",
                "source_url": "",
                "image_url": "",
                "license": "Obtain directly from the brand",
                "use_case": (
                    f"Official {brand} {product} photography for campaign "
                    "layouts and creative production."
                ),
                "note": (
                    "Request press-kit imagery from the brand's marketing "
                    "team. Do not use unofficial product images in live ads."
                ),
            },
            {
                "title": f"Lifestyle reference — {audience_short}",
                "asset_type": "Lifestyle reference",
                "source": _LIFESTYLE_SOURCES[0]["source"],
                "source_url": _LIFESTYLE_SOURCES[0]["source_url"],
                "image_url": "",
                "license": _LIFESTYLE_SOURCES[0]["license"],
                "use_case": (
                    f"Mood and lifestyle imagery matching the {brand} "
                    f"campaign tone for {audience_short}."
                ),
                "note": _LIFESTYLE_SOURCES[0]["note"],
            },
            {
                "title": f"Social context reference — {channel}",
                "asset_type": "Lifestyle reference",
                "source": _LIFESTYLE_SOURCES[1]["source"],
                "source_url": _LIFESTYLE_SOURCES[1]["source_url"],
                "image_url": "",
                "license": _LIFESTYLE_SOURCES[1]["license"],
                "use_case": (
                    f"Social and contextual imagery for {brand} {channel} "
                    "creative routes."
                ),
                "note": _LIFESTYLE_SOURCES[1]["note"],
            },
        ]

        if _is_alcohol(product):
            assets.append({
                "title": "Responsible drinking imagery guidance",
                "asset_type": "Compliance reference",
                "source": "Drinkaware / platform ad policies",
                "source_url": "https://www.drinkaware.co.uk",
                "image_url": "",
                "license": "N/A — compliance reference only",
                "use_case": (
                    "Ensure all alcohol campaign imagery meets responsible "
                    "drinking guidelines and platform policies."
                ),
                "note": (
                    "Include a responsible drinking message in all alcohol "
                    "ads. Check Meta, Google, and local market policies "
                    "before launch."
                ),
            })

        return {
            "asset_strategy": (
                f"Use a combination of official {brand} product photography "
                f"and audience-relevant lifestyle imagery to build compelling "
                f"{channel} campaign concepts."
            ),
            "usage_note": (
                "These are reference sources for draft layouts. For a real "
                "launch, use owned brand assets, approved product photography,"
                " and legally cleared model releases."
            ),
            "assets": assets,
        }
