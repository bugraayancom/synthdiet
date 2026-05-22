"""Look AHEAD trial validation.

Reference
---------
Look AHEAD Research Group. (2007). "Reduction in weight and cardiovascular
disease risk factors in individuals with type 2 diabetes: One-year results of
the Look AHEAD trial." Diabetes Care 30:1374-1383.

Expected effect: ~8.6 kg (8.6%) weight loss at 1 year in the intensive
lifestyle intervention vs. ~0.7 kg in the diabetes support and education
control arm. HbA1c falls by ~0.7 percentage points in ILI vs ~0.1 in control.
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

LOOK_AHEAD_TARGET = ValidationTarget(
    name="Look AHEAD (ILI vs DSE, 12 mo weight loss difference)",
    citation="Look AHEAD Research Group. Diabetes Care 2007;30:1374-83",
    outcome="weight change difference (kg)",
    expected_effect=-7.9,
    expected_ci_95=(-9.0, -7.0),
    tolerance=3.0,
    units="kg",
    description="12 mo, T2DM, BMI >=25",
)


def simulate(n_patients: int = 150, seed: int = 42) -> float:
    spec = CohortSpec(
        size=n_patients,
        diseases=[DiseaseSpec("type_2_diabetes", prevalence=1.0)],
        base_generator=DistributionPatientGenerator(
            age_mean=58, age_sd=7,
            bmi_overrides={"male": 36.0, "female": 36.0, "male_sd": 5.0, "female_sd": 5.0},
            seed=seed,
        ),
    )
    cohort = CohortGenerator(spec, seed=seed).generate()

    ili = diabetic_diet(daily_energy_kcal=1300)
    dse = standard_diet(daily_energy_kcal=2000)
    sim = DietSimulator(adherence=0.70, engine="hall_2011")

    ili_losses, dse_losses = [], []
    for patient in cohort:
        r1 = sim.run(patient.clone(), ili, duration_weeks=52)
        r2 = sim.run(patient.clone(), dse, duration_weeks=52)
        ili_losses.append(r1.weight_change_kg)
        dse_losses.append(r2.weight_change_kg)
    return float(np.mean(ili_losses) - np.mean(dse_losses))


def validate(n_patients: int = 150, seed: int = 42) -> ValidationReport:
    effect = simulate(n_patients=n_patients, seed=seed)
    return ValidationReport(
        target=LOOK_AHEAD_TARGET,
        simulated_effect=effect,
        n_simulated=n_patients,
    )
