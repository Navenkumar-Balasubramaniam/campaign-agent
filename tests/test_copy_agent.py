from src.agents.copy_agent import CopyAgent
from src.models.schemas import CampaignBrief


class FakeClient:
    def generate_text(self, prompt: str):
        return {
            "headlines": ["Headline 1", "Headline 2", "Headline 3"],
            "primary_texts": ["Text 1", "Text 2", "Text 3"],
            "ctas": ["Shop Now", "Learn More"],
        }


def test_copy_agent_returns_copy_variants():
    brief = CampaignBrief(
        product="Herbal Tea",
        audience="Women 25-45",
        goal="Sales",
        budget=500,
        channel="Instagram",
        tone="Premium",
        duration_days=7,
        cta="Shop Now",
    )

    result = CopyAgent(FakeClient()).generate(brief)

    assert len(result["headlines"]) == 3
    assert len(result["primary_texts"]) == 3
    assert "ctas" in result