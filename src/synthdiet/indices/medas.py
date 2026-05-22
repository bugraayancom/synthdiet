"""Mediterranean Diet Adherence Screener (MEDAS, 14-item).

Reference: Schroder H, Fito M, Estruch R, et al. (2011). "A short screener
is valid for assessing Mediterranean diet adherence among older Spanish men
and women." J Nutr 141:1140-1145. doi:10.3945/jn.110.135566
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from synthdiet.indices.base import DietQualityIndex, IndexComponent, IndexScore

if TYPE_CHECKING:
    from synthdiet.diets.base import DietPlan
    from synthdiet.patients.patient import Patient


class MEDAS(DietQualityIndex):
    name = "MEDAS"
    max_total = 14.0

    def score(
        self, diet: "DietPlan", patient: Optional["Patient"] = None
    ) -> IndexScore:
        tags = diet.tags or set()
        is_med = "mediterranean" in tags
        is_plant = "plant_based" in tags or "vegan" in tags
        fiber = diet.fiber_g_per_day or 0.0
        sat_fat = diet.saturated_fat_pct or 0.10
        added_sugar = diet.added_sugar_pct or 0.10

        items = [
            ("Use olive oil as main culinary fat", 1.0 if is_med else 0.3),
            ("Olive oil >= 4 tbsp/day", 1.0 if is_med else 0.2),
            ("Vegetables >= 2 servings/day", 1.0 if fiber >= 20 else 0.4),
            ("Fruits >= 3 servings/day", 1.0 if fiber >= 22 else 0.4),
            ("Red meat < 1 serving/day", 1.0 if is_plant or is_med else 0.5),
            ("Butter/cream/margarine < 1/day", 1.0 if sat_fat <= 0.08 else 0.4),
            ("Sugar-sweetened beverages < 1/day", 1.0 if added_sugar <= 0.05 else 0.3),
            ("Wine >= 7 glasses/week (moderate)", 0.5),
            ("Legumes >= 3 servings/week", 1.0 if is_med or is_plant else 0.5),
            ("Fish/seafood >= 3 servings/week", 1.0 if is_med else 0.3),
            ("Commercial sweets < 3/week", 1.0 if added_sugar <= 0.05 else 0.3),
            ("Nuts >= 3 servings/week", 1.0 if is_med or is_plant else 0.4),
            ("Poultry preferred over red meat", 1.0 if is_med or is_plant else 0.5),
            ("Sofrito sauce >= 2/week", 1.0 if is_med else 0.3),
        ]
        components = [
            IndexComponent(name, raw_value=score, score=score, max_score=1.0)
            for name, score in items
        ]
        return IndexScore(
            index_name=self.name,
            total=sum(c.score for c in components),
            max_total=self.max_total,
            components=components,
        )
