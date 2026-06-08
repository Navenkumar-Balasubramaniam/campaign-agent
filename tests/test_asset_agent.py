from src.agents.asset_agent import AssetAgent
from src.models.schemas import CampaignBrief


def test_asset_agent_returns_mock_sources():
    brief = CampaignBrief(
        brand="Estrella",
        product="Mediterranean-style beer",
        audience="young adults aged 18-24",
        goal="Sales",
        budget=1000,
        channel="Instagram",
        tone="Fun, party, good vibes",
        duration_days=14,
        cta="Shop Now",
    )

    result = AssetAgent().generate(brief)

    assert "asset_strategy" in result
    assert len(result["assets"]) == 3
    assert result["assets"][0]["source"] == "Wikimedia Commons"
