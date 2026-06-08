from src.clients.demo_client import DemoClient
from src.models.schemas import CampaignBrief


def test_demo_client_generates_copy_without_api_key():
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

    result = DemoClient().generate_copy(brief)

    assert len(result["headlines"]) == 3
    assert len(result["primary_texts"]) == 3
    assert result["ctas"][0] == "Shop Now"
