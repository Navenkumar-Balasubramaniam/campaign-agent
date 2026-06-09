class ReportAgent:
    def generate(
        self,
        brief_summary,
        copy,
        visuals,
        budget,
        ab_tests,
        image_urls=None,
        image_errors=None,
        strategy=None,
        mock_assets=None,
        mockups=None,
        classification=None,
        retrieved=None,
        decision=None,
        benchmarks=None,
    ):
        image_urls = image_urls or []
        image_errors = image_errors or []
        strategy = strategy or {}
        mock_assets = mock_assets or {"assets": []}
        mockups = mockups or {"assets": []}
        classification = classification or {}
        retrieved = retrieved or []
        decision = decision or {}
        brand = brief_summary.get("brand", "the brand")

        primary_metric = decision.get("primary_metric") or self._primary_metric(
            brief_summary["goal"]
        )

        recommendation_note = (
            f"This {brand} campaign is designed for {brief_summary['channel']} with the objective of "
            f"driving {brief_summary['goal'].lower()}. "
            f"{decision.get('historical_evidence', '')} "
            f"The recommended creative angle is '{decision.get('recommended_angle', 'the strongest tested route')}'. "
            f"{decision.get('winning_variant_logic', '')}"
        ).strip()

        budget_note = (
            f"The total budget of {brief_summary['budget']} is distributed across prospecting, "
            f"retargeting, and creative testing. {decision.get('budget_tilt', '')}"
        ).strip()

        ab_test_note = (
            "The A/B test structure compares different headline and visual combinations. "
            f"Lead with the '{decision.get('recommended_angle', 'best')}' angle and use "
            f"{primary_metric} as the early decision metric, then optimise on conversion economics."
        )

        # Prefer the decision agent's data-grounded reasoning; fall back to a
        # generic rationale only if it produced none.
        decision_rationale = decision.get("rationale_points") or self._default_rationale(
            brief_summary, budget, primary_metric, brand
        )

        # Slim, display-friendly view of the retrieved campaigns.
        grounded_campaigns = [
            {
                "name": c.get("name"),
                "year": c.get("year"),
                "angle": c.get("creative", {}).get("angle"),
                "results_summary": c.get("results_summary", {}),
                "match_score": c.get("_score"),
            }
            for c in retrieved
        ]

        historical_benchmarks = decision.get("by_angle", {})

        assumptions = [
            "The campaign is an early-stage academic prototype, not a live media plan.",
            "Audience and product details come from the user-provided brief.",
            "The trigger sentence is treated as the reason the campaign should happen now.",
            "Historical results in this prototype are realistic but synthetic; replace them with real Ads Manager data before relying on the numbers.",
            "Mock assets are used for academic demonstration and do not replace official brand-approved creative.",
        ]

        limitations = [
            "The prototype does not connect to a live ad account; benchmarks come from a static, synthetic dataset.",
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
        for flag in classification.get("risk_flags", []):
            note = f"Flagged risk from the trigger: '{flag}' — review against platform and local rules."
            if note not in ethical_considerations:
                ethical_considerations.append(note)

        kpi_plan = {
            "primary_metric": primary_metric,
            "secondary_metrics": ["CTR", "Conversion Rate", "CPA", "ROAS"],
            "optimization_rule": (
                "Compare variants after an initial learning period, then shift budget "
                "toward the variant with the strongest primary metric and acceptable cost."
            ),
            "expected_performance": decision.get("expected_performance", {}),
        }

        return {
            "campaign_pack": {
                "brief_summary": brief_summary,
                "recommendation_note": recommendation_note,
                "trigger_classification": classification,
                "campaign_strategy": strategy,
                "grounded_campaigns": grounded_campaigns,
                "historical_benchmarks": historical_benchmarks,
                "decision": decision,
                "decision_rationale": decision_rationale,
                "copy_variants": copy,
                "visual_concepts": visuals,
                "mock_assets": mock_assets,
                "mockup_assets": mockups,
                "generated_image_urls": image_urls,
                "generated_image_errors": image_errors,
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
                    "a first campaign plan grounded in their own past campaigns, then refine "
                    "the output with live performance data."
                ),
                "launch_status": "Ready for academic demo review",
            }
        }

    def _default_rationale(self, brief_summary, budget, primary_metric, brand):
        return [
            {
                "step": "Input interpretation",
                "evidence": (
                    f"Product: {brief_summary['product']}; audience: "
                    f"{brief_summary['audience']}; goal: {brief_summary['goal']}."
                ),
                "decision": (
                    "Treat the brief as a paid social campaign and produce copy, visuals, "
                    "budget guidance, testing recommendations, and a launch-ready plan."
                ),
            },
            {
                "step": "Measurement plan",
                "evidence": f"Campaign goal: {brief_summary['goal']}.",
                "decision": (
                    f"Use {primary_metric} as the main decision metric and move budget "
                    "toward the best-performing creative after early results."
                ),
            },
        ]

    def _primary_metric(self, goal):
        goal = goal.lower()

        if "awareness" in goal:
            return "Reach and CPM"
        if "lead" in goal:
            return "Cost per Lead"
        return "Conversion Rate and CPA"
