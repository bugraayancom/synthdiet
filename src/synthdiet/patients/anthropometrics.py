"""Anthropometric measurements (height, weight, body composition, etc.)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from synthdiet.utils.validators import ensure_positive


@dataclass
class Anthropometrics:
    """Anthropometric attributes of a patient.

    All measurements use SI units: kilograms, centimetres, and percentages.
    """

    height_cm: float
    weight_kg: float
    waist_cm: Optional[float] = None
    hip_cm: Optional[float] = None
    neck_cm: Optional[float] = None
    body_fat_pct: Optional[float] = None
    muscle_mass_kg: Optional[float] = None
    bone_mass_kg: Optional[float] = None
    # Hall body composition model compartments. Filled in lazily by
    # :func:`initialise_body_composition` or by the Hall simulator on first use.
    fat_mass_kg: Optional[float] = None
    lean_mass_kg: Optional[float] = None
    extracellular_water_l: Optional[float] = None
    glycogen_kg: Optional[float] = None

    def __post_init__(self) -> None:
        ensure_positive(self.height_cm, "height_cm")
        ensure_positive(self.weight_kg, "weight_kg")
        if self.waist_cm is not None:
            ensure_positive(self.waist_cm, "waist_cm")
        if self.hip_cm is not None:
            ensure_positive(self.hip_cm, "hip_cm")

    @property
    def height_m(self) -> float:
        return self.height_cm / 100.0

    @property
    def bmi(self) -> float:
        """Body Mass Index in kg/m^2."""
        return self.weight_kg / (self.height_m ** 2)

    @property
    def bmi_category(self) -> str:
        """WHO BMI classification."""
        bmi = self.bmi
        if bmi < 18.5:
            return "underweight"
        if bmi < 25:
            return "normal"
        if bmi < 30:
            return "overweight"
        if bmi < 35:
            return "obesity_class_I"
        if bmi < 40:
            return "obesity_class_II"
        return "obesity_class_III"

    @property
    def waist_to_hip_ratio(self) -> Optional[float]:
        if self.waist_cm is None or self.hip_cm is None:
            return None
        return self.waist_cm / self.hip_cm

    @property
    def waist_to_height_ratio(self) -> Optional[float]:
        if self.waist_cm is None:
            return None
        return self.waist_cm / self.height_cm

    def ideal_body_weight_kg(self, sex: str) -> float:
        """Devine formula for ideal body weight."""
        inches_over_5ft = max(0.0, (self.height_cm - 152.4) / 2.54)
        base = 50.0 if sex == "male" else 45.5
        return base + 2.3 * inches_over_5ft

    def estimate_body_fat_pct(self, sex: str, age: int) -> float:
        """Deurenberg (1991) BMI-based body-fat estimate (population mean).

        Returns body fat as a percentage of total body mass. Useful for
        initialising the Hall body composition compartments when DXA data is
        unavailable.
        """
        sex_factor = 1 if sex == "male" else 0
        return 1.20 * self.bmi + 0.23 * age - 10.8 * sex_factor - 5.4
