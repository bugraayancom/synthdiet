"""Oncology-related nutritional disorders."""

from __future__ import annotations

from typing import TYPE_CHECKING, Mapping

from synthdiet.diseases.base import Disease, NutritionalConstraints
from synthdiet.diseases.registry import register

if TYPE_CHECKING:
    from synthdiet.patients.patient import Patient


@register
class CancerCachexia(Disease):
    name = "cancer_cachexia"
    icd10 = "R64"
    category = "oncology"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            protein_pct_range=(0.20, 0.30),
            encouraged_foods={
                "high_calorie_dense_foods",
                "omega3_rich_fish",
                "oral_nutrition_supplements",
            },
            notes=[
                "Target ≥ 1.2 g protein/kg/day (1.5 g if severe).",
                "Energy needs 30-35 kcal/kg/day; consider EPA 2 g/day.",
                "Frequent small meals improve intake; manage taste/nausea actively.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        return {"crp_mg_l": 15.0, "hemoglobin_g_dl": -1.5}
