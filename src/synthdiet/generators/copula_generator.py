"""Gaussian copula based generator for correlated biomarkers.

This is a thin wrapper around :class:`DistributionPatientGenerator` that injects
a small Gaussian copula across selected biomarkers so that values move together
(e.g. higher BMI implies higher HOMA-IR, higher triglycerides, lower HDL).
"""

from __future__ import annotations

from typing import List, Mapping, Optional, Sequence

import numpy as np
from scipy.stats import norm

from synthdiet.generators.distribution_generator import DistributionPatientGenerator
from synthdiet.patients.biomarkers import ADULT_REFERENCE_RANGES, Biomarkers
from synthdiet.patients.patient import Patient


# Default correlation structure between four common biomarkers and BMI.
# Order: bmi, hba1c_pct, triglycerides_mg_dl, hdl_mg_dl, systolic_bp_mmhg
_DEFAULT_FEATURES: List[str] = [
    "bmi",
    "hba1c_pct",
    "triglycerides_mg_dl",
    "hdl_mg_dl",
    "systolic_bp_mmhg",
]

_DEFAULT_CORR = np.array(
    [
        [1.00, 0.45, 0.55, -0.40, 0.35],
        [0.45, 1.00, 0.50, -0.35, 0.30],
        [0.55, 0.50, 1.00, -0.45, 0.25],
        [-0.40, -0.35, -0.45, 1.00, -0.20],
        [0.35, 0.30, 0.25, -0.20, 1.00],
    ]
)


class CopulaPatientGenerator(DistributionPatientGenerator):
    """Sample patients whose listed biomarkers exhibit user-defined correlations."""

    def __init__(
        self,
        features: Optional[Sequence[str]] = None,
        correlation_matrix: Optional[np.ndarray] = None,
        marginal_distributions: Optional[Mapping[str, tuple]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.features = list(features or _DEFAULT_FEATURES)
        if correlation_matrix is None:
            correlation_matrix = _DEFAULT_CORR
        corr = np.asarray(correlation_matrix, dtype=float)
        if corr.shape != (len(self.features), len(self.features)):
            raise ValueError(
                f"correlation_matrix shape must be {(len(self.features),) * 2}"
            )
        self.correlation_matrix = corr
        self.cholesky = np.linalg.cholesky(corr)
        self.marginal_distributions = dict(marginal_distributions or {})

    def sample(self) -> Patient:
        patient = super().sample()
        u = self._sample_uniform_marginals(patient)
        for name, percentile in zip(self.features, u):
            value = self._inverse_marginal(name, percentile, patient)
            if name == "bmi":
                # Rescale weight to match the sampled BMI.
                patient.anthropometrics.weight_kg = (
                    value * (patient.anthropometrics.height_m ** 2)
                )
            else:
                patient.biomarkers.set(name, value)
        return patient

    def _sample_uniform_marginals(self, patient: Patient) -> np.ndarray:
        z = self.rng.standard_normal(len(self.features))
        correlated = self.cholesky @ z
        return norm.cdf(correlated)

    def _inverse_marginal(self, name: str, percentile: float, patient: Patient) -> float:
        # Allow user-defined (low, high) or (mean, sd) marginal overrides.
        if name in self.marginal_distributions:
            spec = self.marginal_distributions[name]
            if len(spec) == 2:
                low, high = spec
                return float(low + (high - low) * percentile)
        if name == "bmi":
            return float(np.clip(norm.ppf(percentile, loc=27.5, scale=5.5), 15.0, 55.0))
        ref = ADULT_REFERENCE_RANGES.get(name)
        if ref is None:
            current = patient.biomarkers.get(name) or 0.0
            return float(current + norm.ppf(percentile) * 0.1 * max(current, 1.0))
        low, high = ref
        lo = low if low is not None else 0.0
        hi = high if high is not None else lo * 1.5 + 1.0
        mid = (lo + hi) / 2.0
        spread = (hi - lo) / 3.0 if hi > lo else max(lo * 0.1, 0.5)
        return float(np.clip(norm.ppf(percentile, loc=mid, scale=spread),
                             lo * 0.3, hi * 1.8))
