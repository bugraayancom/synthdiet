"""Measurement error and missing-data injection.

Real clinical datasets always have noise: lab assays have a known coefficient
of variation (CV%), self-reported dietary intake is biased downward by ~10-30%,
and any longitudinal study has missing observations under one of three patterns
(MCAR, MAR, MNAR). These helpers let you inject realistic imperfection into
synthetic cohorts so that downstream statistics behave more like real-world data.
"""

from synthdiet.noise.measurement_error import (
    LAB_CV_PERCENT,
    add_lab_measurement_error,
    add_self_report_bias,
)
from synthdiet.noise.missing_data import (
    MissingPattern,
    inject_mar_missing,
    inject_mcar_missing,
    inject_mnar_missing,
)

__all__ = [
    "LAB_CV_PERCENT",
    "MissingPattern",
    "add_lab_measurement_error",
    "add_self_report_bias",
    "inject_mar_missing",
    "inject_mcar_missing",
    "inject_mnar_missing",
]
