from src.agents.report_agent import ReportAgent


def test_report_agent_combines_sections():
    result = ReportAgent().generate(
        brief_summary={"product": "Tea"},
        copy={"headlines": ["H1"], "primary_texts": ["T1"], "ctas": ["Buy"]},
        visuals={"image_prompts": ["Prompt 1"]},
        budget={"daily_budget": 10, "budget_split": []},
        ab_tests={"tests": []},
        image_url="https://example.com/image.png",
    )

    assert result["campaign_pack"]["brief_summary"]["product"] == "Tea"
    assert result["campaign_pack"]["generated_image_url"] == "https://example.com/image.png"