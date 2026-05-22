"""Sample-size estimation for two-arm RCTs."""

from __future__ import annotations

from math import ceil

from scipy import stats


def sample_size_continuous(
    *,
    effect_size: float,
    sd: float = 1.0,
    alpha: float = 0.05,
    power: float = 0.80,
    two_sided: bool = True,
    ratio: float = 1.0,
) -> int:
    """Per-arm sample size for a two-arm continuous outcome (Cohen's d).

    Parameters
    ----------
    effect_size:
        Mean difference between arms in the original units (NOT a
        standardised effect; pair with ``sd``).
    sd:
        Common standard deviation.
    alpha:
        Two-sided type-I error rate.
    power:
        Desired power = 1 - beta.
    ratio:
        Allocation ratio (arm B / arm A). Default 1 = balanced.
    """
    z_alpha = stats.norm.ppf(1 - alpha / (2 if two_sided else 1))
    z_beta = stats.norm.ppf(power)
    d = effect_size / sd
    if d == 0:
        raise ValueError("effect_size cannot be zero")
    n_per_arm = ((z_alpha + z_beta) ** 2 * (1 + 1 / ratio)) / d ** 2
    return int(ceil(n_per_arm))


def sample_size_binary(
    *,
    p1: float,
    p2: float,
    alpha: float = 0.05,
    power: float = 0.80,
    two_sided: bool = True,
) -> int:
    """Per-arm sample size for a two-proportion z test (Fleiss approximation)."""
    if not (0 < p1 < 1 and 0 < p2 < 1):
        raise ValueError("p1 and p2 must be in (0, 1)")
    z_alpha = stats.norm.ppf(1 - alpha / (2 if two_sided else 1))
    z_beta = stats.norm.ppf(power)
    p_bar = (p1 + p2) / 2
    q_bar = 1 - p_bar
    numerator = (
        z_alpha * (2 * p_bar * q_bar) ** 0.5
        + z_beta * (p1 * (1 - p1) + p2 * (1 - p2)) ** 0.5
    ) ** 2
    n_per_arm = numerator / (p1 - p2) ** 2
    return int(ceil(n_per_arm))
