"""Cardiovascular and related metabolic conditions."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Mapping

from synthdiet.diseases.base import Disease, NutritionalConstraints
from synthdiet.diseases.registry import register

if TYPE_CHECKING:
    from synthdiet.diets.base import DietPlan
    from synthdiet.patients.patient import Patient


@register
class Hypertension(Disease):
    name = "hypertension"
    icd10 = "I10"
    category = "cardiovascular"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        sodium_cap = {"mild": 2300.0, "moderate": 1800.0, "severe": 1500.0}[self.severity]
        return NutritionalConstraints(
            sodium_mg_max=sodium_cap,
            potassium_mg_max=None,
            saturated_fat_pct_max=0.07,
            fiber_g_min=30.0,
            limited_foods={"processed_meat", "salted_snacks", "canned_soup", "pickles"},
            encouraged_foods={"vegetables", "fruits", "low_fat_dairy", "nuts"},
            notes=[
                "DASH pattern is first-line dietary therapy.",
                "Target potassium intake 3500-5000 mg/day if renal function is normal.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        sbp_bump = {"mild": 10.0, "moderate": 25.0, "severe": 40.0}[self.severity]
        dbp_bump = {"mild": 5.0, "moderate": 12.0, "severe": 20.0}[self.severity]
        return {
            "systolic_bp_mmhg": sbp_bump,
            "diastolic_bp_mmhg": dbp_bump,
        }

    def response_to_diet(
        self,
        patient: "Patient",
        diet: "DietPlan",
        duration_weeks: int,
    ) -> Dict[str, float]:
        sodium = diet.sodium_mg_per_day or 3000.0
        weeks = max(duration_weeks, 1)
        sbp_delta = 0.0
        if sodium <= 1500:
            sbp_delta -= 0.6 * weeks
        elif sodium <= 2300:
            sbp_delta -= 0.3 * weeks
        return {"systolic_bp_mmhg": sbp_delta, "diastolic_bp_mmhg": sbp_delta / 2}


@register
class Dyslipidemia(Disease):
    name = "dyslipidemia"
    icd10 = "E78"
    category = "cardiovascular"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            fat_pct_range=(0.25, 0.35),
            saturated_fat_pct_max=0.06,
            cholesterol_mg_max=200.0,
            fiber_g_min=30.0,
            limited_foods={"butter", "palm_oil", "fatty_red_meat", "fried_foods"},
            encouraged_foods={"oily_fish", "oats", "legumes", "nuts", "olive_oil"},
            notes=[
                "Replace saturated with unsaturated fats.",
                "Include 10-25 g/day soluble fibre.",
                "Add 2 g/day plant stanols/sterols if available.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        sev = {"mild": (20.0, -3.0, 30.0), "moderate": (45.0, -8.0, 80.0),
               "severe": (75.0, -15.0, 150.0)}[self.severity]
        ldl_b, hdl_b, tg_b = sev
        return {
            "ldl_mg_dl": ldl_b,
            "hdl_mg_dl": hdl_b,
            "triglycerides_mg_dl": tg_b,
            "total_cholesterol_mg_dl": ldl_b + 20,
        }

    def response_to_diet(
        self,
        patient: "Patient",
        diet: "DietPlan",
        duration_weeks: int,
    ) -> Dict[str, float]:
        weeks = max(duration_weeks, 1)
        sat_pct = diet.saturated_fat_pct or 0.10
        fiber = diet.fiber_g_per_day or 15.0
        ldl_delta = 0.0
        if sat_pct <= 0.07:
            ldl_delta -= 1.0 * weeks
        if fiber >= 25:
            ldl_delta -= 0.5 * weeks
        return {"ldl_mg_dl": ldl_delta, "total_cholesterol_mg_dl": ldl_delta * 1.1}


@register
class MetabolicSyndrome(Disease):
    name = "metabolic_syndrome"
    icd10 = "E88.81"
    category = "cardiovascular"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            carbohydrate_pct_range=(0.35, 0.50),
            protein_pct_range=(0.20, 0.30),
            fat_pct_range=(0.25, 0.35),
            saturated_fat_pct_max=0.07,
            added_sugar_pct_max=0.05,
            sodium_mg_max=2000.0,
            fiber_g_min=30.0,
            notes=[
                "Mediterranean and DASH patterns both show benefit.",
                "Combine with 150 min/week moderate exercise.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        return {
            "fasting_glucose_mg_dl": 15.0,
            "triglycerides_mg_dl": 60.0,
            "hdl_mg_dl": -8.0,
            "systolic_bp_mmhg": 8.0,
            "diastolic_bp_mmhg": 5.0,
        }
