"""Liver diseases."""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Mapping

from synthdiet.diseases.base import Disease, NutritionalConstraints
from synthdiet.diseases.registry import register

if TYPE_CHECKING:
    from synthdiet.diets.base import DietPlan
    from synthdiet.patients.patient import Patient


@register
class NAFLD(Disease):
    """Non-Alcoholic Fatty Liver Disease."""

    name = "nafld"
    icd10 = "K76.0"
    category = "hepatic"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            carbohydrate_pct_range=(0.35, 0.45),
            fat_pct_range=(0.30, 0.35),
            saturated_fat_pct_max=0.07,
            added_sugar_pct_max=0.05,
            fiber_g_min=30.0,
            limited_foods={"fructose_corn_syrup", "sugar_sweetened_beverages", "alcohol"},
            encouraged_foods={"oily_fish", "olive_oil", "leafy_greens", "berries"},
            notes=[
                "Mediterranean diet first-line.",
                "Avoid alcohol; target 7-10% weight loss over 6-12 months.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        sev = {"mild": (10.0, 5.0), "moderate": (35.0, 20.0), "severe": (75.0, 45.0)}
        alt, ast = sev[self.severity]
        return {"alt_u_l": alt, "ast_u_l": ast, "ggt_u_l": alt * 0.6}

    def response_to_diet(
        self,
        patient: "Patient",
        diet: "DietPlan",
        duration_weeks: int,
    ) -> Dict[str, float]:
        weeks = max(duration_weeks, 1)
        sugar = diet.added_sugar_pct or 0.10
        sat = diet.saturated_fat_pct or 0.10
        alt_delta = 0.0
        if sugar <= 0.05:
            alt_delta -= 0.4 * weeks
        if sat <= 0.07:
            alt_delta -= 0.2 * weeks
        return {"alt_u_l": alt_delta, "ast_u_l": alt_delta * 0.6}


@register
class Cirrhosis(Disease):
    name = "cirrhosis"
    icd10 = "K74"
    category = "hepatic"

    def __init__(
        self,
        child_pugh_class: str = "B",
        ascites: bool = False,
        encephalopathy: bool = False,
        **kwargs,
    ) -> None:
        if child_pugh_class not in {"A", "B", "C"}:
            raise ValueError("child_pugh_class must be 'A', 'B', or 'C'")
        sev = {"A": "mild", "B": "moderate", "C": "severe"}[child_pugh_class]
        super().__init__(
            severity=kwargs.pop("severity", sev),
            child_pugh_class=child_pugh_class,
            ascites=ascites,
            encephalopathy=encephalopathy,
            **kwargs,
        )
        self.child_pugh_class = child_pugh_class
        self.ascites = ascites
        self.encephalopathy = encephalopathy

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        sodium = 2000.0 if not self.ascites else 1500.0
        protein_pct = (0.18, 0.22)  # 1.2-1.5 g/kg typical
        if self.encephalopathy:
            protein_pct = (0.12, 0.15)
        return NutritionalConstraints(
            protein_pct_range=protein_pct,
            sodium_mg_max=sodium,
            fluid_ml_max=1500.0 if self.ascites else None,
            limited_foods={"alcohol", "raw_seafood", "high_sodium_foods"},
            encouraged_foods={"plant_proteins", "branched_chain_amino_acids"},
            notes=[
                f"Child-Pugh {self.child_pugh_class}.",
                "Frequent small meals; bedtime snack reduces muscle catabolism.",
                "Prefer plant protein sources in hepatic encephalopathy.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        bumps = {
            "A": (30.0, 25.0, 0.5),
            "B": (75.0, 55.0, 1.5),
            "C": (140.0, 110.0, 3.0),
        }[self.child_pugh_class]
        alt, ast, bili = bumps
        return {"alt_u_l": alt, "ast_u_l": ast, "ggt_u_l": alt}
