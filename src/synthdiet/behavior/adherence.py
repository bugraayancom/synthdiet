"""Diet-adherence and dropout models.

Each model implements the :class:`AdherenceModel` protocol and returns, for a
given week, an *adherence fraction* in [0, 1] that the simulator multiplies
into the consumed energy / nutrient delta. A return value of 0 represents a
full drop-out for that week.

References
----------
- Hall KD, Sacks G, Chandramohan D, et al. (2011) describe how compensatory
  behavioural adaptation degrades adherence over time.
- Greaves CJ et al. (2011) review behaviour-change interventions, motivating
  the Weibull dropout pattern.
- Burke LE, Wang J, Sevick MA. (2011) report mean dietary self-monitoring
  adherence declining roughly linearly during 12 mo trials.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Protocol, runtime_checkable

import numpy as np

from synthdiet.patients.patient import Patient
from synthdiet.utils.random_state import RandomState, as_random_state


@runtime_checkable
class AdherenceModel(Protocol):
    """Returns an adherence fraction in [0, 1] for a given week and patient."""

    def adherence_for_week(self, week: int, patient: Patient) -> float: ...

    def reset(self) -> None: ...


@dataclass
class ConstantAdherence:
    """Time-invariant adherence (matches the legacy ``DietSimulator`` flag)."""

    value: float = 1.0

    def adherence_for_week(self, week: int, patient: Patient) -> float:
        return float(np.clip(self.value, 0.0, 1.0))

    def reset(self) -> None:
        return None


@dataclass
class DecayingAdherence:
    """Linear or exponential decay of adherence over time.

    Parameters
    ----------
    initial:
        Adherence at week 0.
    floor:
        Lower bound that the curve asymptotes to.
    mode:
        ``"linear"`` decays at ``rate`` per week; ``"exponential"`` decays as
        ``floor + (initial - floor) * exp(-rate * week)``.
    rate:
        Decay rate per week.
    """

    initial: float = 0.95
    floor: float = 0.40
    mode: str = "exponential"
    rate: float = 0.03

    def adherence_for_week(self, week: int, patient: Patient) -> float:
        if self.mode == "linear":
            value = self.initial - self.rate * week
        elif self.mode == "exponential":
            value = self.floor + (self.initial - self.floor) * np.exp(
                -self.rate * week
            )
        else:
            raise ValueError("mode must be 'linear' or 'exponential'")
        return float(np.clip(value, self.floor, 1.0))

    def reset(self) -> None:
        return None


@dataclass
class WeibullDropoutAdherence:
    """Patient drops out at a Weibull-distributed week.

    Until the dropout week, adherence equals :attr:`pre_dropout`; afterwards
    it equals :attr:`post_dropout` (default 0). This is the standard
    behavioural model used in RCT simulations.

    The Weibull dropout time is drawn once at construction (deterministic
    given a seed) so all subsequent ``adherence_for_week`` calls are pure.
    """

    shape: float = 1.5
    scale_weeks: float = 26.0
    pre_dropout: float = 0.85
    post_dropout: float = 0.0
    seed: RandomState = None
    _dropout_week: Optional[int] = field(default=None, init=False, repr=False)

    def __post_init__(self) -> None:
        if self.shape <= 0 or self.scale_weeks <= 0:
            raise ValueError("shape and scale must be > 0")
        rng = as_random_state(self.seed)
        sample = rng.weibull(self.shape) * self.scale_weeks
        self._dropout_week = int(np.ceil(sample))

    def adherence_for_week(self, week: int, patient: Patient) -> float:
        assert self._dropout_week is not None
        if week < self._dropout_week:
            return float(self.pre_dropout)
        return float(self.post_dropout)

    @property
    def dropout_week(self) -> int:
        assert self._dropout_week is not None
        return self._dropout_week

    def reset(self) -> None:
        rng = as_random_state(self.seed)
        sample = rng.weibull(self.shape) * self.scale_weeks
        self._dropout_week = int(np.ceil(sample))


@dataclass
class StochasticSkipAdherence:
    """Patient skips the prescription on a random fraction of days each week."""

    skip_probability: float = 0.20
    seed: RandomState = None
    _rng: np.random.Generator = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if not 0 <= self.skip_probability <= 1:
            raise ValueError("skip_probability must be in [0, 1]")
        self._rng = as_random_state(self.seed)

    def adherence_for_week(self, week: int, patient: Patient) -> float:
        skipped_days = self._rng.binomial(7, self.skip_probability)
        return float((7 - skipped_days) / 7.0)

    def reset(self) -> None:
        self._rng = as_random_state(self.seed)


@dataclass
class PerceivedBurdenAdherence:
    """Adherence falls with diet "burden" (deviation from baseline pattern).

    A simple proxy: the further the prescribed energy is from the patient's
    estimated maintenance intake, the more burdensome the diet feels and the
    sooner adherence decays. Patients with active eating disorders or
    documented "very_low" cooking skill experience an extra penalty.

    Returns adherence = ``max(floor, base * burden_factor * patient_factor)``.
    """

    base: float = 0.90
    floor: float = 0.30
    burden_kcal_threshold: int = 500
    burden_sensitivity: float = 0.15
    decay_rate: float = 0.015

    def adherence_for_week(self, week: int, patient: Patient) -> float:
        from synthdiet.simulation.metabolism import total_daily_energy_expenditure

        tdee = total_daily_energy_expenditure(patient)
        deficit = abs(getattr(patient, "_prescribed_kcal", tdee) - tdee)
        burden = max(0.0, deficit - self.burden_kcal_threshold) / 1000.0
        burden_factor = max(0.0, 1.0 - burden * self.burden_sensitivity)

        patient_factor = 1.0
        if patient.has_disease("binge_eating_disorder"):
            patient_factor *= 0.85
        if patient.has_disease("bulimia_nervosa"):
            patient_factor *= 0.80
        if patient.lifestyle.cooking_skill == "low":
            patient_factor *= 0.90

        time_factor = np.exp(-self.decay_rate * week)
        value = self.base * burden_factor * patient_factor * time_factor
        return float(np.clip(value, self.floor, 1.0))

    def reset(self) -> None:
        return None
