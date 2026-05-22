"""DASH diet score (Fung et al. 2008, 8 components).

Reference: Fung TT, Chiuve SE, McCullough ML, Rexrode KM, Logroscino G,
Hu FB. (2008). "Adherence to a DASH-style diet and risk of coronary heart
disease and stroke in women." Arch Intern Med 168:713-720.
doi:10.1001/archinte.168.7.713
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from synthdiet.indices.base import DietQualityIndex, IndexComponent, IndexScore, linear_score

if TYPE_CHECKING:
    from synthdiet.diets.base import DietPlan
    from synthdiet.patients.patient import Patient


class DASHScore(DietQualityIndex):
    name = "DASH-Score (Fung 2008)"
    # Fung's 8-component score ranges 8-40 with quintile scoring.
    max_total = 40.0

    def score(
        self, diet: "DietPlan", patient: Optional["Patient"] = None
    ) -> IndexScore:
        macros = diet.macronutrient_distribution()
        fiber = diet.fiber_g_per_day or 0.0
        sodium = diet.sodium_mg_per_day or 0.0
        sat_fat = diet.saturated_fat_pct or 0.10
        added_sugar = diet.added_sugar_pct or 0.10
        tags = diet.tags or set()
        is_dash = "dash" in tags

        # Each component scored 1 (worst quintile) to 5 (best quintile).
        c_fruit = linear_score(fiber, 5, 25, max_points=4) + 1
        c_veg = linear_score(fiber, 5, 25, max_points=4) + 1
        c_nuts_legumes = 3 + (2 if is_dash else 0)
        c_whole = linear_score(macros.get("carbohydrate", 0.0), 0.30, 0.55,
                               max_points=4) + 1
        c_low_dairy = 3 + (2 if is_dash else 0)
        c_sodium = linear_score(sodium, 4000, 1000, max_points=4) + 1
        c_red_meat = 3 + (2 if "vegan" in tags or "vegetarian" in tags else 0)
        c_ssb = linear_score(added_sugar, 0.20, 0.0, max_points=4) + 1

        components = [
            IndexComponent("Fruits", fiber, c_fruit, 5),
            IndexComponent("Vegetables", fiber, c_veg, 5),
            IndexComponent("Nuts & Legumes", 0.0, c_nuts_legumes, 5),
            IndexComponent("Whole Grains", macros.get("carbohydrate", 0.0),
                           c_whole, 5),
            IndexComponent("Low-Fat Dairy", 0.0, c_low_dairy, 5),
            IndexComponent("Sodium (reverse)", sodium, c_sodium, 5),
            IndexComponent("Red/Processed Meat (reverse)", 0.0, c_red_meat, 5),
            IndexComponent("Sugar-Sweetened Beverages (reverse)", added_sugar,
                           c_ssb, 5),
        ]
        return IndexScore(
            index_name=self.name,
            total=float(sum(c.score for c in components)),
            max_total=self.max_total,
            components=components,
        )
