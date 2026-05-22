"""Renal diseases."""

from __future__ import annotations

from typing import TYPE_CHECKING, Mapping

from synthdiet.diseases.base import Disease, NutritionalConstraints
from synthdiet.diseases.registry import register

if TYPE_CHECKING:
    from synthdiet.patients.patient import Patient


@register
class ChronicKidneyDisease(Disease):
    """Chronic kidney disease, stages 1-5 modelled via ``stage`` detail."""

    name = "chronic_kidney_disease"
    icd10 = "N18"
    category = "renal"
    severity_levels = ("mild", "moderate", "severe")

    def __init__(self, stage: int = 3, on_dialysis: bool = False, **kwargs) -> None:
        if stage not in {1, 2, 3, 4, 5}:
            raise ValueError("CKD stage must be 1-5")
        sev = {1: "mild", 2: "mild", 3: "moderate", 4: "severe", 5: "severe"}[stage]
        super().__init__(severity=kwargs.pop("severity", sev), stage=stage,
                         on_dialysis=on_dialysis, **kwargs)
        self.stage = stage
        self.on_dialysis = on_dialysis

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        # Protein recommendations vary by stage and dialysis status.
        if self.on_dialysis:
            protein_pct = (0.18, 0.22)
            protein_note = "Dialysis: 1.2-1.4 g protein/kg body weight per day."
        elif self.stage >= 4:
            protein_pct = (0.08, 0.12)
            protein_note = "Stage 4-5 (predialysis): 0.6-0.8 g protein/kg/day."
        elif self.stage == 3:
            protein_pct = (0.12, 0.15)
            protein_note = "Stage 3: 0.8 g protein/kg/day."
        else:
            protein_pct = (0.15, 0.20)
            protein_note = "Stages 1-2: standard protein intake."

        sodium = 2000.0 if not self.on_dialysis else 1800.0
        potassium = 3000.0 if self.stage >= 4 else 4000.0
        phosphorus = 800.0 if self.stage >= 4 else 1200.0
        fluid = 1500.0 if self.on_dialysis else None

        return NutritionalConstraints(
            protein_pct_range=protein_pct,
            sodium_mg_max=sodium,
            potassium_mg_max=potassium,
            phosphorus_mg_max=phosphorus,
            fluid_ml_max=fluid,
            limited_foods={
                "processed_meats",
                "dark_cola",
                "high_potassium_fruits",
                "whole_grain_breads",
                "dairy",
            },
            encouraged_foods={"apples", "berries", "cauliflower", "white_rice"},
            notes=[
                protein_note,
                f"CKD stage {self.stage}{' on dialysis' if self.on_dialysis else ''}.",
                "Monitor potassium and phosphorus closely.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        stage_egfr = {1: 95.0, 2: 75.0, 3: 50.0, 4: 25.0, 5: 10.0}
        return {
            "egfr_ml_min_1_73m2": stage_egfr[self.stage] - 90.0,
            "creatinine_mg_dl": {1: 0.0, 2: 0.2, 3: 0.6, 4: 1.5, 5: 4.0}[self.stage],
            "bun_mg_dl": {1: 0.0, 2: 3.0, 3: 8.0, 4: 25.0, 5: 60.0}[self.stage],
            "potassium_mmol_l": {1: 0.0, 2: 0.1, 3: 0.3, 4: 0.6, 5: 1.0}[self.stage],
            "phosphate_mg_dl": {1: 0.0, 2: 0.0, 3: 0.2, 4: 0.8, 5: 1.6}[self.stage],
        }


@register
class NephroticSyndrome(Disease):
    name = "nephrotic_syndrome"
    icd10 = "N04"
    category = "renal"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            protein_pct_range=(0.12, 0.16),
            sodium_mg_max=1500.0,
            saturated_fat_pct_max=0.07,
            cholesterol_mg_max=200.0,
            fluid_ml_max=1500.0,
            notes=[
                "Replace protein losses, but avoid high-protein diets.",
                "Restrict sodium aggressively to manage oedema.",
            ],
        )

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        return {"ldl_mg_dl": 60.0, "triglycerides_mg_dl": 80.0}


@register
class KidneyStones(Disease):
    name = "kidney_stones"
    icd10 = "N20"
    category = "renal"

    def __init__(self, stone_type: str = "calcium_oxalate", **kwargs) -> None:
        super().__init__(stone_type=stone_type, **kwargs)
        self.stone_type = stone_type

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        notes = ["Aim for ≥ 2.5 L urine output daily."]
        limited = {"oxalate_rich_foods", "salted_snacks", "soda"}
        if self.stone_type == "uric_acid":
            limited |= {"organ_meats", "shellfish", "beer"}
            notes.append("Limit purines; alkalinise urine with citrus fruits.")
        elif self.stone_type == "calcium_oxalate":
            notes.append("Maintain 1000-1200 mg calcium with meals to bind oxalate.")
        return NutritionalConstraints(
            sodium_mg_max=2000.0,
            limited_foods=limited,
            encouraged_foods={"water", "citrus_fruits"},
            notes=notes,
        )
