"""Validation suite: reproduce published RCT outcomes.

Each submodule defines:

* a published *expected* effect with its 95% CI from a peer-reviewed RCT;
* a function ``simulate()`` that runs synthdiet to estimate the same effect
  on a comparable synthetic cohort;
* a function ``validate()`` returning a :class:`ValidationReport` with the
  observed vs. expected values and a pass/fail flag against a tolerance band.

These tests are *not* claims that synthdiet reproduces real-world RCTs out of
the box. They are sanity checks that flag when an internal change pushes a
result far outside the published confidence interval — useful as regression
tests for clinical plausibility.
"""

from synthdiet.validation.base import ValidationReport, ValidationTarget
from synthdiet.validation.dash_sodium import (
    DASH_SODIUM_TARGET,
    simulate as simulate_dash_sodium,
    validate as validate_dash_sodium,
)
from synthdiet.validation.direct import (
    DIRECT_TARGET,
    simulate as simulate_direct,
    validate as validate_direct,
)
from synthdiet.validation.dpp import (
    DPP_TARGET,
    simulate as simulate_dpp,
    validate as validate_dpp,
)
from synthdiet.validation.look_ahead import (
    LOOK_AHEAD_TARGET,
    simulate as simulate_look_ahead,
    validate as validate_look_ahead,
)
from synthdiet.validation.predimed import (
    PREDIMED_TARGET,
    simulate as simulate_predimed,
    validate as validate_predimed,
)

ALL_TARGETS = [
    DASH_SODIUM_TARGET,
    PREDIMED_TARGET,
    DIRECT_TARGET,
    LOOK_AHEAD_TARGET,
    DPP_TARGET,
]

__all__ = [
    "ALL_TARGETS",
    "DASH_SODIUM_TARGET",
    "DIRECT_TARGET",
    "DPP_TARGET",
    "LOOK_AHEAD_TARGET",
    "PREDIMED_TARGET",
    "ValidationReport",
    "ValidationTarget",
    "simulate_dash_sodium",
    "simulate_direct",
    "simulate_dpp",
    "simulate_look_ahead",
    "simulate_predimed",
    "validate_dash_sodium",
    "validate_direct",
    "validate_dpp",
    "validate_look_ahead",
    "validate_predimed",
]
