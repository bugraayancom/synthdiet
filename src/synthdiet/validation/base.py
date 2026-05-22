"""Shared validation primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple


@dataclass(frozen=True)
class ValidationTarget:
    """A peer-reviewed RCT result that synthdiet should approximately match."""

    name: str
    citation: str
    outcome: str
    expected_effect: float
    expected_ci_95: Tuple[float, float]
    tolerance: float = 0.5
    units: str = ""
    description: str = ""

    def pretty(self) -> str:
        lo, hi = self.expected_ci_95
        return (
            f"{self.name}: {self.outcome} = {self.expected_effect:+.2f} {self.units} "
            f"(95% CI {lo:+.2f}, {hi:+.2f}), tol ±{self.tolerance}\n"
            f"  citation: {self.citation}"
        )


@dataclass
class ValidationReport:
    """The outcome of a single validation run."""

    target: ValidationTarget
    simulated_effect: float
    simulated_se: Optional[float] = None
    n_simulated: int = 0
    details: dict = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return abs(self.simulated_effect - self.target.expected_effect) <= self.target.tolerance

    @property
    def within_ci(self) -> bool:
        lo, hi = self.target.expected_ci_95
        return lo <= self.simulated_effect <= hi

    def pretty(self) -> str:
        status = "PASS" if self.passed else "FAIL"
        return (
            f"[{status}] {self.target.name} ({self.n_simulated} patients): "
            f"simulated = {self.simulated_effect:+.2f} {self.target.units}, "
            f"expected = {self.target.expected_effect:+.2f} ±{self.target.tolerance}"
        )
