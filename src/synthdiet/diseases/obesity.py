"""Weight-related diagnoses."""

from __future__ import annotations

from typing import TYPE_CHECKING, Mapping

from synthdiet.diseases.base import Disease, NutritionalConstraints
from synthdiet.diseases.registry import register

if TYPE_CHECKING:
    from synthdiet.patients.patient import Patient


@register
class Overweight(Disease):
    name = "overweight"
    icd10 = "E66.3"
    category = "metabolic"
    default_severity = "mild"
    severity_levels = ("mild",)

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            fiber_g_min=28.0,
            added_sugar_pct_max=0.08,
            notes=[
                "Target 5% body-weight reduction over 6 months as first goal.",
                "Recommended deficit: 300-500 kcal/day below estimated needs.",
            ],
        )


@register
class Obesity(Disease):
    """Obesity classified by BMI class (I, II, III)."""

    name = "obesity"
    icd10 = "E66.9"
    category = "metabolic"

    def __init__(self, bmi_class: str = "I", **kwargs) -> None:
        if bmi_class not in {"I", "II", "III"}:
            raise ValueError("bmi_class must be 'I', 'II', or 'III'")
        sev = {"I": "mild", "II": "moderate", "III": "severe"}[bmi_class]
        super().__init__(severity=kwargs.pop("severity", sev), bmi_class=bmi_class, **kwargs)
        self.bmi_class = bmi_class

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        deficit_note = {
            "I": "Aim for 5-10% weight loss; 500 kcal/day deficit.",
            "II": "Aim for 10-15% weight loss; 500-750 kcal/day deficit.",
            "III": "Consider very-low-calorie diet under supervision or bariatric referral.",
        }[self.bmi_class]
        return NutritionalConstraints(
            protein_pct_range=(0.20, 0.30),
            fiber_g_min=30.0,
            added_sugar_pct_max=0.05,
            saturated_fat_pct_max=0.08,
            encouraged_foods={"vegetables", "lean_protein", "whole_grains"},
            limited_foods={"ultra_processed_foods", "sugar_sweetened_beverages"},
            notes=[deficit_note, "Combine with ≥150 minutes/week of moderate activity."],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        bumps = {
            "I": {"crp_mg_l": 2.0, "fasting_insulin_uIU_ml": 4.0, "triglycerides_mg_dl": 20.0},
            "II": {"crp_mg_l": 4.0, "fasting_insulin_uIU_ml": 9.0, "triglycerides_mg_dl": 45.0},
            "III": {"crp_mg_l": 7.0, "fasting_insulin_uIU_ml": 15.0, "triglycerides_mg_dl": 75.0},
        }
        return bumps[self.bmi_class]
