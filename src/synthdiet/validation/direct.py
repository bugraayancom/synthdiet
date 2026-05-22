"""DiRECT trial validation.

Reference
---------
Lean MEJ, Leslie WS, Barnes AC, et al. (2018). "Primary care-led weight
management for remission of type 2 diabetes (DiRECT): an open-label,
cluster-randomised trial." Lancet 391:541-551.
doi:10.1016/S0140-6736(17)33102-1

Expected effect: ~10 kg mean weight loss at 12 months in the intensive
calorie-restricted arm (vs. ~1 kg in usual care).
"""

from __future__ import annotations

import numpy as np

from synthdiet.diets.presets import diabetic_diet, standard_diet
from synthdiet.generators import (
    CohortGenerator,
    CohortSpec,
    DiseaseSpec,
    DistributionPatientGenerator,
)
from synthdiet.simulation import DietSimulator
from synthdiet.validation.base import ValidationReport, ValidationTarget

DIRECT_TARGET = ValidationTarget(
    name="DiRECT (very-low-calorie diet vs usual care, 12 mo weight change)",
    citation="Lean MEJ et al. Lancet 2018;391:541-551",
    outcome="weight change (kg)",
    expected_effect=-10.0,
    expected_ci_95=(-12.0, -8.0),
    tolerance=3.0,
    units="kg",
    description="12 mo, T2DM adults BMI 27-45",
)


def simulate(n_patients: int = 100, seed: int = 42) -> float:
    spec = CohortSpec(
        size=n_patients,
        diseases=[DiseaseSpec("type_2_diabetes", prevalence=1.0)],
        base_generator=DistributionPatientGenerator(
            age_mean=54, age_sd=8,
            bmi_overrides={"male": 35.5, "female": 35.5, "male_sd": 4.0, "female_sd": 4.0},
            seed=seed,
        ),
    )
    cohort = CohortGenerator(spec, seed=seed).generate()

    intensive_diet = diabetic_diet(daily_energy_kcal=900)
    control_diet = standard_diet(daily_energy_kcal=2000)

    sim = DietSimulator(adherence=0.65, engine="hall_2011")
    intensive_losses, control_losses = [], []
    for patient in cohort:
        ir = sim.run(patient.clone(), intensive_diet, duration_weeks=52)
        cr = sim.run(patient.clone(), control_diet, duration_weeks=52)
        intensive_losses.append(ir.weight_change_kg)
        control_losses.append(cr.weight_change_kg)
    return float(np.mean(intensive_losses) - np.mean(control_losses))


def validate(n_patients: int = 100, seed: int = 42) -> ValidationReport:
    effect = simulate(n_patients=n_patients, seed=seed)
    return ValidationReport(
        target=DIRECT_TARGET,
        simulated_effect=effect,
        n_simulated=n_patients,
    )
