"""Musculoskeletal and rheumatologic conditions."""

from __future__ import annotations

from typing import TYPE_CHECKING, Mapping

from synthdiet.diseases.base import Disease, NutritionalConstraints
from synthdiet.diseases.registry import register

if TYPE_CHECKING:
    from synthdiet.patients.patient import Patient


@register
class Gout(Disease):
    name = "gout"
    icd10 = "M10"
    category = "rheumatologic"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            limited_foods={
                "organ_meats",
                "shellfish",
                "red_meat",
                "anchovies",
                "sardines",
                "beer",
                "fructose_corn_syrup",
            },
            encouraged_foods={"low_fat_dairy", "cherries", "coffee", "water"},
            notes=[
                "Target serum urate < 6 mg/dL.",
                "DASH-style diet reduces flare frequency.",
                "Hydration > 2 L/day reduces stone risk.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        return {"uric_acid_mg_dl": 2.5}


@register
class Osteoporosis(Disease):
    name = "osteoporosis"
    icd10 = "M81"
    category = "rheumatologic"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            encouraged_foods={
                "dairy",
                "fortified_plant_milk",
                "leafy_greens",
                "fatty_fish",
                "almonds",
            },
            limited_foods={"excess_caffeine", "excess_alcohol", "sugar_sweetened_beverages"},
            notes=[
                "Target 1000-1200 mg calcium and 800-1000 IU vitamin D daily.",
                "Adequate protein (~1.0-1.2 g/kg) supports bone matrix.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        return {"vitamin_d_25oh_ng_ml": -8.0, "calcium_mg_dl": -0.3}


@register
class Sarcopenia(Disease):
    name = "sarcopenia"
    icd10 = "M62.84"
    category = "rheumatologic"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            protein_pct_range=(0.20, 0.30),
            encouraged_foods={"lean_protein", "whey", "leucine_rich_foods", "fatty_fish"},
            notes=[
                "Target 1.2-1.5 g protein/kg body weight daily.",
                "Distribute protein evenly across meals (~25-30 g per meal).",
                "Pair with resistance training 2-3x/week.",
            ],
        )
