"""PREDIMED trial validation (simplified surrogate).

Reference
---------
Estruch R, Ros E, Salas-Salvado J, et al. (2018). "Primary prevention of
cardiovascular disease with a Mediterranean diet supplemented with extra-virgin
olive oil or nuts." NEJM 378:e34. doi:10.1056/NEJMoa1800389

The original endpoint is a hard composite CVD outcome (MI, stroke, CV death)
over 4.8 years; reproducing that requires a survival model we will only add
in a later milestone. As an interim surrogate we validate the LDL-cholesterol
reduction between Mediterranean + EVOO and a low-fat control diet, which
PREDIMED-Plus and earlier sub-studies put at ~-6 mg/dL over 12 months.
"""

from __future__ import annotations

import numpy as np

from synthdiet.diets.presets import mediterranean_diet, standard_diet
from synthdiet.generators import (
    CohortGenerator,
    CohortSpec,
    DiseaseSpec,
    DistributionPatientGenerator,
)
from synthdiet.simulation import DietSimulator
from synthdiet.validation.base import ValidationReport, ValidationTarget

PREDIMED_TARGET = ValidationTarget(
    name="PREDIMED (Mediterranean + EVOO vs low-fat, 12 mo LDL change)",
    citation="Estruch R et al. NEJM 2018;378:e34 (surrogate endpoint)",
    outcome="LDL cholesterol change (mg/dL)",
    expected_effect=-6.0,
    expected_ci_95=(-10.0, -2.0),
    tolerance=4.0,
    units="mg/dL",
    description="12 mo, CVD-risk adults",
)


def simulate(n_patients: int = 200, seed: int = 42) -> float:
    spec = CohortSpec(
        size=n_patients,
        diseases=[
            DiseaseSpec("dyslipidemia", prevalence=0.7),
            DiseaseSpec("hypertension", prevalence=0.5),
            DiseaseSpec("type_2_diabetes", prevalence=0.4),
        ],
        base_generator=DistributionPatientGenerator(age_mean=67, age_sd=6, seed=seed),
    )
    cohort = CohortGenerator(spec, seed=seed).generate()

    sim = DietSimulator(adherence=0.80)
    diffs = []
    for patient in cohort:
        med = sim.run(patient.clone(), mediterranean_diet(), duration_weeks=52)
        ctrl = sim.run(patient.clone(), standard_diet(), duration_weeks=52)
        baseline = med.timeline[0].biomarkers.get("ldl_mg_dl", 0.0)
        med_ldl = med.timeline[-1].biomarkers.get("ldl_mg_dl", baseline)
        ctrl_ldl = ctrl.timeline[-1].biomarkers.get("ldl_mg_dl", baseline)
        diffs.append(med_ldl - ctrl_ldl)
    return float(np.mean(diffs))


def validate(n_patients: int = 200, seed: int = 42) -> ValidationReport:
    effect = simulate(n_patients=n_patients, seed=seed)
    return ValidationReport(
        target=PREDIMED_TARGET,
        simulated_effect=effect,
        n_simulated=n_patients,
    )
