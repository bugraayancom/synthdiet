"""Diet plan, meal, and food-serving abstractions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Mapping, Optional, Sequence, Set

from synthdiet.nutrition.foods import FoodDatabase, default_food_database
from synthdiet.nutrition.nutrients import NutrientProfile
from synthdiet.utils.constants import KCAL_PER_GRAM


@dataclass
class FoodServing:
    """A specific quantity of a named food."""

    food_name: str
    grams: float

    def nutrient_profile(self, database: FoodDatabase) -> NutrientProfile:
        return database.get(self.food_name).portion(self.grams)


@dataclass
class Meal:
    """A meal made of one or more servings of foods."""

    name: str
    servings: List[FoodServing] = field(default_factory=list)

    def nutrient_profile(self, database: FoodDatabase) -> NutrientProfile:
        return sum((s.nutrient_profile(database) for s in self.servings),
                   start=NutrientProfile())


@dataclass
class DietPlan:
    """A daily dietary prescription.

    A :class:`DietPlan` is either *food-based* (provide :attr:`meals`) or
    *target-based* (set :attr:`daily_energy_kcal` and the macro percentage
    fields directly). Both styles work with the simulation engine.
    """

    name: str
    description: str = ""

    # Food-based specification
    meals: List[Meal] = field(default_factory=list)
    food_database: Optional[FoodDatabase] = None

    # Target-based specification (filled in by ``compute_targets`` if missing)
    daily_energy_kcal: float = 0.0
    macronutrient_pct: Dict[str, float] = field(default_factory=dict)
    sodium_mg_per_day: Optional[float] = None
    potassium_mg_per_day: Optional[float] = None
    fiber_g_per_day: Optional[float] = None
    saturated_fat_pct: Optional[float] = None
    added_sugar_pct: Optional[float] = None
    cholesterol_mg_per_day: Optional[float] = None
    fluid_ml_per_day: Optional[float] = None
    tags: Set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        if self.meals and self.food_database is None:
            self.food_database = default_food_database()
        if self.meals:
            self._refresh_from_meals()

    # Computed properties --------------------------------------------------
    def _refresh_from_meals(self) -> None:
        if not self.meals or self.food_database is None:
            return
        total = sum((m.nutrient_profile(self.food_database) for m in self.meals),
                    start=NutrientProfile())
        self.daily_energy_kcal = total.energy_kcal
        kcals = {
            "protein": total.get("protein_g") * KCAL_PER_GRAM["protein"],
            "carbohydrate": total.get("carbohydrate_g") * KCAL_PER_GRAM["carbohydrate"],
            "fat": total.get("fat_g") * KCAL_PER_GRAM["fat"],
        }
        ek = max(self.daily_energy_kcal, 1.0)
        self.macronutrient_pct = {k: v / ek for k, v in kcals.items()}
        self.fiber_g_per_day = total.get("fiber_g")
        self.sodium_mg_per_day = total.get("sodium_mg") or self.sodium_mg_per_day
        self.potassium_mg_per_day = total.get("potassium_mg") or self.potassium_mg_per_day
        if total.get("fat_g") > 0:
            self.saturated_fat_pct = (
                total.get("saturated_fat_g") * KCAL_PER_GRAM["fat"] / ek
            )
        if total.get("carbohydrate_g") > 0:
            self.added_sugar_pct = (
                total.get("added_sugar_g") * KCAL_PER_GRAM["carbohydrate"] / ek
            )

    def macronutrient_distribution(self) -> Mapping[str, float]:
        """Return percentages of energy from protein, carbohydrate, and fat."""
        if self.macronutrient_pct:
            return dict(self.macronutrient_pct)
        return {"protein": 0.15, "carbohydrate": 0.50, "fat": 0.35}

    def daily_profile(self) -> NutrientProfile:
        """Return the aggregated nutrient profile for the full day."""
        if not self.meals or self.food_database is None:
            return NutrientProfile(energy_kcal=self.daily_energy_kcal)
        return sum((m.nutrient_profile(self.food_database) for m in self.meals),
                   start=NutrientProfile())

    def forbidden_food_set(self) -> Set[str]:
        return {s.food_name for m in self.meals for s in m.servings}

    # Constructors ---------------------------------------------------------
    @classmethod
    def from_targets(
        cls,
        name: str,
        *,
        daily_energy_kcal: float,
        macronutrient_pct: Mapping[str, float],
        description: str = "",
        sodium_mg_per_day: Optional[float] = None,
        fiber_g_per_day: Optional[float] = None,
        saturated_fat_pct: Optional[float] = None,
        added_sugar_pct: Optional[float] = None,
        cholesterol_mg_per_day: Optional[float] = None,
        fluid_ml_per_day: Optional[float] = None,
        tags: Optional[Sequence[str]] = None,
    ) -> "DietPlan":
        plan = cls(
            name=name,
            description=description,
            daily_energy_kcal=daily_energy_kcal,
            macronutrient_pct=dict(macronutrient_pct),
            sodium_mg_per_day=sodium_mg_per_day,
            fiber_g_per_day=fiber_g_per_day,
            saturated_fat_pct=saturated_fat_pct,
            added_sugar_pct=added_sugar_pct,
            cholesterol_mg_per_day=cholesterol_mg_per_day,
            fluid_ml_per_day=fluid_ml_per_day,
            tags=set(tags or ()),
        )
        return plan

    def summary(self) -> str:
        macros = self.macronutrient_distribution()
        return (
            f"DietPlan({self.name}) | {self.daily_energy_kcal:.0f} kcal | "
            f"C {macros.get('carbohydrate', 0) * 100:.0f}% / "
            f"P {macros.get('protein', 0) * 100:.0f}% / "
            f"F {macros.get('fat', 0) * 100:.0f}%"
        )
