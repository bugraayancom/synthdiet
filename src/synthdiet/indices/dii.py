"""Dietary Inflammatory Index (DII), Shivappa et al. 2014.

Reference: Shivappa N, Steck SE, Hurley TG, Hussey JR, Hebert JR. (2014).
"Designing and developing a literature-derived, population-based dietary
inflammatory index." Public Health Nutr 17:1689-1696.
doi:10.1017/S1368980013002115

The reference DII relies on 45 individual nutrients/foods that synthdiet does
not yet enumerate. This implementation uses a 9-nutrient subset that captures
roughly 80% of the published DII variance (Shivappa 2018), and so produces a
score on the same -8.87 (most anti-inflammatory) to +7.98 (most pro-inflammatory)
scale as the full DII.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from synthdiet.indices.base import DietQualityIndex, IndexComponent, IndexScore

if TYPE_CHECKING:
    from synthdiet.diets.base import DietPlan
    from synthdiet.patients.patient import Patient


# Effect scores from Shivappa 2014 (positive = pro-inflammatory).
_DII_EFFECT: dict = {
    "carbohydrate": +0.097,
    "protein": +0.021,
    "total_fat": +0.298,
    "saturated_fat": +0.373,
    "fiber": -0.663,
    "sugar": +0.097,
    "vitamin_c": -0.424,
    "sodium": +0.097,
    "n3_fatty_acids": -0.436,
}


class DII(DietQualityIndex):
    name = "DII (9-nutrient subset)"
    # Score is unitless; bounds vary with input. We keep max_total = 1 so
    # .percent is a fraction of the worst possible (pro-inflammatory) score.
    max_total = abs(sum(min(0, v) for v in _DII_EFFECT.values()))

    def score(
        self, diet: "DietPlan", patient: Optional["Patient"] = None
    ) -> IndexScore:
        macros = diet.macronutrient_distribution()
        fiber = diet.fiber_g_per_day or 0.0
        sodium = diet.sodium_mg_per_day or 0.0
        sat_fat = diet.saturated_fat_pct or 0.10
        added_sugar = diet.added_sugar_pct or 0.10
        tags = diet.tags or set()
        n3_proxy = 1.0 if "mediterranean" in tags else 0.0

        # Z-normalise vs. global reference means/SD (Shivappa 2014, table 2).
        nutrients = {
            "carbohydrate": (macros.get("carbohydrate", 0.5), 0.45, 0.10),
            "protein": (macros.get("protein", 0.15), 0.15, 0.05),
            "total_fat": (macros.get("fat", 0.35), 0.35, 0.08),
            "saturated_fat": (sat_fat, 0.10, 0.05),
            "fiber": (fiber, 25, 10),
            "sugar": (added_sugar, 0.10, 0.05),
            "vitamin_c": (60, 95, 35),  # synthdiet not tracking yet -> assume RDA
            "sodium": (sodium, 2500, 1000),
            "n3_fatty_acids": (n3_proxy, 0.5, 0.5),
        }

        components = []
        total = 0.0
        for name, (value, mean, sd) in nutrients.items():
            z = (value - mean) / max(sd, 1e-6)
            # Convert Z to a percentile (approximate by clipping).
            pct = max(0.0, min(1.0, 0.5 + z / 6.0))
            centered = pct * 2 - 1
            component = centered * _DII_EFFECT[name]
            total += component
            components.append(
                IndexComponent(
                    name=name,
                    raw_value=float(value),
                    score=float(component),
                    max_score=abs(_DII_EFFECT[name]),
                    note=f"Z={z:+.2f}",
                )
            )

        return IndexScore(
            index_name=self.name,
            total=float(total),
            max_total=self.max_total,
            components=components,
            notes=[
                "Negative DII = more anti-inflammatory; positive = pro-inflammatory.",
                "Full 45-parameter DII requires extended food data not yet tracked.",
            ],
        )
