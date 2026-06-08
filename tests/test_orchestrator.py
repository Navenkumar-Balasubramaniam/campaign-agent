from src.orchestrator import CampaignOrchestrator
from src.models.schemas import CampaignBrief


class FakeClient:
    def generate_text(self, prompt: str):
        return {
            "headlines": ["Headline 1", "Headline 2", "Headline 3"],
            "primary_texts": ["Text 1", "Text 2", "Text 3"],
            "ctas": ["Shop Now", "Learn More"],
        }

    def generate_image(self, prompt: str):
        return "https://example.com/generated-image.png"


def test_orchestrator_generates_campaign_pack():
    brief = CampaignBrief(
        product="Herbal Tea",
        audience="Women 25-45",
        goal="Sales",
        budget=1000,
        channel="Instagram",
        tone="Premium wellness",
        duration_days=10,
        cta="Shop Now",
    )

    orchestrator = CampaignOrchestrator(FakeClient())
    result = orchestrator.run(brief, generate_image=True)

    assert "campaign_pack" in result
    assert result["campaign_pack"]["brief_summary"]["product"] == "Herbal Tea"
    assert result["campaign_pack"]["generated_image_urls"] == [
        "https://example.com/generated-image.png",
        "https://example.com/generated-image.png",
        "https://example.com/generated-image.png",
    ]
    assert "decision_rationale" in result["campaign_pack"]
    assert "campaign_strategy" in result["campaign_pack"]
    assert "mock_assets" in result["campaign_pack"]
    assert len(result["campaign_pack"]["mockup_assets"]["assets"]) == 3
