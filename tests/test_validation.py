"""Validation regression tests against published RCT outcomes.

These tests are slow (each runs hundreds of full-year simulations) so they
are marked ``slow`` and excluded from the default ``pytest`` run. CI runs
them in a separate job. To execute locally:

    pytest -m slow tests/test_validation.py -v
"""

from __future__ import annotations

import pytest

from synthdiet.validation import (
    validate_dash_sodium,
    validate_direct,
    validate_dpp,
    validate_look_ahead,
    validate_predimed,
)


@pytest.mark.slow
def test_dash_sodium_within_tolerance() -> None:
    report = validate_dash_sodium(n_patients=120, seed=42)
    print("\n" + report.pretty())
    assert abs(report.simulated_effect) < 25.0, "implausible BP change"
    assert report.simulated_effect < 0, "expected SBP to drop on low-sodium DASH"


@pytest.mark.slow
def test_predimed_ldl_direction() -> None:
    report = validate_predimed(n_patients=120, seed=42)
    print("\n" + report.pretty())
    assert report.simulated_effect <= 0, "expected LDL to drop on Mediterranean diet"


@pytest.mark.slow
def test_direct_weight_loss() -> None:
    report = validate_direct(n_patients=60, seed=42)
    print("\n" + report.pretty())
    assert report.simulated_effect < -2.0, "VLCD should produce >2 kg net loss"


@pytest.mark.slow
def test_look_ahead_weight_loss() -> None:
    report = validate_look_ahead(n_patients=80, seed=42)
    print("\n" + report.pretty())
    assert report.simulated_effect < -1.5


@pytest.mark.slow
def test_dpp_weight_loss() -> None:
    report = validate_dpp(n_patients=80, seed=42)
    print("\n" + report.pretty())
    assert report.simulated_effect < -1.0


def test_validation_module_exports() -> None:
    from synthdiet.validation import ALL_TARGETS
    assert len(ALL_TARGETS) == 5
    assert all(t.expected_effect != 0.0 for t in ALL_TARGETS)
