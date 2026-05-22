"""Energy expenditure equations."""

from __future__ import annotations

from typing import TYPE_CHECKING

from synthdiet.patients.demographics import Sex

if TYPE_CHECKING:
    from synthdiet.patients.patient import Patient


def mifflin_st_jeor(weight_kg: float, height_cm: float, age: int, sex: Sex) -> float:
    """Mifflin-St Jeor basal metabolic rate in kcal/day."""
    base = 10.0 * weight_kg + 6.25 * height_cm - 5.0 * age
    if sex == Sex.MALE:
        return base + 5.0
    if sex == Sex.FEMALE:
        return base - 161.0
    # Intersex: average of the two
    return base - 78.0


def harris_benedict(weight_kg: float, height_cm: float, age: int, sex: Sex) -> float:
    """Original Harris-Benedict (1919) BMR equation."""
    if sex == Sex.MALE:
        return 66.5 + 13.75 * weight_kg + 5.003 * height_cm - 6.755 * age
    if sex == Sex.FEMALE:
        return 655.1 + 9.563 * weight_kg + 1.850 * height_cm - 4.676 * age
    return (
        (66.5 + 13.75 * weight_kg + 5.003 * height_cm - 6.755 * age)
        + (655.1 + 9.563 * weight_kg + 1.850 * height_cm - 4.676 * age)
    ) / 2.0


def basal_metabolic_rate(patient: "Patient", equation: str = "mifflin_st_jeor") -> float:
    """Return BMR for ``patient`` using the requested equation."""
    if equation == "mifflin_st_jeor":
        fn = mifflin_st_jeor
    elif equation == "harris_benedict":
        fn = harris_benedict
    else:
        raise ValueError(f"Unknown equation {equation!r}")
    return fn(
        patient.anthropometrics.weight_kg,
        patient.anthropometrics.height_cm,
        patient.demographics.age,
        patient.demographics.sex,
    )


def total_daily_energy_expenditure(
    patient: "Patient", equation: str = "mifflin_st_jeor"
) -> float:
    """Estimated total daily energy expenditure (kcal)."""
    bmr = basal_metabolic_rate(patient, equation=equation)
    factor = patient.lifestyle.activity_level.factor
    # Hyperthyroidism is markedly hyper-metabolic.
    if patient.has_disease("hyperthyroidism"):
        factor *= 1.15
    if patient.has_disease("hypothyroidism"):
        factor *= 0.90
    if patient.has_disease("cancer_cachexia"):
        factor *= 1.20
    return bmr * factor
