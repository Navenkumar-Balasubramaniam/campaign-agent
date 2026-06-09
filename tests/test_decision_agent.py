from src.agents.decision_agent import DecisionAgent
from src.knowledge.benchmarks import Benchmarks
from src.knowledge.campaign_store import CampaignStore
from src.models.schemas import CampaignBrief


def _brief(goal="Sales"):
    return CampaignBrief(
        brand="Estrella",
        campaign_trigger="The sun is out, head to the beer garden for a cold beer.",
        product="Mediterranean-style beer",
        audience="adults 18-24",
        goal=goal,
        budget=1000,
        channel="Instagram",
        tone="Fun",
        duration_days=14,
        cta="Shop Now",
    )


def test_decision_recommends_product_led_for_sales():
    bench = Benchmarks(brand="Estrella")
    store = CampaignStore(brand="Estrella")
    classification = {
        "season": "summer",
        "themes": ["summer", "social"],
        "suggested_angle": "product-led",
    }
    retrieved = store.retrieve(season="summer", goal="Sales", query="cold beer terrace", k=3)

    decision = DecisionAgent().generate(_brief("Sales"), classification, bench, retrieved)

    assert decision["available"] is True
    assert decision["recommended_angle"] == "product-led"
    assert decision["primary_metric"] == "ROAS"
    assert decision["expected_performance"]["roas"]
    assert len(decision["rationale_points"]) >= 2


def test_decision_handles_no_benchmarks():
    classification = {"season": "summer", "themes": [], "suggested_angle": "lifestyle"}
    decision = DecisionAgent().generate(_brief(), classification, None, [])
    assert decision["available"] is False
    assert decision["confidence"] == "low"
