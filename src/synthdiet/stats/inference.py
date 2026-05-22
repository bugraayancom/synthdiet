"""Bootstrap, permutation, and multiple-comparison helpers."""

from __future__ import annotations

from typing import Callable, Sequence

import numpy as np

from synthdiet.utils.random_state import RandomState, as_random_state


def bootstrap_ci(
    values: Sequence[float],
    *,
    statistic: Callable[[np.ndarray], float] = np.mean,
    n_resamples: int = 2000,
    confidence: float = 0.95,
    seed: RandomState = None,
) -> tuple:
    """Percentile bootstrap confidence interval."""
    rng = as_random_state(seed)
    arr = np.asarray(values, dtype=float)
    if len(arr) == 0:
        raise ValueError("values must be non-empty")
    estimates = np.empty(n_resamples)
    for i in range(n_resamples):
        sample = rng.choice(arr, size=len(arr), replace=True)
        estimates[i] = statistic(sample)
    alpha = (1 - confidence) / 2
    lo = float(np.percentile(estimates, 100 * alpha))
    hi = float(np.percentile(estimates, 100 * (1 - alpha)))
    return lo, hi


def permutation_test(
    a: Sequence[float],
    b: Sequence[float],
    *,
    statistic: Callable[[np.ndarray, np.ndarray], float] = lambda x, y: float(
        np.mean(x) - np.mean(y)
    ),
    n_resamples: int = 5000,
    two_sided: bool = True,
    seed: RandomState = None,
) -> dict:
    """Permutation test for the equality of two samples."""
    rng = as_random_state(seed)
    a_arr = np.asarray(a, dtype=float)
    b_arr = np.asarray(b, dtype=float)
    observed = statistic(a_arr, b_arr)
    combined = np.concatenate([a_arr, b_arr])
    n_a = len(a_arr)

    null = np.empty(n_resamples)
    for i in range(n_resamples):
        rng.shuffle(combined)
        null[i] = statistic(combined[:n_a], combined[n_a:])

    if two_sided:
        p = float((np.abs(null) >= abs(observed)).mean())
    else:
        p = float((null >= observed).mean())
    return {
        "observed": float(observed),
        "p_value": p,
        "null_mean": float(np.mean(null)),
        "null_sd": float(np.std(null, ddof=1)),
    }


def fdr_bh(p_values: Sequence[float], alpha: float = 0.05) -> np.ndarray:
    """Benjamini-Hochberg adjusted p-values (Step-up)."""
    pvals = np.asarray(p_values, dtype=float)
    n = len(pvals)
    order = np.argsort(pvals)
    ranked = pvals[order]
    adjusted = ranked * n / (np.arange(n) + 1)
    # Enforce monotonicity from the largest rank down.
    adjusted_min = np.minimum.accumulate(adjusted[::-1])[::-1]
    out = np.empty(n)
    out[order] = np.clip(adjusted_min, 0, 1)
    return out


def holm_bonferroni(p_values: Sequence[float], alpha: float = 0.05) -> np.ndarray:
    """Holm-Bonferroni adjusted p-values."""
    pvals = np.asarray(p_values, dtype=float)
    n = len(pvals)
    order = np.argsort(pvals)
    ranked = pvals[order]
    factors = np.arange(n, 0, -1)
    # Holm step-down: enforce monotonicity from smallest to largest.
    adjusted = np.maximum.accumulate(ranked * factors)
    out = np.empty(n)
    out[order] = np.clip(adjusted, 0, 1)
    return out
