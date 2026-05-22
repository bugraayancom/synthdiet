"""Tests for the statistics utilities."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from synthdiet.stats import (
    ancova_baseline_adjusted,
    bootstrap_ci,
    fdr_bh,
    holm_bonferroni,
    permutation_test,
    sample_size_binary,
    sample_size_continuous,
)


def test_continuous_sample_size_known_value() -> None:
    # Cohen's d = 0.5, alpha=0.05, power=0.80 -> n ~ 64 per arm
    n = sample_size_continuous(effect_size=0.5, sd=1.0, alpha=0.05, power=0.80)
    assert 60 <= n <= 68


def test_binary_sample_size_reasonable() -> None:
    # p1=0.20, p2=0.30 -> ~292/arm
    n = sample_size_binary(p1=0.20, p2=0.30, alpha=0.05, power=0.80)
    assert 280 <= n <= 310


def test_bootstrap_ci_covers_mean() -> None:
    rng = np.random.default_rng(0)
    sample = rng.normal(0, 1, 200)
    lo, hi = bootstrap_ci(sample, statistic=np.mean, n_resamples=500, seed=1)
    assert lo < 0 < hi


def test_permutation_test_detects_difference() -> None:
    rng = np.random.default_rng(0)
    a = rng.normal(0, 1, 100)
    b = rng.normal(0.6, 1, 100)
    result = permutation_test(a, b, n_resamples=1000, seed=1)
    assert result["p_value"] < 0.05


def test_fdr_bh_monotone_in_p() -> None:
    pvals = np.array([0.01, 0.02, 0.04, 0.10, 0.50])
    adj = fdr_bh(pvals)
    assert all(adj[i] <= adj[i + 1] for i in range(len(adj) - 1))


def test_holm_bonferroni_no_smaller_than_input() -> None:
    pvals = np.array([0.01, 0.02, 0.04, 0.10])
    adj = holm_bonferroni(pvals)
    assert (adj >= pvals).all()


def test_ancova_recovers_treatment_effect() -> None:
    rng = np.random.default_rng(42)
    n = 300
    baseline = rng.normal(100, 15, n)
    treatment = rng.binomial(1, 0.5, n)
    delta = -0.4 * baseline + 5 * treatment + rng.normal(0, 5, n)
    df = pd.DataFrame({"baseline": baseline, "treatment": treatment, "delta": delta})
    result = ancova_baseline_adjusted(
        df, outcome="delta", baseline="baseline", treatment="treatment"
    )
    assert abs(result.treatment_effect - 5.0) < 1.5
    assert result.p_value < 0.01
