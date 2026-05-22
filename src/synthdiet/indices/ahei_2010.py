"""Alternate Healthy Eating Index 2010 (AHEI-2010).

Reference: Chiuve SE, Fung TT, Rimm EB, et al. (2012). "Alternative Dietary
Indices Both Strongly Predict Risk of Chronic Disease." J Nutr 142:1009-1018.
doi:10.3945/jn.111.157222
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from synthdiet.indices.base import DietQualityIndex, IndexComponent, IndexScore, linear_score

if TYPE_CHECKING:
    from synthdiet.diets.base import DietPlan
    from synthdiet.patients.patient import Patient


class AHEI2010(DietQualityIndex):
    name = "AHEI-2010"
    max_total = 110.0  # 11 components x 10 points

    def score(
        self, diet: "DietPlan", patient: Optional["Patient"] = None
    ) -> IndexScore:
        macros = diet.macronutrient_distribution()
        fiber = diet.fiber_g_per_day or 0.0
        sodium = diet.sodium_mg_per_day or 0.0
        sat_fat = diet.saturated_fat_pct or 0.10
        added_sugar = diet.added_sugar_pct or 0.10
        tags = diet.tags or set()

        c_veg = linear_score(fiber, 5, 25, max_points=10)
        c_fruit = linear_score(fiber, 5, 22, max_points=10)
        c_whole_grain = linear_score(macros.get("carbohydrate", 0.0), 0.30, 0.55, max_points=10)
        c_ssb = linear_score(added_sugar, 0.20, 0.0, max_points=10)
        c_nuts = 5.0 + (5.0 if "mediterranean" in tags or "plant_based" in tags else 0.0)
        c_red_processed = 5.0 + (5.0 if "vegan" in tags else 0.0)
        c_trans = 10.0  # synthdiet ignores trans fat -> assume best-case
        c_lcn3 = 5.0 + (5.0 if "mediterranean" in tags else 0.0)
        c_pufa = linear_score(macros.get("fat", 0.0), 0.15, 0.40, max_points=10)
        c_sodium = linear_score(sodium, 3500, 1100, max_points=10)
        c_alcohol = 5.0  # default moderate

        components = [
            IndexComponent("Vegetables", fiber, c_veg, 10),
            IndexComponent("Fruit", fiber, c_fruit, 10),
            IndexComponent("Whole Grains", macros.get("carbohydrate", 0.0),
                           c_whole_grain, 10),
            IndexComponent("Sugar-Sweetened Beverages (reverse)", added_sugar,
                           c_ssb, 10),
            IndexComponent("Nuts and Legumes", 0.0, c_nuts, 10),
            IndexComponent("Red/Processed Meat (reverse)", 0.0,
                           c_red_processed, 10),
            IndexComponent("Trans Fat (reverse, default)", 0.0, c_trans, 10),
            IndexComponent("Long-chain (n-3) PUFA", 0.0, c_lcn3, 10),
            IndexComponent("PUFA share", macros.get("fat", 0.0), c_pufa, 10),
            IndexComponent("Sodium (reverse)", sodium, c_sodium, 10),
            IndexComponent("Alcohol (moderate)", 0.0, c_alcohol, 10),
        ]
        total = sum(c.score for c in components)
        return IndexScore(
            index_name=self.name,
            total=float(total),
            max_total=self.max_total,
            components=components,
        )
