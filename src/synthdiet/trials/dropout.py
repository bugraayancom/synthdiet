"""Dropout-time generators for trial simulations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np

from synthdiet.utils.random_state import RandomState, as_random_state


class DropoutModel(Protocol):
    def sample_dropout_week(self, max_weeks: int) -> int: ...


@dataclass
class NoDropout:
    """No patient drops out."""

    def sample_dropout_week(self, max_weeks: int) -> int:
        return max_weeks + 1


@dataclass
class WeibullDropout:
    """Dropout time follows a Weibull distribution."""

    shape: float = 1.5
    scale_weeks: float = 30.0
    seed: RandomState = None
    rng: np.random.Generator = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.rng is None:
            self.rng = as_random_state(self.seed)

    def sample_dropout_week(self, max_weeks: int) -> int:
        value = float(self.rng.weibull(self.shape) * self.scale_weeks)
        return int(np.clip(np.ceil(value), 1, max_weeks + 1))


@dataclass
class LogNormalDropout:
    """Dropout time follows a log-normal distribution."""

    mean_log: float = 3.0
    sd_log: float = 0.6
    seed: RandomState = None
    rng: np.random.Generator = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.rng is None:
            self.rng = as_random_state(self.seed)

    def sample_dropout_week(self, max_weeks: int) -> int:
        value = float(self.rng.lognormal(self.mean_log, self.sd_log))
        return int(np.clip(np.ceil(value), 1, max_weeks + 1))
