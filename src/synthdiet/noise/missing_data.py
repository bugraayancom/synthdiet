"""Missing-data injection helpers (MCAR / MAR / MNAR)."""

from __future__ import annotations

from enum import Enum
from typing import Callable, Iterable, Optional

import numpy as np
import pandas as pd

from synthdiet.utils.random_state import RandomState, as_random_state


class MissingPattern(str, Enum):
    MCAR = "MCAR"  # missing completely at random
    MAR = "MAR"    # missing at random (depends on observed covariates)
    MNAR = "MNAR"  # missing not at random (depends on the value itself)


def inject_mcar_missing(
    df: pd.DataFrame,
    columns: Iterable[str],
    *,
    fraction: float = 0.10,
    seed: RandomState = None,
) -> pd.DataFrame:
    """Replace ``fraction`` of values in each column with NaN, independently."""
    rng = as_random_state(seed)
    df = df.copy()
    for col in columns:
        if col not in df.columns:
            continue
        mask = rng.random(len(df)) < fraction
        df.loc[mask, col] = np.nan
    return df


def inject_mar_missing(
    df: pd.DataFrame,
    target_columns: Iterable[str],
    *,
    depends_on: str,
    fraction: float = 0.10,
    seed: RandomState = None,
) -> pd.DataFrame:
    """MAR: probability of missingness depends on the values of an observed
    covariate ``depends_on`` (e.g. older patients miss follow-up labs)."""
    rng = as_random_state(seed)
    df = df.copy()
    if depends_on not in df.columns:
        raise KeyError(f"column '{depends_on}' missing from DataFrame")
    raw = df[depends_on].astype(float).to_numpy()
    if np.nanstd(raw) == 0:
        scale = np.zeros_like(raw)
    else:
        scale = (raw - np.nanmean(raw)) / np.nanstd(raw)
    # Sigmoid centred around the desired marginal ``fraction``.
    target_logit = np.log(fraction / (1 - fraction)) if 0 < fraction < 1 else 0.0
    probs = 1 / (1 + np.exp(-(target_logit + 0.5 * scale)))
    mask = rng.random(len(df)) < probs
    for col in target_columns:
        if col in df.columns:
            df.loc[mask, col] = np.nan
    return df


def inject_mnar_missing(
    df: pd.DataFrame,
    target_columns: Iterable[str],
    *,
    fraction: float = 0.10,
    high_value_bias: bool = True,
    seed: RandomState = None,
) -> pd.DataFrame:
    """MNAR: probability of missingness depends on the target value itself.

    If ``high_value_bias`` is True, patients with extreme high values are more
    likely to be missing (e.g. severe cases withdraw from a trial).
    """
    rng = as_random_state(seed)
    df = df.copy()
    for col in target_columns:
        if col not in df.columns:
            continue
        values = df[col].astype(float).to_numpy()
        if np.nanstd(values) == 0:
            scale = np.zeros_like(values)
        else:
            scale = (values - np.nanmean(values)) / np.nanstd(values)
        if not high_value_bias:
            scale = -scale
        probs = 1 / (1 + np.exp(-(np.log(fraction / (1 - fraction)) + 0.8 * scale)))
        mask = rng.random(len(df)) < probs
        df.loc[mask, col] = np.nan
    return df
