class ABTestAgent:
    def generate(self, copy_variants, visual_prompts, mockup_assets=None):
        mockup_assets = mockup_assets or []
        headlines = copy_variants["headlines"][:2]
        texts = copy_variants["primary_texts"][:2]
        prompts = visual_prompts[:2]

        tests = []
        labels = ["A", "B", "C", "D"]
        index = 0

        for headline in headlines:
            for visual in prompts:
                mockup = mockup_assets[index % len(mockup_assets)] if mockup_assets else {}
                tests.append(
                    {
                        "variant": labels[index],
                        "headline": headline,
                        "primary_text": texts[index % len(texts)],
                        "visual_prompt": visual,
                        "mockup_asset": mockup.get("format"),
                        "success_metric": "CTR",
                    }
                )
                index += 1

        return {"tests": tests}
