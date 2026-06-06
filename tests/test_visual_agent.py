from src.agents.visual_agent import VisualAgent
from src.models.schemas import CampaignBrief


def test_visual_agent_generates_prompts():
    brief = CampaignBrief(
        product="Herbal Tea",
        audience="Women 25-45",
        goal="Sales",
        budget=500,
        channel="Instagram",
        tone="Premium wellness",
        duration_days=7,
        cta="Shop Now",
    )

    result = VisualAgent().generate_prompts(brief)

    assert "image_prompts" in result
    assert len(result["image_prompts"]) == 2
    assert "Herbal Tea" in result["image_prompts"][0]