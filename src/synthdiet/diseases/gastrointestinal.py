"""Gastrointestinal diseases."""

from __future__ import annotations

from typing import TYPE_CHECKING, Mapping

from synthdiet.diseases.base import Disease, NutritionalConstraints
from synthdiet.diseases.registry import register

if TYPE_CHECKING:
    from synthdiet.patients.patient import Patient


@register
class CeliacDisease(Disease):
    name = "celiac_disease"
    icd10 = "K90.0"
    category = "gastrointestinal"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            forbidden_foods={"wheat", "barley", "rye", "spelt", "kamut", "triticale"},
            encouraged_foods={"quinoa", "buckwheat", "millet", "naturally_gf_oats"},
            fiber_g_min=25.0,
            notes=[
                "Lifelong strict gluten-free diet (< 20 ppm gluten).",
                "Monitor iron, folate, B12, vitamin D, calcium status.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        return {
            "hemoglobin_g_dl": -1.5,
            "ferritin_ng_ml": -20.0,
            "vitamin_d_25oh_ng_ml": -8.0,
        }


@register
class IBS(Disease):
    """Irritable Bowel Syndrome."""

    name = "ibs"
    icd10 = "K58"
    category = "gastrointestinal"

    def __init__(self, subtype: str = "mixed", **kwargs) -> None:
        if subtype not in {"diarrhea", "constipation", "mixed", "unsubtyped"}:
            raise ValueError("IBS subtype must be 'diarrhea', 'constipation', 'mixed', or 'unsubtyped'")
        super().__init__(subtype=subtype, **kwargs)
        self.subtype = subtype

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        notes = ["Trial a structured low-FODMAP diet for 4-6 weeks, then reintroduce."]
        if self.subtype == "constipation":
            notes.append("Increase soluble fibre gradually; ensure adequate fluids.")
        if self.subtype == "diarrhea":
            notes.append("Limit insoluble fibre and caffeine.")
        return NutritionalConstraints(
            limited_foods={"high_fodmap_fruits", "onion", "garlic", "wheat", "lactose"},
            encouraged_foods={"oats", "low_fodmap_vegetables", "kiwi", "psyllium"},
            fiber_g_min=22.0,
            notes=notes,
        )


@register
class CrohnsDisease(Disease):
    name = "crohns_disease"
    icd10 = "K50"
    category = "gastrointestinal"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            protein_pct_range=(0.18, 0.25),
            fiber_g_min=18.0,
            limited_foods={"raw_vegetables", "popcorn", "nuts_with_skin", "alcohol"},
            encouraged_foods={"lean_protein", "cooked_vegetables", "omega3_rich_fish"},
            notes=[
                "Adjust fibre based on stricturing disease.",
                "Monitor B12 (terminal ileum), iron, vitamin D, zinc.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        return {
            "hemoglobin_g_dl": -1.2,
            "vitamin_b12_pg_ml": -120.0,
            "vitamin_d_25oh_ng_ml": -8.0,
            "crp_mg_l": 12.0,
        }


@register
class UlcerativeColitis(Disease):
    name = "ulcerative_colitis"
    icd10 = "K51"
    category = "gastrointestinal"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            protein_pct_range=(0.18, 0.25),
            limited_foods={"alcohol", "spicy_foods", "high_sulfur_foods"},
            encouraged_foods={"omega3_rich_fish", "well_cooked_vegetables"},
            notes=[
                "Track flare triggers individually.",
                "During flares: low-residue diet may help.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        return {"hemoglobin_g_dl": -1.0, "ferritin_ng_ml": -25.0, "crp_mg_l": 8.0}


@register
class GERD(Disease):
    name = "gerd"
    icd10 = "K21.9"
    category = "gastrointestinal"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            limited_foods={
                "coffee",
                "chocolate",
                "mint",
                "tomato_sauce",
                "citrus_juice",
                "fried_foods",
                "alcohol",
                "carbonated_beverages",
            },
            notes=[
                "Smaller, more frequent meals.",
                "Avoid eating 2-3 hours before lying down.",
                "Elevate head of bed; weight loss helps when BMI > 25.",
            ],
        )
