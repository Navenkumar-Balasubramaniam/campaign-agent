from src.agents.classifier_agent import ClassifierAgent
from src.models.schemas import CampaignBrief


def _brief(goal="Sales", trigger="The sun is out, head to the beer garden for a cold beer."):
    return CampaignBrief(
        brand="Estrella",
        campaign_trigger=trigger,
        product="Mediterranean-style beer",
        audience="adults 18-24",
        goal=goal,
        budget=1000,
        channel="Instagram",
        tone="Fun",
        duration_days=14,
        cta="Shop Now",
    )


def test_classifier_detects_summer_and_alcohol_risk():
    result = ClassifierAgent().classify(_brief())
    assert result["season"] == "summer"
    assert "alcohol" in result["risk_flags"]
    assert result["method"] == "rules"


def test_sales_goal_suggests_product_led():
    result = ClassifierAgent().classify(_brief(goal="Sales"))
    assert result["suggested_angle"] == "product-led"


def test_awareness_goal_suggests_emotional():
    result = ClassifierAgent().classify(_brief(goal="Awareness"))
    assert result["suggested_angle"] == "emotional-narrative"
