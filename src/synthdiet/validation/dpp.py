"""Diabetes Prevention Program (DPP) trial validation.

Reference
---------
Knowler WC, Barrett-Connor E, Fowler SE, et al. (2002). "Reduction in the
incidence of type 2 diabetes with lifestyle intervention or metformin."
NEJM 346:393-403. doi:10.1056/NEJMoa012512

Expected effect: ~5.6 kg weight loss in the lifestyle intervention arm vs
~0.1 kg in placebo at 12 months in adults with impaired glucose tolerance.
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

DPP_TARGET = ValidationTarget(
    name="DPP (lifestyle vs placebo, 12 mo weight change difference)",
    citation="Knowler WC et al. NEJM 2002;346:393-403",
    outcome="weight change difference (kg)",
    expected_effect=-5.5,
    expected_ci_95=(-6.5, -4.5),
    tolerance=2.5,
    units="kg",
    description="12 mo, prediabetic adults",
)


def simulate(n_patients: int = 150, seed: int = 42) -> float:
    spec = CohortSpec(
        size=n_patients,
        diseases=[DiseaseSpec("prediabetes", prevalence=1.0)],
        base_generator=DistributionPatientGenerator(
            age_mean=51, age_sd=10,
            bmi_overrides={"male": 33.0, "female": 33.0, "male_sd": 4.5, "female_sd": 4.5},
            seed=seed,
        ),
    )
    cohort = CohortGenerator(spec, seed=seed).generate()

    lifestyle = diabetic_diet(daily_energy_kcal=1500)
    placebo = standard_diet(daily_energy_kcal=2050)
    sim = DietSimulator(adherence=0.65, engine="hall_2011")

    intervention, control = [], []
    for patient in cohort:
        a = sim.run(patient.clone(), lifestyle, duration_weeks=52)
        b = sim.run(patient.clone(), placebo, duration_weeks=52)
        intervention.append(a.weight_change_kg)
        control.append(b.weight_change_kg)
    return float(np.mean(intervention) - np.mean(control))


def validate(n_patients: int = 150, seed: int = 42) -> ValidationReport:
    effect = simulate(n_patients=n_patients, seed=seed)
    return ValidationReport(
        target=DPP_TARGET,
        simulated_effect=effect,
        n_simulated=n_patients,
    )
