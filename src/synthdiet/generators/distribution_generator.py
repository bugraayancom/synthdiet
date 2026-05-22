"""Distribution-based patient generator.

Anthropometrics are sampled from realistic-ish marginal distributions taken
from NHANES adult means (heights are normal, weights are log-normal-ish). Lab
biomarkers are sampled around their reference midpoint with bounded noise.

This generator does *not* preserve cross-feature correlations
(e.g. height ↔ weight). For correlated draws use
:class:`~synthdiet.generators.CopulaPatientGenerator`.
"""

from __future__ import annotations

from typing import Mapping, Optional

import numpy as np

from synthdiet.generators.base import PatientGenerator
from synthdiet.patients.anthropometrics import Anthropometrics
from synthdiet.patients.biomarkers import ADULT_REFERENCE_RANGES, Biomarkers
from synthdiet.patients.demographics import Demographics, Sex
from synthdiet.patients.lifestyle import ActivityLevel, Lifestyle
from synthdiet.patients.patient import Patient

# Approximate adult population parameters used by the generator.
_HEIGHT_PARAMS = {
    Sex.MALE: (175.4, 7.0),
    Sex.FEMALE: (161.5, 6.5),
    Sex.INTERSEX: (168.5, 8.0),
}
_BMI_PARAMS = (27.8, 6.0)  # mean, sd (NHANES adult ~ 27-29 kg/m²)


class DistributionPatientGenerator(PatientGenerator):
    """Sample patients from marginal distributions."""

    def __init__(
        self,
        sex_ratio_female: float = 0.51,
        age_mean: float = 45.0,
        age_sd: float = 17.0,
        min_age: int = 18,
        max_age: int = 90,
        bmi_overrides: Optional[Mapping[str, float]] = None,
        seed=None,
    ) -> None:
        super().__init__(seed=seed)
        self.sex_ratio_female = float(sex_ratio_female)
        self.age_mean = float(age_mean)
        self.age_sd = float(age_sd)
        self.min_age = int(min_age)
        self.max_age = int(max_age)
        self.bmi_overrides = dict(bmi_overrides or {})

    def sample(self) -> Patient:
        sex = Sex.FEMALE if self.rng.random() < self.sex_ratio_female else Sex.MALE
        age = int(np.clip(self.rng.normal(self.age_mean, self.age_sd),
                          self.min_age, self.max_age))
        height_mean, height_sd = _HEIGHT_PARAMS[sex]
        height = float(np.clip(self.rng.normal(height_mean, height_sd),
                               height_mean - 3 * height_sd,
                               height_mean + 3 * height_sd))
        bmi_mean = self.bmi_overrides.get(sex.value, _BMI_PARAMS[0])
        bmi_sd = self.bmi_overrides.get(f"{sex.value}_sd", _BMI_PARAMS[1])
        bmi = float(np.clip(self.rng.normal(bmi_mean, bmi_sd), 15.0, 55.0))
        weight = bmi * (height / 100.0) ** 2

        waist = self._sample_waist(sex, bmi)
        hip = waist + float(self.rng.normal(8.0 if sex == Sex.FEMALE else 0.0, 4.0))

        activity = ActivityLevel(
            self.rng.choice(
                [a.value for a in ActivityLevel],
                p=[0.30, 0.30, 0.20, 0.12, 0.06, 0.02],
            )
        )

        patient = Patient(
            demographics=Demographics(age=age, sex=sex),
            anthropometrics=Anthropometrics(
                height_cm=height,
                weight_kg=weight,
                waist_cm=waist,
                hip_cm=hip,
            ),
            lifestyle=Lifestyle(activity_level=activity),
            biomarkers=self._sample_biomarkers(),
        )
        return patient

    def _sample_waist(self, sex: Sex, bmi: float) -> float:
        base = 70 if sex == Sex.FEMALE else 80
        return float(base + 1.6 * (bmi - 22) + self.rng.normal(0, 4))

    def _sample_biomarkers(self) -> Biomarkers:
        values = {}
        for name, (low, high) in ADULT_REFERENCE_RANGES.items():
            lo = low if low is not None else 0.0
            hi = high if high is not None else lo * 1.5 + 1.0
            mid = (lo + hi) / 2
            spread = (hi - lo) / 4 if hi > lo else max(lo * 0.05, 0.1)
            values[name] = float(np.clip(self.rng.normal(mid, spread), lo * 0.5, hi * 1.5))
        return Biomarkers(values=values)
