"""Lab CV% and self-report dietary bias."""

from __future__ import annotations

from typing import Iterable, Mapping, Optional, Sequence

import numpy as np

from synthdiet.patients.patient import Patient
from synthdiet.utils.random_state import RandomState, as_random_state

# Approximate analytical CV% for common clinical assays.
LAB_CV_PERCENT: Mapping[str, float] = {
    "hba1c_pct": 3.0,
    "fasting_glucose_mg_dl": 2.5,
    "fasting_insulin_uIU_ml": 6.0,
    "total_cholesterol_mg_dl": 3.5,
    "ldl_mg_dl": 6.0,
    "hdl_mg_dl": 4.0,
    "triglycerides_mg_dl": 5.0,
    "creatinine_mg_dl": 3.5,
    "egfr_ml_min_1_73m2": 6.0,
    "potassium_mmol_l": 1.5,
    "sodium_mmol_l": 1.0,
    "alt_u_l": 7.0,
    "ast_u_l": 7.0,
    "vitamin_d_25oh_ng_ml": 10.0,
    "vitamin_b12_pg_ml": 7.0,
    "ferritin_ng_ml": 8.0,
    "crp_mg_l": 12.0,
    "systolic_bp_mmhg": 4.0,
    "diastolic_bp_mmhg": 5.0,
    "tsh_uIU_ml": 6.0,
    "uric_acid_mg_dl": 3.0,
}


def add_lab_measurement_error(
    patients: Sequence[Patient],
    biomarkers: Optional[Iterable[str]] = None,
    cv_overrides: Optional[Mapping[str, float]] = None,
    *,
    seed: RandomState = None,
    in_place: bool = True,
) -> None:
    """Add multiplicative Gaussian noise to each named biomarker.

    Each value becomes ``v * (1 + epsilon)`` where ``epsilon ~ N(0, CV%/100)``.
    The CV% defaults come from :data:`LAB_CV_PERCENT`; pass ``cv_overrides`` to
    customise for a particular assay or lab.
    """
    rng = as_random_state(seed)
    cv_table = {**LAB_CV_PERCENT, **(cv_overrides or {})}
    keys = list(biomarkers) if biomarkers is not None else None
    for p in patients:
        if not in_place:
            raise NotImplementedError("non-in-place mode not yet supported")
        for k in keys or list(p.biomarkers.values.keys()):
            cv = cv_table.get(k)
            if cv is None:
                continue
            current = p.biomarkers.get(k)
            if current is None:
                continue
            noise = rng.normal(0.0, cv / 100.0)
            p.biomarkers.set(k, max(0.0, current * (1.0 + noise)))


def add_self_report_bias(
    reported_intake_kcal: float,
    *,
    bmi: float,
    rng: Optional[np.random.Generator] = None,
    bias_mean: float = -0.18,
    bias_sd: float = 0.10,
    bmi_modifier: float = -0.01,
) -> float:
    """Apply a realistic under-reporting bias to a self-reported intake value.

    Higher BMI patients under-report more (~1% per BMI unit above 25). The
    returned value can be used to drive missing-data analyses or to test the
    robustness of a model against measurement bias.
    """
    rng = rng or np.random.default_rng()
    bias = bias_mean + bmi_modifier * max(0, bmi - 25) + rng.normal(0, bias_sd)
    return reported_intake_kcal * (1.0 + bias)
