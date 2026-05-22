"""ANCOVA-style baseline-adjusted treatment effect estimation.

A lightweight implementation that does *not* require statsmodels: we estimate
the treatment effect from a delta variable while regressing out the baseline
value using OLS on a stacked X = [1, baseline, treatment_indicator] design
matrix.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

import numpy as np
import pandas as pd
from scipy import stats


@dataclass
class ANCOVAResult:
    """Baseline-adjusted treatment effect."""

    treatment_effect: float
    se: float
    ci_95: tuple
    p_value: float
    n: int
    baseline_coef: float
    r_squared: float

    def pretty(self) -> str:
        lo, hi = self.ci_95
        return (
            f"ANCOVA: treatment effect = {self.treatment_effect:+.3f} "
            f"(95% CI {lo:+.3f}, {hi:+.3f}), p={self.p_value:.4f}, "
            f"n={self.n}, R²={self.r_squared:.3f}"
        )


def ancova_baseline_adjusted(
    df: pd.DataFrame,
    *,
    outcome: str,
    baseline: str,
    treatment: str,
    treatment_levels: Optional[Sequence] = None,
) -> ANCOVAResult:
    """Estimate a baseline-adjusted two-arm treatment effect.

    Parameters
    ----------
    df:
        Tidy DataFrame with the three columns named below.
    outcome:
        Name of the final-value or delta-value outcome column.
    baseline:
        Name of the baseline value column (used as a covariate).
    treatment:
        Name of the treatment indicator column. Must take exactly two values;
        the *second* unique level (by ``treatment_levels`` ordering, or
        natural sort) is treated as the active arm.
    """
    df = df.dropna(subset=[outcome, baseline, treatment]).copy()
    if treatment_levels is None:
        levels = sorted(df[treatment].unique())
    else:
        levels = list(treatment_levels)
    if len(levels) != 2:
        raise ValueError("treatment column must have exactly two levels")
    df["_t"] = (df[treatment] == levels[1]).astype(float)
    X = np.column_stack(
        [np.ones(len(df)), df[baseline].to_numpy(float), df["_t"].to_numpy()]
    )
    y = df[outcome].to_numpy(float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    residuals = y - X @ beta
    n, p = X.shape
    dof = n - p
    if dof <= 0:
        raise ValueError("not enough observations for ANCOVA")
    sigma2 = float(np.sum(residuals ** 2) / dof)
    cov = sigma2 * np.linalg.inv(X.T @ X)
    se_treat = float(np.sqrt(cov[2, 2]))
    t_stat = beta[2] / se_treat
    p_value = 2 * (1 - stats.t.cdf(abs(t_stat), df=dof))
    ci = (beta[2] - 1.96 * se_treat, beta[2] + 1.96 * se_treat)
    ss_total = float(np.sum((y - y.mean()) ** 2))
    ss_res = float(np.sum(residuals ** 2))
    r2 = 1 - ss_res / max(ss_total, 1e-12)
    return ANCOVAResult(
        treatment_effect=float(beta[2]),
        se=se_treat,
        ci_95=ci,
        p_value=float(p_value),
        n=int(n),
        baseline_coef=float(beta[1]),
        r_squared=float(r2),
    )
