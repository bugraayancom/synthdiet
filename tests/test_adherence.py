"""Tests for the behavioural adherence models."""

from __future__ import annotations

import numpy as np
import pytest

from synthdiet import (
    Anthropometrics,
    Demographics,
    DietSimulator,
    Lifestyle,
    Patient,
    Sex,
    standard_diet,
)
from synthdiet.behavior import (
    ConstantAdherence,
    DecayingAdherence,
    PerceivedBurdenAdherence,
    StochasticSkipAdherence,
    WeibullDropoutAdherence,
)


def _patient() -> Patient:
    return Patient(
        demographics=Demographics(age=45, sex=Sex.FEMALE),
        anthropometrics=Anthropometrics(height_cm=165, weight_kg=78),
        lifestyle=Lifestyle(),
    )


def test_constant_adherence_returns_same_value() -> None:
    m = ConstantAdherence(value=0.6)
    p = _patient()
    assert m.adherence_for_week(0, p) == 0.6
    assert m.adherence_for_week(52, p) == 0.6


def test_decaying_exponential_drops_over_time() -> None:
    m = DecayingAdherence(initial=0.9, floor=0.3, rate=0.05, mode="exponential")
    p = _patient()
    assert m.adherence_for_week(0, p) == pytest.approx(0.9)
    assert m.adherence_for_week(100, p) <= 0.45
    assert m.adherence_for_week(100, p) >= 0.30


def test_weibull_dropout_deterministic_with_seed() -> None:
    a = WeibullDropoutAdherence(shape=1.5, scale_weeks=20, seed=123)
    b = WeibullDropoutAdherence(shape=1.5, scale_weeks=20, seed=123)
    assert a.dropout_week == b.dropout_week
    p = _patient()
    pre = a.adherence_for_week(a.dropout_week - 1, p)
    post = a.adherence_for_week(a.dropout_week + 1, p)
    assert pre > post
    assert post == 0.0


def test_stochastic_skip_within_bounds() -> None:
    m = StochasticSkipAdherence(skip_probability=0.3, seed=0)
    p = _patient()
    values = [m.adherence_for_week(w, p) for w in range(50)]
    arr = np.array(values)
    assert arr.min() >= 0
    assert arr.max() <= 1
    # On average ~70% adherence
    assert 0.55 < arr.mean() < 0.85


def test_perceived_burden_penalises_extreme_deficits() -> None:
    m = PerceivedBurdenAdherence()
    p = _patient()
    setattr(p, "_prescribed_kcal", 2500)
    mild = m.adherence_for_week(4, p)
    setattr(p, "_prescribed_kcal", 800)
    severe = m.adherence_for_week(4, p)
    assert severe < mild


def test_simulator_accepts_adherence_model() -> None:
    p = _patient()
    sim = DietSimulator(
        adherence=WeibullDropoutAdherence(shape=1.5, scale_weeks=10, seed=42),
        sampling_weeks=2,
    )
    result = sim.run(p, standard_diet(daily_energy_kcal=1400), duration_weeks=24)
    adherences = [tp.adherence for tp in result.timeline]
    # Should see a drop from positive to zero
    assert any(a > 0 for a in adherences)
    assert any(a == 0 for a in adherences[1:])


def test_simulator_still_accepts_float_adherence() -> None:
    p = _patient()
    sim = DietSimulator(adherence=0.7)
    result = sim.run(p, standard_diet(daily_energy_kcal=1500), duration_weeks=8)
    assert all(tp.adherence == 0.7 for tp in result.timeline)
