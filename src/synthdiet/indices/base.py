"""Common protocol and dataclasses for diet quality indices."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Dict, List, Optional, Protocol, runtime_checkable

if TYPE_CHECKING:
    from synthdiet.diets.base import DietPlan
    from synthdiet.patients.patient import Patient


@dataclass
class IndexComponent:
    """One scored component of a composite diet-quality index."""

    name: str
    raw_value: float
    score: float
    max_score: float
    note: str = ""


@dataclass
class IndexScore:
    """A composite diet-quality score with per-component breakdown."""

    index_name: str
    total: float
    max_total: float
    components: List[IndexComponent] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    @property
    def percent(self) -> float:
        return 100.0 * self.total / max(self.max_total, 1e-9)

    def as_dict(self) -> Dict[str, float]:
        return {c.name: c.score for c in self.components} | {
            "total": self.total,
            "max_total": self.max_total,
            "percent": self.percent,
        }

    def pretty(self) -> str:
        lines = [f"{self.index_name}: {self.total:.1f} / {self.max_total:.0f}"
                 f" ({self.percent:.0f}%)"]
        for c in self.components:
            lines.append(f"  {c.name:<28s} {c.score:5.1f} / {c.max_score:>4.0f}"
                         f"   raw = {c.raw_value:.2f}")
        if self.notes:
            lines.append("notes:")
            for n in self.notes:
                lines.append(f"  - {n}")
        return "\n".join(lines)


@runtime_checkable
class DietQualityIndex(Protocol):
    """Common interface implemented by every quality index."""

    name: str

    def score(
        self,
        diet: "DietPlan",
        patient: Optional["Patient"] = None,
    ) -> IndexScore: ...


def linear_score(
    value: float,
    target_low: float,
    target_high: float,
    max_points: float = 10.0,
) -> float:
    """Linear scoring rubric used by most quality indices.

    ``value`` <= ``target_low`` gives 0 points; ``value`` >= ``target_high``
    gives ``max_points``; values in between scale linearly. Use a *reversed*
    pair (``target_low > target_high``) for "less is better" rubrics.
    """
    reverse = target_low > target_high
    if reverse:
        target_low, target_high = target_high, target_low
        if value <= target_low:
            return max_points
        if value >= target_high:
            return 0.0
        return max_points * (target_high - value) / (target_high - target_low)
    if value <= target_low:
        return 0.0
    if value >= target_high:
        return max_points
    return max_points * (value - target_low) / (target_high - target_low)
