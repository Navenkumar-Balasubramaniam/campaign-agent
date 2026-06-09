import csv
from pathlib import Path

DATA_ROOT = Path(__file__).resolve().parents[2] / "data"

_RATE_FIELDS = ["ctr", "cpc", "cpa", "conversion_rate", "roas"]
_GOAL_PRIMARY_METRIC = {
    "awareness": ("ctr", "max"),
    "sales": ("roas", "max"),
    "lead generation": ("roas", "max"),
}


def _avg(rows, field):
    values = [r[field] for r in rows if field in r]
    return round(sum(values) / len(values), 2) if values else 0.0


class Benchmarks:
    """Aggregates historical per-variant results so the decision agent can
    reason from real numbers (what angle/audience has historically won)."""

    def __init__(self, brand="estrella", data_root=None):
        root = Path(data_root) if data_root else DATA_ROOT
        self.path = root / brand.strip().lower() / "results.csv"
        self.rows = self._load()

    def _load(self):
        if not self.path.exists():
            return []
        rows = []
        with open(self.path, "r", encoding="utf-8") as f:
            for raw in csv.DictReader(f):
                row = dict(raw)
                for field in ["impressions", "clicks", "spend", "conversions"]:
                    row[field] = float(row.get(field, 0) or 0)
                for field in _RATE_FIELDS:
                    row[field] = float(row.get(field, 0) or 0)
                rows.append(row)
        return rows

    def is_available(self):
        return bool(self.rows)

    def _group(self, key):
        groups = {}
        for row in self.rows:
            groups.setdefault(row.get(key, "unknown"), []).append(row)
        return groups

    def _aggregate(self, rows):
        agg = {field: _avg(rows, field) for field in _RATE_FIELDS}
        agg["variants"] = len(rows)
        return agg

    def overall(self):
        return self._aggregate(self.rows)

    def by_angle(self):
        return {angle: self._aggregate(rows) for angle, rows in self._group("angle").items()}

    def by_audience(self):
        return {aud: self._aggregate(rows) for aud, rows in self._group("audience_type").items()}

    def best_angle_for_goal(self, goal):
        """Return (angle, metrics, primary_metric) that historically performed
        best for this goal, using CTR for awareness and ROAS for sales/leads."""
        metric, direction = _GOAL_PRIMARY_METRIC.get(
            (goal or "").strip().lower(), ("roas", "max")
        )
        angle_stats = self.by_angle()
        if not angle_stats:
            return None, {}, metric

        ranked = sorted(
            angle_stats.items(),
            key=lambda kv: kv[1].get(metric, 0),
            reverse=(direction == "max"),
        )
        best_angle, best_metrics = ranked[0]
        return best_angle, best_metrics, metric
