class AssetAgent:
    def generate(self, brief):
        base_assets = [
            {
                "title": "Estrella bottle product reference",
                "asset_type": "Product reference",
                "source": "Wikimedia Commons",
                "source_url": "https://commons.wikimedia.org/wiki/File:Estrella2014.jpg",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Estrella2014.jpg",
                "license": "CC0 1.0 public domain dedication",
                "use_case": "Product-reference image for academic mockups and layout planning.",
                "note": "Use as a reference asset, not as official brand-approved artwork.",
            },
            {
                "title": "Friends at a beer bar",
                "asset_type": "Lifestyle reference",
                "source": "Unsplash",
                "source_url": "https://unsplash.com/photos/group-of-friends-at-the-cellar-bar-8LlEY7DEvWo",
                "image_url": "",
                "license": "Free to use under the Unsplash License",
                "use_case": "Mood reference for social, bar, and friendship campaign concepts.",
                "note": "Check the page before final use and avoid implying people endorse the brand.",
            },
            {
                "title": "Friends with beers at a bar",
                "asset_type": "Lifestyle reference",
                "source": "Pexels",
                "source_url": "https://www.pexels.com/photo/friends-with-beers-at-a-bar-3851576/",
                "image_url": "",
                "license": "Free to use under the Pexels License",
                "use_case": "Mood reference for warm pub and group-social creative routes.",
                "note": "Use as mock campaign inspiration and review licensing before real publishing.",
            },
        ]

        return {
            "asset_strategy": (
                f"Use a mix of product-reference and lifestyle-reference assets to build "
                f"{brief.brand} mock campaign concepts for {brief.channel}."
            ),
            "usage_note": (
                "These are academic mockup sources. For a real launch, use owned brand "
                "assets, approved product photography, and legally cleared model releases."
            ),
            "assets": base_assets,
        }
