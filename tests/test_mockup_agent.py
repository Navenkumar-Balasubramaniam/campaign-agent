from src.agents.mockup_agent import MockupAgent
from src.agents.strategy_agent import StrategyAgent
from src.clients.demo_client import DemoClient
from src.models.schemas import CampaignBrief


def test_mockup_agent_generates_offline_image_assets():
    brief = CampaignBrief(
        brand="Estrella",
        campaign_trigger="The sun is out and people want to go to beer gardens.",
        product="Mediterranean-style beer",
        audience="adults aged 18-24",
        goal="Sales",
        budget=1000,
        channel="Instagram",
        tone="Fun, party, good vibes",
        duration_days=14,
        cta="Shop Now",
    )

    copy = DemoClient().generate_copy(brief)
    strategy = StrategyAgent().generate(brief)
    result = MockupAgent().generate(brief, copy, strategy)

    assert len(result["assets"]) == 3
    assert result["assets"][0]["image_data_url"].startswith("data:image/png;base64,")
    assert result["assets"][0]["format"] == "Instagram Feed Ad"
