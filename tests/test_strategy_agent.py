from src.agents.strategy_agent import StrategyAgent
from src.models.schemas import CampaignBrief


def test_strategy_agent_generates_whole_campaign_plan():
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

    result = StrategyAgent().generate(brief)

    assert result["campaign_name"] == "Estrella Social Pour"
    assert len(result["message_pillars"]) == 3
    assert len(result["content_plan"]) == 3
    assert len(result["launch_checklist"]) >= 3
