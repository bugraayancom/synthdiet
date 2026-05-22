"""Eating disorders."""

from __future__ import annotations

from typing import TYPE_CHECKING, Mapping

from synthdiet.diseases.base import Disease, NutritionalConstraints
from synthdiet.diseases.registry import register

if TYPE_CHECKING:
    from synthdiet.patients.patient import Patient


@register
class AnorexiaNervosa(Disease):
    name = "anorexia_nervosa"
    icd10 = "F50.0"
    category = "psychiatric"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            notes=[
                "Multidisciplinary management essential.",
                "Begin refeeding cautiously (start ~20 kcal/kg/day) to avoid refeeding syndrome.",
                "Monitor phosphate, potassium, magnesium and thiamine during refeeding.",
            ],
            encouraged_foods={"nutrient_dense_foods"},
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        return {
            "hemoglobin_g_dl": -1.0,
            "phosphate_mg_dl": -0.5,
            "potassium_mmol_l": -0.3,
            "magnesium_mg_dl": -0.2,
        }


@register
class BulimiaNervosa(Disease):
    name = "bulimia_nervosa"
    icd10 = "F50.2"
    category = "psychiatric"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            notes=[
                "Structured 3 meals + 2 snacks/day pattern reduces binge-purge cycles.",
                "Monitor electrolytes (especially potassium) and dental health.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        return {"potassium_mmol_l": -0.4, "sodium_mmol_l": -3.0}


@register
class BingeEatingDisorder(Disease):
    name = "binge_eating_disorder"
    icd10 = "F50.81"
    category = "psychiatric"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            notes=[
                "Regular structured meals; avoid restrictive dieting.",
                "Combine with CBT-E for best outcomes.",
            ],
            fiber_g_min=28.0,
            added_sugar_pct_max=0.08,
        )
