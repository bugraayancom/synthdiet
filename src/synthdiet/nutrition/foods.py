"""A lightweight built-in food database.

The provided table covers about 50 commonly used dietetic foods with approximate
USDA-FDC values per 100 g (edible portion). Power users may load their own
:class:`Food` objects or replace :func:`default_food_database` entirely.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Set

from synthdiet.nutrition.nutrients import NutrientProfile


@dataclass
class Food:
    """A single food item with per-100-g nutrient information."""

    name: str
    category: str
    profile_per_100g: NutrientProfile
    tags: Set[str] = field(default_factory=set)
    allergens: Set[str] = field(default_factory=set)

    def portion(self, grams: float) -> NutrientProfile:
        return self.profile_per_100g.scale(grams / 100.0)


class FoodDatabase:
    """In-memory food database with simple search helpers."""

    def __init__(self, foods: Optional[Iterable[Food]] = None) -> None:
        self._foods: Dict[str, Food] = {}
        if foods:
            for f in foods:
                self.add(f)

    def add(self, food: Food) -> None:
        self._foods[food.name.lower()] = food

    def get(self, name: str) -> Food:
        try:
            return self._foods[name.lower()]
        except KeyError as exc:
            raise KeyError(f"Unknown food: {name!r}") from exc

    def names(self) -> List[str]:
        return sorted(self._foods)

    def filter(self, *, tag: Optional[str] = None, category: Optional[str] = None,
               exclude_allergens: Optional[Iterable[str]] = None) -> List[Food]:
        items = list(self._foods.values())
        if tag is not None:
            items = [f for f in items if tag in f.tags]
        if category is not None:
            items = [f for f in items if f.category == category]
        if exclude_allergens:
            ex = set(exclude_allergens)
            items = [f for f in items if not (f.allergens & ex)]
        return items

    def __len__(self) -> int:
        return len(self._foods)

    def __contains__(self, name: object) -> bool:
        return isinstance(name, str) and name.lower() in self._foods


def _f(
    name: str,
    category: str,
    kcal: float,
    protein: float,
    carb: float,
    fat: float,
    *,
    sat: float = 0.0,
    fiber: float = 0.0,
    added_sugar: float = 0.0,
    sodium: float = 0.0,
    potassium: float = 0.0,
    calcium: float = 0.0,
    iron: float = 0.0,
    phosphorus: float = 0.0,
    vitamin_c: float = 0.0,
    tags: Optional[Iterable[str]] = None,
    allergens: Optional[Iterable[str]] = None,
) -> Food:
    """Helper to keep the food table concise."""
    profile = NutrientProfile(
        energy_kcal=kcal,
        nutrients={
            "protein_g": protein,
            "carbohydrate_g": carb,
            "fat_g": fat,
            "saturated_fat_g": sat,
            "fiber_g": fiber,
            "added_sugar_g": added_sugar,
            "sodium_mg": sodium,
            "potassium_mg": potassium,
            "calcium_mg": calcium,
            "iron_mg": iron,
            "phosphorus_mg": phosphorus,
            "vitamin_c_mg": vitamin_c,
        },
    )
    return Food(
        name=name,
        category=category,
        profile_per_100g=profile,
        tags=set(tags or ()),
        allergens=set(allergens or ()),
    )


def default_food_database() -> FoodDatabase:
    """Return a populated :class:`FoodDatabase` with common foods."""
    foods = [
        # --- grains / starches ---
        _f("oats", "grain", 389, 16.9, 66.3, 6.9, sat=1.2, fiber=10.6, potassium=429, iron=4.7,
           tags={"whole_grain", "low_glycaemic", "soluble_fiber"}, allergens={"gluten_possible"}),
        _f("brown_rice", "grain", 111, 2.6, 23.0, 0.9, fiber=1.8, potassium=43,
           tags={"whole_grain"}),
        _f("white_rice", "grain", 130, 2.7, 28.0, 0.3, fiber=0.4,
           tags={"refined_grain"}),
        _f("quinoa", "grain", 120, 4.4, 21.3, 1.9, fiber=2.8, iron=1.5,
           tags={"whole_grain", "gluten_free", "complete_protein"}),
        _f("whole_wheat_bread", "grain", 247, 13.0, 41.0, 3.4, fiber=7.0, sodium=400,
           tags={"whole_grain"}, allergens={"wheat", "gluten"}),
        _f("white_bread", "grain", 265, 9.0, 49.0, 3.2, fiber=2.7, sodium=491,
           tags={"refined_grain"}, allergens={"wheat", "gluten"}),
        # --- legumes ---
        _f("lentils_cooked", "legume", 116, 9.0, 20.0, 0.4, fiber=7.9, potassium=369, iron=3.3,
           tags={"plant_protein", "low_fodmap_in_small_serves"}),
        _f("chickpeas_cooked", "legume", 164, 8.9, 27.4, 2.6, fiber=7.6, potassium=291, iron=2.9,
           tags={"plant_protein"}),
        _f("black_beans_cooked", "legume", 132, 8.9, 23.7, 0.5, fiber=8.7, potassium=355,
           tags={"plant_protein"}),
        _f("tofu", "legume", 76, 8.0, 1.9, 4.8, calcium=350,
           tags={"plant_protein", "complete_protein"}, allergens={"soy"}),
        # --- vegetables ---
        _f("broccoli", "vegetable", 35, 2.4, 7.2, 0.4, fiber=3.3, potassium=316, calcium=40, vitamin_c=89,
           tags={"low_glycaemic", "cruciferous", "high_fiber"}),
        _f("spinach", "vegetable", 23, 2.9, 3.6, 0.4, fiber=2.2, potassium=558, calcium=99, iron=2.7,
           tags={"leafy_green", "low_calorie"}),
        _f("carrot", "vegetable", 41, 0.9, 9.6, 0.2, fiber=2.8, potassium=320,
           tags={"low_glycaemic"}),
        _f("tomato", "vegetable", 18, 0.9, 3.9, 0.2, fiber=1.2, potassium=237, vitamin_c=13,
           tags={"low_glycaemic"}),
        _f("kale", "vegetable", 49, 4.3, 8.8, 0.9, fiber=3.6, calcium=150,
           tags={"leafy_green", "cruciferous"}),
        _f("sweet_potato", "vegetable", 86, 1.6, 20.1, 0.1, fiber=3.0, potassium=337,
           tags={"complex_carb"}),
        # --- fruits ---
        _f("apple", "fruit", 52, 0.3, 14.0, 0.2, fiber=2.4, potassium=107, vitamin_c=4.6,
           tags={"low_fodmap_no", "fiber"}),
        _f("banana", "fruit", 89, 1.1, 23.0, 0.3, fiber=2.6, potassium=358,
           tags={"high_potassium"}),
        _f("blueberries", "fruit", 57, 0.7, 14.5, 0.3, fiber=2.4, vitamin_c=9.7,
           tags={"low_glycaemic", "antioxidant"}),
        _f("orange", "fruit", 47, 0.9, 11.8, 0.1, fiber=2.4, potassium=181, calcium=40, vitamin_c=53,
           tags={"vitamin_c"}),
        _f("strawberries", "fruit", 32, 0.7, 7.7, 0.3, fiber=2.0, vitamin_c=59,
           tags={"low_glycaemic"}),
        # --- proteins (animal) ---
        _f("chicken_breast", "meat", 165, 31.0, 0.0, 3.6, sat=1.0, potassium=256, phosphorus=210,
           tags={"lean_protein"}),
        _f("salmon", "fish", 208, 20.4, 0.0, 13.4, sat=3.1, potassium=363, phosphorus=240,
           tags={"omega3", "fatty_fish"}, allergens={"fish"}),
        _f("egg", "egg", 155, 12.6, 1.1, 10.6, sat=3.3, calcium=50, iron=1.8,
           tags={"complete_protein"}, allergens={"egg"}),
        _f("greek_yogurt", "dairy", 59, 10.0, 3.6, 0.4, calcium=110, sodium=36,
           tags={"high_protein"}, allergens={"milk"}),
        _f("cottage_cheese", "dairy", 98, 11.1, 3.4, 4.3, sat=1.7, calcium=83, sodium=364,
           tags={"high_protein"}, allergens={"milk"}),
        _f("milk_whole", "dairy", 61, 3.2, 4.8, 3.3, sat=1.9, calcium=113, potassium=132,
           allergens={"milk"}),
        _f("milk_skim", "dairy", 34, 3.4, 5.0, 0.1, calcium=125, potassium=156,
           tags={"low_fat"}, allergens={"milk"}),
        _f("cheddar_cheese", "dairy", 402, 24.9, 1.3, 33.1, sat=18.9, calcium=721, sodium=621,
           allergens={"milk"}),
        # --- fats / oils ---
        _f("olive_oil", "fat", 884, 0.0, 0.0, 100.0, sat=13.8,
           tags={"mufa", "mediterranean"}),
        _f("butter", "fat", 717, 0.9, 0.1, 81.1, sat=51.4, sodium=11,
           allergens={"milk"}),
        _f("avocado", "fat", 160, 2.0, 8.5, 14.7, sat=2.1, fiber=6.7, potassium=485,
           tags={"mufa"}),
        # --- nuts / seeds ---
        _f("almonds", "nut", 579, 21.2, 21.6, 49.9, sat=3.8, fiber=12.5, calcium=269,
           tags={"omega3_alpha_linolenic"}, allergens={"tree_nut"}),
        _f("walnuts", "nut", 654, 15.2, 13.7, 65.2, sat=6.1, fiber=6.7,
           tags={"omega3"}, allergens={"tree_nut"}),
        _f("peanut_butter", "nut", 588, 25.1, 19.6, 50.4, sat=10.0, fiber=6.0, sodium=476,
           allergens={"peanut"}),
        _f("chia_seeds", "seed", 486, 16.5, 42.1, 30.7, fiber=34.4, calcium=631,
           tags={"omega3", "high_fiber"}),
        # --- processed / discretionary ---
        _f("white_sugar", "sweetener", 387, 0.0, 100.0, 0.0, added_sugar=100,
           tags={"refined_sugar"}),
        _f("honey", "sweetener", 304, 0.3, 82.4, 0.0, added_sugar=82,
           tags={"natural_sweetener"}),
        _f("dark_chocolate_70", "confectionery", 598, 7.8, 45.9, 42.6, sat=24.5, fiber=10.9,
           tags={"flavanols"}),
        _f("potato_chips", "snack", 536, 7.0, 53.0, 34.6, sat=3.2, sodium=525,
           tags={"ultra_processed"}),
        _f("cola", "beverage", 41, 0.0, 10.6, 0.0, added_sugar=10.6, sodium=4,
           tags={"sugar_sweetened_beverage"}),
        # --- beverages ---
        _f("coffee_black", "beverage", 2, 0.3, 0.0, 0.0,
           tags={"caffeine"}),
        _f("green_tea", "beverage", 1, 0.0, 0.0, 0.0,
           tags={"antioxidant"}),
        _f("water", "beverage", 0, 0.0, 0.0, 0.0,
           tags={"hydration"}),
    ]
    return FoodDatabase(foods)
