"""Diabetes-related diagnoses."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Mapping

from synthdiet.diseases.base import Disease, NutritionalConstraints
from synthdiet.diseases.registry import register

if TYPE_CHECKING:
    from synthdiet.diets.base import DietPlan
    from synthdiet.patients.patient import Patient


@register
class Type1Diabetes(Disease):
    name = "type_1_diabetes"
    icd10 = "E10"
    category = "endocrine"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            carbohydrate_pct_range=(0.40, 0.50),
            protein_pct_range=(0.15, 0.20),
            fat_pct_range=(0.30, 0.35),
            saturated_fat_pct_max=0.10,
            added_sugar_pct_max=0.05,
            fiber_g_min=25.0,
            limited_foods={"sugar_sweetened_beverages", "candy"},
            notes=[
                "Carbohydrate counting recommended.",
                "Match insulin dose to meal carbohydrate content.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        severity_map = {"mild": (0.7, 30.0), "moderate": (1.4, 60.0), "severe": (2.5, 110.0)}
        a1c_bump, glucose_bump = severity_map[self.severity]
        return {
            "hba1c_pct": a1c_bump,
            "fasting_glucose_mg_dl": glucose_bump,
        }

    def response_to_diet(
        self,
        patient: "Patient",
        diet: "DietPlan",
        duration_weeks: int,
    ) -> Dict[str, float]:
        carb_pct = diet.macronutrient_distribution().get("carbohydrate", 0.5)
        weeks = max(duration_weeks, 1)
        a1c_delta = -0.02 * weeks if carb_pct <= 0.45 else 0.0
        return {"hba1c_pct": a1c_delta}


@register
class Type2Diabetes(Disease):
    name = "type_2_diabetes"
    icd10 = "E11"
    category = "endocrine"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            carbohydrate_pct_range=(0.30, 0.45),
            protein_pct_range=(0.20, 0.30),
            fat_pct_range=(0.30, 0.40),
            saturated_fat_pct_max=0.07,
            added_sugar_pct_max=0.05,
            fiber_g_min=30.0,
            sodium_mg_max=2300.0,
            limited_foods={
                "sugar_sweetened_beverages",
                "white_bread",
                "white_rice",
                "candy",
            },
            encouraged_foods={"non_starchy_vegetables", "legumes", "whole_grains"},
            notes=[
                "Favor low glycaemic index carbohydrates.",
                "Aim for 5-10% weight reduction if BMI > 25.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        severity_map = {
            "mild": (0.8, 25.0, 5.0),
            "moderate": (1.6, 55.0, 12.0),
            "severe": (2.8, 100.0, 25.0),
        }
        a1c_bump, glucose_bump, insulin_bump = severity_map[self.severity]
        return {
            "hba1c_pct": a1c_bump,
            "fasting_glucose_mg_dl": glucose_bump,
            "fasting_insulin_uIU_ml": insulin_bump,
            "triglycerides_mg_dl": 40.0,
            "hdl_mg_dl": -5.0,
        }

    def response_to_diet(
        self,
        patient: "Patient",
        diet: "DietPlan",
        duration_weeks: int,
    ) -> Dict[str, float]:
        macros = diet.macronutrient_distribution()
        carb_pct = macros.get("carbohydrate", 0.5)
        fiber = diet.fiber_g_per_day or 0.0
        weeks = max(duration_weeks, 1)

        a1c_delta = 0.0
        if carb_pct <= 0.40:
            a1c_delta -= 0.04 * weeks
        if fiber >= 30.0:
            a1c_delta -= 0.01 * weeks

        kcal_balance = diet.daily_energy_kcal - patient_estimated_needs(patient)
        weight_delta = (kcal_balance * 7 * weeks) / 7700.0  # rough kg conversion

        return {
            "hba1c_pct": a1c_delta,
            "fasting_glucose_mg_dl": a1c_delta * 28.7,
            "weight_kg": weight_delta,
        }


@register
class PreDiabetes(Disease):
    name = "prediabetes"
    icd10 = "R73.03"
    category = "endocrine"
    default_severity = "mild"
    severity_levels = ("mild", "moderate")

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            carbohydrate_pct_range=(0.35, 0.50),
            protein_pct_range=(0.15, 0.25),
            fat_pct_range=(0.30, 0.40),
            added_sugar_pct_max=0.06,
            fiber_g_min=28.0,
            notes=[
                "Lifestyle intervention can reduce progression to T2DM by ~58%.",
                "Target 7% weight loss if overweight.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        return {"hba1c_pct": 0.5, "fasting_glucose_mg_dl": 15.0}


@register
class GestationalDiabetes(Disease):
    name = "gestational_diabetes"
    icd10 = "O24.4"
    category = "endocrine"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            carbohydrate_pct_range=(0.40, 0.50),
            protein_pct_range=(0.20, 0.25),
            fat_pct_range=(0.30, 0.40),
            added_sugar_pct_max=0.05,
            fiber_g_min=28.0,
            notes=[
                "Spread carbohydrates across 3 small meals + 2-3 snacks.",
                "Avoid carbohydrate-heavy breakfast (dawn cortisol effect).",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        return {"fasting_glucose_mg_dl": 18.0, "hba1c_pct": 0.4}


def patient_estimated_needs(patient: "Patient") -> float:
    """Lightweight Mifflin-St Jeor estimation kept local to avoid circular imports."""
    from synthdiet.simulation.metabolism import total_daily_energy_expenditure

    return total_daily_energy_expenditure(patient)
