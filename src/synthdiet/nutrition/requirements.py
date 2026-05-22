"""Dietary Reference Intakes (DRIs) for common nutrients.

Values are approximate adult reference intakes synthesised from the U.S.
National Academies of Sciences DRI tables. They are intentionally rounded and
should not be used to make individual clinical recommendations without a
qualified dietitian's review.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Mapping

if TYPE_CHECKING:
    from synthdiet.patients.patient import Patient


# Reference intakes for an adult (19-50 y). Sex-specific keys override.
_BASE_RDA: Mapping[str, Mapping[str, float]] = {
    "default": {
        "protein_g": 0.8,  # g/kg body weight, applied below
        "fiber_g": 25.0,
        "water_ml": 2700.0,
        "sodium_mg": 1500.0,
        "potassium_mg": 3400.0,
        "calcium_mg": 1000.0,
        "magnesium_mg": 320.0,
        "iron_mg": 18.0,
        "zinc_mg": 8.0,
        "vitamin_a_ug": 700.0,
        "vitamin_c_mg": 75.0,
        "vitamin_d_iu": 600.0,
        "vitamin_e_mg": 15.0,
        "vitamin_k_ug": 90.0,
        "thiamin_mg": 1.1,
        "riboflavin_mg": 1.1,
        "niacin_mg": 14.0,
        "vitamin_b6_mg": 1.3,
        "folate_ug": 400.0,
        "vitamin_b12_ug": 2.4,
        "choline_mg": 425.0,
    },
    "male": {
        "fiber_g": 38.0,
        "water_ml": 3700.0,
        "iron_mg": 8.0,
        "zinc_mg": 11.0,
        "vitamin_a_ug": 900.0,
        "vitamin_c_mg": 90.0,
        "choline_mg": 550.0,
    },
}

DRI_TABLE: Dict[str, Dict[str, float]] = {
    k: dict(v) for k, v in _BASE_RDA.items()
}


def daily_reference_intake(patient: "Patient") -> Dict[str, float]:
    """Return a dictionary of reference intake values for ``patient``."""
    rda = dict(DRI_TABLE["default"])
    if patient.demographics.sex.value == "male":
        rda.update(DRI_TABLE["male"])

    rda["protein_g"] = estimate_protein_requirement_g(patient)

    if patient.demographics.lactating:
        rda["protein_g"] += 25.0
        rda["water_ml"] = 3800.0
    elif patient.demographics.pregnancy_trimester is not None:
        rda["protein_g"] += 25.0
        rda["water_ml"] = 3000.0
        rda["folate_ug"] = 600.0
        rda["iron_mg"] = 27.0

    if patient.demographics.is_geriatric:
        rda["vitamin_d_iu"] = 800.0
        rda["calcium_mg"] = 1200.0

    return rda


def estimate_protein_requirement_g(patient: "Patient") -> float:
    """Return total daily protein requirement in grams."""
    weight = patient.anthropometrics.weight_kg
    per_kg = 0.8
    if patient.demographics.is_geriatric:
        per_kg = 1.2
    elif patient.demographics.is_pediatric:
        per_kg = 1.1
    if patient.has_disease("sarcopenia"):
        per_kg = max(per_kg, 1.3)
    return round(per_kg * weight, 1)
