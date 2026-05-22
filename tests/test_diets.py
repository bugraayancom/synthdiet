"""Tests for diet plan presets and food-based plans."""

from __future__ import annotations

from synthdiet import (
    DietPlan,
    FoodServing,
    Meal,
    dash_diet,
    keto_diet,
    list_presets,
    mediterranean_diet,
)
from synthdiet.nutrition import default_food_database


def test_list_presets_non_empty() -> None:
    presets = list_presets()
    assert "mediterranean" in presets
    assert "dash" in presets
    assert "keto" in presets


def test_preset_macros_sum_to_one() -> None:
    for builder in (mediterranean_diet, dash_diet, keto_diet):
        plan = builder()
        macros = plan.macronutrient_distribution()
        total = macros["protein"] + macros["carbohydrate"] + macros["fat"]
        assert abs(total - 1.0) < 1e-6


def test_food_based_plan_computes_energy() -> None:
    db = default_food_database()
    breakfast = Meal(
        name="breakfast",
        servings=[
            FoodServing("oats", 60),
            FoodServing("milk_skim", 200),
            FoodServing("blueberries", 80),
        ],
    )
    lunch = Meal(
        name="lunch",
        servings=[
            FoodServing("chicken_breast", 150),
            FoodServing("quinoa", 200),
            FoodServing("broccoli", 200),
            FoodServing("olive_oil", 10),
        ],
    )
    plan = DietPlan(name="custom", meals=[breakfast, lunch], food_database=db)
    assert plan.daily_energy_kcal > 800
    assert plan.fiber_g_per_day is not None
