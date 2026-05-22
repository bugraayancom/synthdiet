"""Planetary Health Diet Index (PHDI, EAT-Lancet).

Reference: Cacau LT, De Carli E, de Carvalho AM, et al. (2021). "Development
and Validation of an Index Based on EAT-Lancet Recommendations: The Planetary
Health Diet Index." Nutrients 13(5):1698. doi:10.3390/nu13051698
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from synthdiet.indices.base import DietQualityIndex, IndexComponent, IndexScore, linear_score

if TYPE_CHECKING:
    from synthdiet.diets.base import DietPlan
    from synthdiet.patients.patient import Patient


class PHDI(DietQualityIndex):
    name = "PHDI (EAT-Lancet)"
    max_total = 150.0

    def score(
        self, diet: "DietPlan", patient: Optional["Patient"] = None
    ) -> IndexScore:
        macros = diet.macronutrient_distribution()
        tags = diet.tags or set()
        fiber = diet.fiber_g_per_day or 0.0
        added_sugar = diet.added_sugar_pct or 0.10
        sat_fat = diet.saturated_fat_pct or 0.10
        is_plant = bool({"vegan", "plant_based"} & tags)
        is_med = "mediterranean" in tags

        c_grains = linear_score(macros.get("carbohydrate", 0.0), 0.30, 0.55, max_points=10)
        c_veg = linear_score(fiber, 5, 35, max_points=10)
        c_fruit = linear_score(fiber, 5, 30, max_points=10)
        c_dairy = 5.0
        c_red_meat = 10.0 if is_plant else 4.0
        c_chicken = 5.0
        c_fish = 5.0 + (5.0 if is_med else 0.0)
        c_eggs = 5.0
        c_legumes = 5.0 + (5.0 if is_plant or is_med else 0.0)
        c_nuts = 5.0 + (5.0 if is_med or is_plant else 0.0)
        c_unsat_oils = linear_score(macros.get("fat", 0.0), 0.20, 0.40, max_points=10)
        c_sat_oils = linear_score(sat_fat, 0.18, 0.06, max_points=10)
        c_added_sugar = linear_score(added_sugar, 0.20, 0.0, max_points=10)
        c_tubers = 5.0
        c_juice = 5.0  # neutral

        components = [
            IndexComponent("Whole Grains", macros.get("carbohydrate", 0.0),
                           c_grains, 10),
            IndexComponent("Vegetables", fiber, c_veg, 10),
            IndexComponent("Fruits", fiber, c_fruit, 10),
            IndexComponent("Dairy (default)", 0.0, c_dairy, 10),
            IndexComponent("Red Meat (reverse)", 0.0, c_red_meat, 10),
            IndexComponent("Chicken/Other", 0.0, c_chicken, 10),
            IndexComponent("Fish", 0.0, c_fish, 10),
            IndexComponent("Eggs", 0.0, c_eggs, 10),
            IndexComponent("Legumes", 0.0, c_legumes, 10),
            IndexComponent("Nuts & Seeds", 0.0, c_nuts, 10),
            IndexComponent("Unsaturated Plant Oils", macros.get("fat", 0.0),
                           c_unsat_oils, 10),
            IndexComponent("Saturated Oils (reverse)", sat_fat, c_sat_oils, 10),
            IndexComponent("Added Sugars (reverse)", added_sugar, c_added_sugar, 10),
            IndexComponent("Tubers/Starchy Vegetables", 0.0, c_tubers, 10),
            IndexComponent("Fruit Juice (default)", 0.0, c_juice, 10),
        ]
        return IndexScore(
            index_name=self.name,
            total=float(sum(c.score for c in components)),
            max_total=self.max_total,
            components=components,
        )
