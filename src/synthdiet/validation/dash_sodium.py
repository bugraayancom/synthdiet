"""DASH-Sodium trial validation.

Reference
---------
Sacks FM, Svetkey LP, Vollmer WM, et al. (2001). "Effects on Blood Pressure
of Reduced Dietary Sodium and the Dietary Approaches to Stop Hypertension
(DASH) Diet." NEJM 344:3-10. doi:10.1056/NEJM200101043440101

Expected effect: in hypertensive participants, switching from a high-sodium
control diet (~3300 mg/day) to a low-sodium DASH diet (~1500 mg/day) reduces
systolic blood pressure by ~11.5 mmHg (95% CI -13.5, -9.5) over 30 days.
"""

from __future__ import annotations

import numpy as np

from synthdiet.diets.presets import dash_diet, standard_diet
from synthdiet.generators import (
    CohortGenerator,
    CohortSpec,
    DiseaseSpec,
    DistributionPatientGenerator,
)
from synthdiet.simulation import DietSimulator
from synthdiet.validation.base import ValidationReport, ValidationTarget

DASH_SODIUM_TARGET = ValidationTarget(
    name="DASH-Sodium (hypertensive subgroup, low Na vs high Na on DASH diet)",
    citation="Sacks FM et al. NEJM 2001;344:3-10",
    outcome="systolic BP change (mmHg)",
    expected_effect=-11.5,
    expected_ci_95=(-13.5, -9.5),
    tolerance=4.0,
    units="mmHg",
    description="30 days, hypertensive adults",
)


def simulate(n_patients: int = 200, seed: int = 42) -> float:
    """Return simulated mean systolic BP change (mmHg) over 30 days."""
    spec = CohortSpec(
        size=n_patients,
        diseases=[DiseaseSpec("hypertension", prevalence=1.0,
                              severity_weights={"mild": 2, "moderate": 3})],
        base_generator=DistributionPatientGenerator(seed=seed),
    )
    cohort = CohortGenerator(spec, seed=seed).generate()

    sim = DietSimulator(adherence=1.0)
    high = standard_diet()
    high.sodium_mg_per_day = 3300
    low = dash_diet()
    low.sodium_mg_per_day = 1500

    diffs = []
    for patient in cohort:
        high_result = sim.run(patient.clone(), high, duration_weeks=4)
        low_result = sim.run(patient.clone(), low, duration_weeks=4)
        baseline = high_result.timeline[0].biomarkers.get("systolic_bp_mmhg", 0)
        sbp_high = high_result.timeline[-1].biomarkers.get("systolic_bp_mmhg", baseline)
        sbp_low = low_result.timeline[-1].biomarkers.get("systolic_bp_mmhg", baseline)
        diffs.append(sbp_low - sbp_high)
    return float(np.mean(diffs))


def validate(n_patients: int = 200, seed: int = 42) -> ValidationReport:
    effect = simulate(n_patients=n_patients, seed=seed)
    return ValidationReport(
        target=DASH_SODIUM_TARGET,
        simulated_effect=effect,
        n_simulated=n_patients,
    )
