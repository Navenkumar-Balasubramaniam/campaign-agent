class ReportAgent:
    def generate(self, brief_summary, copy, visuals, budget, ab_tests, image_urls=None):
        image_urls = image_urls or []

        recommendation_note = (
            f"This campaign is designed for {brief_summary['channel']} with the objective of "
            f"driving {brief_summary['goal'].lower()}. The recommended direction is to use a "
            f"{brief_summary['tone'].lower()} tone that directly connects with "
            f"{brief_summary['audience']}. The campaign should begin with multiple creative "
            f"variants and then shift budget toward the best-performing ad after early results."
        )

        budget_note = (
            f"The total budget of {brief_summary['budget']} is distributed across prospecting, "
            f"retargeting, and creative testing. This structure helps the campaign reach new users "
            f"while also reserving spend for audiences who have already shown interest."
        )

        ab_test_note = (
            "The A/B test structure compares different headline and visual combinations. "
            "The recommended success metric is CTR in the early stage, followed by conversion rate "
            "once enough traffic has been collected."
        )

        return {
            "campaign_pack": {
                "brief_summary": brief_summary,
                "recommendation_note": recommendation_note,
                "copy_variants": copy,
                "visual_concepts": visuals,
                "generated_image_urls": image_urls,
                "budget_plan": budget,
                "budget_note": budget_note,
                "ab_test_plan": ab_tests,
                "ab_test_note": ab_test_note,
                "launch_status": "Ready for academic demo review",
            }
        }