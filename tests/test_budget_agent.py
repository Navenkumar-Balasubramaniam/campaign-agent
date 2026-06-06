from src.agents.budget_agent import BudgetAgent
from src.models.schemas import CampaignBrief


def test_budget_split_sums_to_budget():
    brief = CampaignBrief(
        product="Protein Shake",
        audience="Gym-goers",
        goal="Sales",
        budget=1000,
        channel="Instagram",
        tone="Energetic",
        duration_days=10,
        cta="Buy Now",
    )

    result = BudgetAgent().generate(brief)

    total = sum(item["amount"] for item in result["budget_split"])
    assert total == 1000
    assert result["daily_budget"] == 100
    assert len(result["budget_split"]) >= 2