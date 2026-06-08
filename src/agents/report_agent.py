class ReportAgent:
    def generate(
        self,
        brief_summary,
        copy,
        visuals,
        budget,
        ab_tests,
        image_urls=None,
        strategy=None,
        mock_assets=None,
        mockups=None,
    ):
        image_urls = image_urls or []
        strategy = strategy or {}
        mock_assets = mock_assets or {"assets": []}
        mockups = mockups or {"assets": []}
        primary_metric = self._primary_metric(brief_summary["goal"])
        brand = brief_summary.get("brand", "the brand")

        recommendation_note = (
            f"This {brand} campaign is designed for {brief_summary['channel']} with the objective of "
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

        decision_rationale = [
            {
                "step": "Input interpretation",
                "input_signal": (
                    f"Product: {brief_summary['product']}; audience: "
                    f"{brief_summary['audience']}; goal: {brief_summary['goal']}; "
                    f"brand: {brand}."
                ),
                "decision": (
                    "Treat the brief as a paid social campaign and produce copy, visuals, "
                    "budget guidance, testing recommendations, and a launch-ready campaign plan."
                ),
            },
            {
                "step": "Creative direction",
                "input_signal": f"Requested tone: {brief_summary['tone']}.",
                "decision": (
                    "Generate multiple message routes so the marketing team can compare "
                    "benefit-led, audience-led, and action-led creative variants."
                ),
            },
            {
                "step": "Budget logic",
                "input_signal": (
                    f"Channel: {brief_summary['channel']}; total budget: "
                    f"{budget['total_budget']}; duration: {brief_summary['duration_days']} days."
                ),
                "decision": (
                    "Reserve most spend for reach or prospecting while keeping part of "
                    "the budget for retargeting and creative testing."
                ),
            },
            {
                "step": "Measurement plan",
                "input_signal": f"Campaign goal: {brief_summary['goal']}.",
                "decision": (
                    f"Use {primary_metric} as the main decision metric and move budget "
                    "toward the best-performing creative after early results."
                ),
            },
            {
                "step": "Asset planning",
                "input_signal": f"Brand context: {brand}; product: {brief_summary['product']}.",
                "decision": (
                    "Use free mock/reference assets for academic campaign planning, while "
                    "keeping real launch assets subject to brand and legal approval."
                ),
            },
        ]

        assumptions = [
            "The campaign is an early-stage academic prototype, not a live media plan.",
            "Audience and product details come from the user-provided brief.",
            "The trigger sentence is treated as the reason the campaign should happen now.",
            "Budget recommendations are rule-based and should be checked against real platform data before launch.",
            "Mock assets are used for academic demonstration and do not replace official brand-approved creative.",
        ]

        limitations = [
            "The prototype does not connect to live ad performance, CRM, or competitor data.",
            "Generated copy still needs human review for brand accuracy and platform policy compliance.",
            "Image generation may require a paid API, so the free demo mode focuses on text, strategy, and visual prompts.",
            "Free stock or Commons images may still need review for trademark, model-release, and brand-approval issues.",
        ]

        ethical_considerations = [
            "Avoid targeting vulnerable groups or making misleading product claims.",
            "Review age-sensitive categories, such as alcohol or health products, before publishing.",
            "For beer campaigns, target only users who are legally allowed to buy alcohol in the relevant market.",
            "Keep a human marketer responsible for final approval and campaign monitoring.",
        ]

        kpi_plan = {
            "primary_metric": primary_metric,
            "secondary_metrics": ["CTR", "Conversion Rate", "CPA"],
            "optimization_rule": (
                "Compare variants after an initial learning period, then shift budget "
                "toward the variant with the strongest primary metric and acceptable cost."
            ),
        }

        return {
            "campaign_pack": {
                "brief_summary": brief_summary,
                "recommendation_note": recommendation_note,
                "campaign_strategy": strategy,
                "decision_rationale": decision_rationale,
                "copy_variants": copy,
                "visual_concepts": visuals,
                "mock_assets": mock_assets,
                "mockup_assets": mockups,
                "generated_image_urls": image_urls,
                "budget_plan": budget,
                "budget_note": budget_note,
                "ab_test_plan": ab_tests,
                "ab_test_note": ab_test_note,
                "kpi_plan": kpi_plan,
                "assumptions": assumptions,
                "limitations": limitations,
                "ethical_considerations": ethical_considerations,
                "real_world_use": (
                    "A marketing team could use this agent to turn an initial brief into "
                    "a first campaign plan, then refine the output with real performance data."
                ),
                "launch_status": "Ready for academic demo review",
            }
        }

    def _primary_metric(self, goal):
        goal = goal.lower()

        if "awareness" in goal:
            return "Reach and CPM"
        if "lead" in goal:
            return "Cost per Lead"
        return "Conversion Rate and CPA"
