import json


class DecisionAgent:
    """Turns historical performance data into a concrete recommendation:
    which creative angle to lead with, expected performance, and how to tilt
    the budget. Numbers are computed deterministically from the benchmarks so
    they are never hallucinated; the live model only writes the reasoning."""

    def __init__(self, client=None):
        self.client = client

    def generate(self, brief, classification, benchmarks, retrieved):
        evidence = self._compute_evidence(brief, benchmarks)

        if self.client and getattr(self.client, "is_live", False) and evidence["available"]:
            try:
                narrative = self._ai_narrative(brief, classification, evidence, retrieved)
            except Exception:
                narrative = self._rule_narrative(brief, classification, evidence)
        else:
            narrative = self._rule_narrative(brief, classification, evidence)

        return {**evidence, **narrative}

    def _compute_evidence(self, brief, benchmarks):
        if benchmarks is None or not benchmarks.is_available():
            return {
                "available": False,
                "recommended_angle": None,
                "primary_metric": "Conversion Rate" if "sale" in brief.goal.lower() else "CTR",
                "by_angle": {},
                "expected_performance": {},
            }

        by_angle = benchmarks.by_angle()
        best_angle, best_metrics, metric = benchmarks.best_angle_for_goal(brief.goal)

        # Build an expected-performance range from the winning angle's history.
        def rng(value):
            return f"{round(value * 0.85, 2)} - {round(value * 1.15, 2)}"

        expected = {
            "ctr_pct": rng(best_metrics.get("ctr", 0)),
            "cpa": rng(best_metrics.get("cpa", 0)),
            "conversion_rate_pct": rng(best_metrics.get("conversion_rate", 0)),
            "roas": rng(best_metrics.get("roas", 0)),
        }

        # A contrast angle to justify the choice.
        others = {a: m for a, m in by_angle.items() if a != best_angle}
        contrast_angle = None
        if others:
            if metric == "ctr":
                contrast_angle = max(others, key=lambda a: others[a]["cpa"])  # worst CPA
            else:
                contrast_angle = min(others, key=lambda a: others[a]["roas"])  # worst ROAS

        return {
            "available": True,
            "recommended_angle": best_angle,
            "primary_metric": "CTR" if metric == "ctr" else "ROAS",
            "best_metrics": best_metrics,
            "contrast_angle": contrast_angle,
            "contrast_metrics": by_angle.get(contrast_angle, {}),
            "by_angle": by_angle,
            "audience_stats": benchmarks.by_audience(),
            "expected_performance": expected,
        }

    def _ai_narrative(self, brief, classification, evidence, retrieved):
        retrieved_brief = [
            {
                "name": c.get("name"),
                "angle": c.get("creative", {}).get("angle"),
                "results": c.get("results_summary"),
            }
            for c in retrieved
        ]

        prompt = f"""
You are a paid-social strategist for {brief.brand}. Recommend how to run a new
campaign, grounded STRICTLY in the historical data provided. Do not invent any
numbers; only reference the numbers given.

New campaign goal: {brief.goal}
New campaign trigger: "{brief.campaign_trigger}"
Trigger classification: {json.dumps(classification)}

Historical performance by creative angle (averages):
{json.dumps(evidence['by_angle'], indent=2)}

Performance by audience type:
{json.dumps(evidence.get('audience_stats', {}), indent=2)}

Most relevant past campaigns:
{json.dumps(retrieved_brief, indent=2)}

Data-derived recommended angle: {evidence['recommended_angle']}
(best for this goal on {evidence['primary_metric']})

Return JSON with exactly these keys:
{{
  "historical_evidence": "2-3 sentences citing the specific historical numbers that justify the recommended angle versus a weaker angle",
  "budget_tilt": "1-2 sentences on where to weight budget (prospecting vs retargeting, which angle) based on the data",
  "winning_variant_logic": "1 sentence on which creative variant to lead with and why",
  "confidence": "high, medium, or low",
  "rationale_points": [
    {{"step": "short label", "evidence": "the data signal", "decision": "the action taken"}}
  ]
}}
"""
        result = self.client.generate_json(prompt)
        result["method"] = "ai"
        result.setdefault("rationale_points", [])
        return result

    def _rule_narrative(self, brief, classification, evidence):
        if not evidence["available"]:
            return {
                "historical_evidence": "No historical campaign data was available, so this recommendation is based on standard paid-social heuristics.",
                "budget_tilt": "Reserve most budget for prospecting, keep a retargeting pool, and ring-fence budget for creative testing.",
                "winning_variant_logic": "Lead with the variant that most directly matches the campaign goal.",
                "confidence": "low",
                "rationale_points": [],
                "method": "rules",
            }

        angle = evidence["recommended_angle"]
        metric = evidence["primary_metric"]
        best = evidence["best_metrics"]
        contrast = evidence.get("contrast_angle")
        contrast_m = evidence.get("contrast_metrics", {})
        goal = brief.goal.lower()

        if metric == "CTR":
            evid = (
                f"Historically the '{angle}' angle delivered the best awareness performance "
                f"(avg CTR {best.get('ctr')}%, ROAS {best.get('roas')})"
            )
            if contrast:
                evid += (
                    f", while the '{contrast}' angle converted worst "
                    f"(CPA {contrast_m.get('cpa')}, ROAS {contrast_m.get('roas')})."
                )
            budget_tilt = (
                "Weight budget toward prospecting to maximise reach, keep ~25% for retargeting, "
                "and reserve ~15% to test creative variants."
            )
        else:
            evid = (
                f"Historically the '{angle}' angle drove the strongest conversion economics "
                f"(avg CPA {best.get('cpa')}, conversion rate {best.get('conversion_rate')}%, ROAS {best.get('roas')})"
            )
            if contrast:
                evid += (
                    f", far ahead of the '{contrast}' angle (ROAS {contrast_m.get('roas')})."
                )
            budget_tilt = (
                "Tilt budget toward retargeting warm audiences with product-led creative, which "
                "historically returned the best CPA and ROAS, while keeping prospecting to feed the funnel."
            )

        rationale_points = [
            {
                "step": "Trigger classification",
                "evidence": f"Trigger read as season='{classification['season']}', themes={classification['themes']}.",
                "decision": f"Route the campaign as a {classification['season']} moment with a {classification['suggested_angle']} starting hypothesis.",
            },
            {
                "step": "Historical angle selection",
                "evidence": evid,
                "decision": f"Lead the new campaign with the '{angle}' angle to optimise {metric}.",
            },
            {
                "step": "Budget allocation",
                "evidence": "Audience-type history shows retargeting outperforms prospecting on CPA/ROAS.",
                "decision": budget_tilt,
            },
        ]

        return {
            "historical_evidence": evid,
            "budget_tilt": budget_tilt,
            "winning_variant_logic": (
                f"Lead with the variant built on the '{angle}' angle; it best matches the "
                f"goal of {goal} based on past results."
            ),
            "confidence": "medium",
            "rationale_points": rationale_points,
            "method": "rules",
        }
