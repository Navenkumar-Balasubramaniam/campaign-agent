from src.agents.report_agent import ReportAgent


def test_report_agent_combines_sections():
    result = ReportAgent().generate(
        brief_summary={
            "brand": "Estrella",
            "product": "Tea",
            "audience": "Wellness shoppers",
            "goal": "Sales",
            "budget": 1000,
            "channel": "Instagram",
            "tone": "Calm",
            "duration_days": 10,
            "cta": "Shop Now",
        },
        copy={"headlines": ["H1"], "primary_texts": ["T1"], "ctas": ["Buy"]},
        visuals={"image_prompts": ["Prompt 1"]},
        budget={"total_budget": 1000, "daily_budget": 100, "budget_split": []},
        ab_tests={"tests": []},
        image_urls=["https://example.com/image.png"],
        strategy={"campaign_name": "Test Campaign"},
        mock_assets={"assets": [{"title": "Test Asset"}]},
        mockups={"assets": [{"format": "Instagram Feed Ad"}]},
    )

    assert result["campaign_pack"]["brief_summary"]["product"] == "Tea"
    assert result["campaign_pack"]["generated_image_urls"] == [
        "https://example.com/image.png"
    ]
    assert result["campaign_pack"]["kpi_plan"]["primary_metric"] == "Conversion Rate and CPA"
    assert len(result["campaign_pack"]["ethical_considerations"]) > 0
    assert result["campaign_pack"]["campaign_strategy"]["campaign_name"] == "Test Campaign"
    assert result["campaign_pack"]["mock_assets"]["assets"][0]["title"] == "Test Asset"
    assert result["campaign_pack"]["mockup_assets"]["assets"][0]["format"] == "Instagram Feed Ad"
