from src.knowledge.campaign_store import CampaignStore


def test_store_loads_estrella_corpus():
    store = CampaignStore(brand="Estrella")
    assert store.is_available()
    assert len(store.campaigns) >= 8
    assert "Mediterranean" in store.brand_guidelines


def test_retrieve_prioritises_summer_sales_campaigns():
    store = CampaignStore(brand="Estrella")
    results = store.retrieve(
        themes=["summer", "outdoor", "social"],
        season="summer",
        channel="Instagram",
        goal="Sales",
        query="sun is out, beer gardens and parks, cold beer",
        k=3,
    )
    assert len(results) == 3
    # Top match should be a real campaign with a positive relevance score.
    assert results[0]["_score"] > 0
    angles = {c["creative"]["angle"] for c in results}
    assert "product-led" in angles


def test_unknown_brand_returns_empty_store():
    store = CampaignStore(brand="NoSuchBrand")
    assert not store.is_available()
    assert store.retrieve(query="anything") == []
