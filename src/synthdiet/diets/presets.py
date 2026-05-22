"""A small library of well-known dietary patterns."""

from __future__ import annotations

from typing import Callable, Dict, List

from synthdiet.diets.base import DietPlan


def mediterranean_diet(daily_energy_kcal: float = 2000) -> DietPlan:
    return DietPlan.from_targets(
        name="mediterranean",
        description="Plant-forward Mediterranean pattern emphasising olive oil, fish, legumes, vegetables, and whole grains.",
        daily_energy_kcal=daily_energy_kcal,
        macronutrient_pct={"protein": 0.18, "carbohydrate": 0.45, "fat": 0.37},
        sodium_mg_per_day=2000,
        fiber_g_per_day=35,
        saturated_fat_pct=0.07,
        added_sugar_pct=0.05,
        cholesterol_mg_per_day=200,
        tags=("mediterranean", "heart_healthy"),
    )


def dash_diet(daily_energy_kcal: float = 2000) -> DietPlan:
    return DietPlan.from_targets(
        name="dash",
        description="Dietary Approaches to Stop Hypertension; rich in fruits, vegetables, low-fat dairy and limited sodium.",
        daily_energy_kcal=daily_energy_kcal,
        macronutrient_pct={"protein": 0.18, "carbohydrate": 0.55, "fat": 0.27},
        sodium_mg_per_day=1500,
        fiber_g_per_day=30,
        saturated_fat_pct=0.06,
        added_sugar_pct=0.05,
        cholesterol_mg_per_day=150,
        tags=("dash", "low_sodium", "heart_healthy"),
    )


def keto_diet(daily_energy_kcal: float = 1800) -> DietPlan:
    return DietPlan.from_targets(
        name="keto",
        description="Very low carbohydrate ketogenic pattern (~5% kcal from carbs).",
        daily_energy_kcal=daily_energy_kcal,
        macronutrient_pct={"protein": 0.25, "carbohydrate": 0.05, "fat": 0.70},
        sodium_mg_per_day=2500,
        fiber_g_per_day=20,
        saturated_fat_pct=0.20,
        added_sugar_pct=0.0,
        tags=("ketogenic", "very_low_carb"),
    )


def low_fodmap_diet(daily_energy_kcal: float = 2000) -> DietPlan:
    return DietPlan.from_targets(
        name="low_fodmap",
        description="Elimination phase of the low-FODMAP diet for IBS.",
        daily_energy_kcal=daily_energy_kcal,
        macronutrient_pct={"protein": 0.20, "carbohydrate": 0.45, "fat": 0.35},
        sodium_mg_per_day=2300,
        fiber_g_per_day=22,
        saturated_fat_pct=0.08,
        added_sugar_pct=0.06,
        tags=("low_fodmap", "ibs"),
    )


def low_sodium_renal_diet(daily_energy_kcal: float = 2000) -> DietPlan:
    return DietPlan.from_targets(
        name="low_sodium_renal",
        description="Renal-friendly pattern with restricted sodium, potassium, and phosphorus.",
        daily_energy_kcal=daily_energy_kcal,
        macronutrient_pct={"protein": 0.12, "carbohydrate": 0.55, "fat": 0.33},
        sodium_mg_per_day=2000,
        fiber_g_per_day=25,
        saturated_fat_pct=0.07,
        added_sugar_pct=0.05,
        tags=("renal", "low_sodium"),
    )


def diabetic_diet(daily_energy_kcal: float = 1800) -> DietPlan:
    return DietPlan.from_targets(
        name="diabetic",
        description="Lower-carbohydrate, high-fibre pattern targeting glycaemic control.",
        daily_energy_kcal=daily_energy_kcal,
        macronutrient_pct={"protein": 0.25, "carbohydrate": 0.35, "fat": 0.40},
        sodium_mg_per_day=2300,
        fiber_g_per_day=35,
        saturated_fat_pct=0.07,
        added_sugar_pct=0.03,
        tags=("diabetes", "low_carb"),
    )


def vegan_diet(daily_energy_kcal: float = 2000) -> DietPlan:
    return DietPlan.from_targets(
        name="vegan",
        description="Whole-food plant-based pattern excluding all animal products.",
        daily_energy_kcal=daily_energy_kcal,
        macronutrient_pct={"protein": 0.15, "carbohydrate": 0.55, "fat": 0.30},
        sodium_mg_per_day=2000,
        fiber_g_per_day=40,
        saturated_fat_pct=0.05,
        added_sugar_pct=0.05,
        tags=("vegan", "plant_based"),
    )


def standard_diet(daily_energy_kcal: float = 2200) -> DietPlan:
    return DietPlan.from_targets(
        name="standard",
        description="Generic balanced reference diet.",
        daily_energy_kcal=daily_energy_kcal,
        macronutrient_pct={"protein": 0.15, "carbohydrate": 0.50, "fat": 0.35},
        sodium_mg_per_day=2300,
        fiber_g_per_day=28,
        saturated_fat_pct=0.10,
        added_sugar_pct=0.08,
        tags=("reference",),
    )


DIET_PRESETS: Dict[str, Callable[[float], DietPlan]] = {
    "mediterranean": mediterranean_diet,
    "dash": dash_diet,
    "keto": keto_diet,
    "low_fodmap": low_fodmap_diet,
    "low_sodium_renal": low_sodium_renal_diet,
    "diabetic": diabetic_diet,
    "vegan": vegan_diet,
    "standard": standard_diet,
}


def list_presets() -> List[str]:
    return sorted(DIET_PRESETS)
