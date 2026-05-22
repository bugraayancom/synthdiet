"""Endocrine conditions excluding diabetes."""

from __future__ import annotations

from typing import TYPE_CHECKING, Mapping

from synthdiet.diseases.base import Disease, NutritionalConstraints
from synthdiet.diseases.registry import register

if TYPE_CHECKING:
    from synthdiet.patients.patient import Patient


@register
class Hypothyroidism(Disease):
    name = "hypothyroidism"
    icd10 = "E03"
    category = "endocrine"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            fiber_g_min=30.0,
            encouraged_foods={"iodine_rich_foods", "selenium_rich_foods", "zinc_rich_foods"},
            limited_foods={"raw_goitrogenic_vegetables"},
            notes=[
                "Take levothyroxine on empty stomach; separate from calcium/iron by 4 h.",
                "Ensure adequate iodine (150 µg/day) and selenium (55 µg/day).",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        bumps = {"mild": (4.0, -0.2), "moderate": (15.0, -0.4), "severe": (40.0, -0.7)}
        tsh, ft4 = bumps[self.severity]
        return {"tsh_uIU_ml": tsh, "free_t4_ng_dl": ft4, "ldl_mg_dl": 20.0}


@register
class Hyperthyroidism(Disease):
    name = "hyperthyroidism"
    icd10 = "E05"
    category = "endocrine"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            protein_pct_range=(0.18, 0.25),
            fiber_g_min=25.0,
            encouraged_foods={"cruciferous_vegetables", "calcium_rich_foods"},
            limited_foods={"iodine_rich_seaweed", "high_iodine_supplements"},
            notes=[
                "Increase energy intake to match hypermetabolism (often +10-20%).",
                "Adequate calcium and vitamin D to protect bone density.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        bumps = {"mild": (-0.3, 0.4), "moderate": (-0.39, 0.9), "severe": (-0.4, 1.8)}
        tsh, ft4 = bumps[self.severity]
        return {"tsh_uIU_ml": tsh, "free_t4_ng_dl": ft4}


@register
class PCOS(Disease):
    """Polycystic Ovary Syndrome."""

    name = "pcos"
    icd10 = "E28.2"
    category = "endocrine"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            carbohydrate_pct_range=(0.35, 0.45),
            protein_pct_range=(0.20, 0.30),
            fat_pct_range=(0.30, 0.40),
            saturated_fat_pct_max=0.07,
            added_sugar_pct_max=0.05,
            fiber_g_min=28.0,
            encouraged_foods={"low_glycaemic_carbs", "omega3_rich_fish", "legumes"},
            notes=[
                "Insulin sensitivity improves with 5-10% weight loss.",
                "Inositol supplementation has supporting evidence.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        return {
            "fasting_insulin_uIU_ml": 8.0,
            "fasting_glucose_mg_dl": 8.0,
            "triglycerides_mg_dl": 30.0,
            "hdl_mg_dl": -4.0,
        }
