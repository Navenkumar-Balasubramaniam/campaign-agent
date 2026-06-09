import json
import re
from pathlib import Path

DATA_ROOT = Path(__file__).resolve().parents[2] / "data"

_STOPWORDS = {
    "the", "and", "for", "with", "that", "this", "are", "out", "but", "you",
    "your", "want", "people", "have", "into", "from", "they", "them", "their",
    "who", "enjoy", "nice", "cold", "can", "will", "should", "trigger", "moment",
    "campaign", "social", "good", "make", "more", "than", "when", "what", "where",
}


def _tokens(text):
    if not text:
        return set()
    words = re.findall(r"[a-zA-Z]+", text.lower())
    return {w for w in words if len(w) > 2 and w not in _STOPWORDS}


class CampaignStore:
    """Loads a brand's past-campaign knowledge base and retrieves the
    campaigns most relevant to a new brief. This is the data source the
    strategy, copy and decision agents are grounded on."""

    def __init__(self, brand="estrella", data_root=None):
        self.brand = brand
        root = Path(data_root) if data_root else DATA_ROOT
        self.brand_dir = root / brand.strip().lower()

        self.campaigns = self._load_campaigns()
        self.brand_guidelines = self._load_guidelines()

    def _load_campaigns(self):
        path = self.brand_dir / "campaigns.json"
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_guidelines(self):
        path = self.brand_dir / "brand_guidelines.md"
        if not path.exists():
            return ""
        return path.read_text(encoding="utf-8")

    def is_available(self):
        return bool(self.campaigns)

    def _score(self, campaign, themes, season, channel, goal, query_tokens):
        score = 0
        camp_themes = {t.lower() for t in campaign.get("theme", [])}

        for theme in themes or []:
            if theme.lower() in camp_themes:
                score += 2

        if season and campaign.get("season", "").lower() == season.lower():
            score += 2
        if season == "summer" and campaign.get("season") == "summer":
            score += 1  # summer is the brand's strongest, reward proven season

        if channel and campaign.get("channel", "").lower() == channel.lower():
            score += 1
        if goal and campaign.get("goal", "").lower() == goal.lower():
            score += 1

        camp_tokens = _tokens(
            " ".join(
                [
                    campaign.get("name", ""),
                    campaign.get("trigger", ""),
                    " ".join(campaign.get("theme", [])),
                    campaign.get("positioning", ""),
                ]
            )
        )
        score += len(query_tokens & camp_tokens)
        return score

    def retrieve(self, themes=None, season=None, channel=None, goal=None, query=None, k=3):
        """Return the top-k most relevant past campaigns, each with a `_score`."""
        query_tokens = _tokens(query)
        scored = []
        for campaign in self.campaigns:
            score = self._score(campaign, themes, season, channel, goal, query_tokens)
            scored.append((score, campaign))

        scored.sort(key=lambda pair: (pair[0], pair[1].get("year", 0)), reverse=True)

        results = []
        for score, campaign in scored[:k]:
            item = dict(campaign)
            item["_score"] = score
            results.append(item)
        return results
