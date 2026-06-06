class ABTestAgent:
    def generate(self, copy_variants, visual_prompts):
        headlines = copy_variants["headlines"][:2]
        texts = copy_variants["primary_texts"][:2]
        prompts = visual_prompts[:2]

        tests = []
        labels = ["A", "B", "C", "D"]
        index = 0

        for headline in headlines:
            for visual in prompts:
                tests.append(
                    {
                        "variant": labels[index],
                        "headline": headline,
                        "primary_text": texts[index % len(texts)],
                        "visual_prompt": visual,
                        "success_metric": "CTR",
                    }
                )
                index += 1

        return {"tests": tests}