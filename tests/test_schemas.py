import pytest
from src.models.schemas import CampaignBrief


def test_campaign_brief_valid():
    brief = CampaignBrief(
        product="Herbal Tea",
        audience="Women aged 25-45 interested in wellness",
        goal="Sales",
        budget=1000,
        channel="Instagram",
        tone="Premium and calming",
        duration_days=14,
        cta="Shop Now",
    )

    assert brief.product == "Herbal Tea"
    assert brief.budget == 1000
    assert brief.duration_days == 14


def test_campaign_brief_rejects_zero_budget():
    with pytest.raises(ValueError):
        CampaignBrief(
            product="Tea",
            audience="Adults",
            goal="Sales",
            budget=0,
            channel="Instagram",
            tone="Friendly",
            duration_days=7,
            cta="Buy Now",
        )