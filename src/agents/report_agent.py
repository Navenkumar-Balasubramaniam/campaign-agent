class ReportAgent:
    def generate(self, brief_summary, copy, visuals, budget, ab_tests, image_url=None):
        return {
            "campaign_pack": {
                "brief_summary": brief_summary,
                "copy_variants": copy,
                "visual_concepts": visuals,
                "budget_plan": budget,
                "ab_test_plan": ab_tests,
                "generated_image_url": image_url,
                "launch_status": "Ready for academic demo review",
            }
        }