"""OSCE-style rubric scoring for a student's diet prescription."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional

from synthdiet.diets.base import DietPlan
from synthdiet.education.cases import CaseStudy
from synthdiet.simulation import DietSimulator


@dataclass
class OSCERubric:
    """A single scoring criterion."""

    code: str
    description: str
    points: float
    check: Callable[[DietPlan, CaseStudy], bool]


@dataclass
class OSCEScore:
    case_id: str
    total: float
    max_total: float
    awarded: List[str] = field(default_factory=list)
    missed: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def percent(self) -> float:
        return 100.0 * self.total / max(self.max_total, 1e-9)

    def pretty(self) -> str:
        lines = [
            f"OSCE score for case {self.case_id}: "
            f"{self.total:.1f} / {self.max_total:.0f} ({self.percent:.0f}%)"
        ]
        if self.awarded:
            lines.append("Awarded:")
            for a in self.awarded:
                lines.append(f"  + {a}")
        if self.missed:
            lines.append("Missed:")
            for m in self.missed:
                lines.append(f"  - {m}")
        if self.warnings:
            lines.append("Warnings:")
            for w in self.warnings:
                lines.append(f"  ! {w}")
        return "\n".join(lines)


@dataclass
class OSCEStation:
    """Score a student-submitted :class:`DietPlan` against an OSCE rubric."""

    case: CaseStudy
    rubric: List[OSCERubric] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.rubric:
            self.rubric = self._default_rubric()

    def grade(self, student_diet: DietPlan) -> OSCEScore:
        score = OSCEScore(case_id=self.case.case_id, total=0.0,
                          max_total=sum(r.points for r in self.rubric))
        for r in self.rubric:
            try:
                if r.check(student_diet, self.case):
                    score.total += r.points
                    score.awarded.append(f"({r.code}) {r.description}")
                else:
                    score.missed.append(f"({r.code}) {r.description}")
            except Exception as exc:  # noqa: BLE001
                score.warnings.append(f"({r.code}) skipped: {exc}")
        # Always layer simulator's safety warnings on top.
        sim = DietSimulator()
        score.warnings.extend(
            sim.check_diet_against_constraints(self.case.patient, student_diet)
        )
        return score

    # Default rubric: 5 criteria worth 4 points each ----------------------
    def _default_rubric(self) -> List[OSCERubric]:
        return [
            OSCERubric(
                "R1", "Total energy is appropriate (within +-300 kcal of needs)",
                4.0,
                lambda plan, case: _energy_appropriate(plan, case),
            ),
            OSCERubric(
                "R2", "No forbidden foods from disease constraints",
                4.0,
                lambda plan, case: not _hits_forbidden(plan, case),
            ),
            OSCERubric(
                "R3", "Protein adequate (>= 15% kcal)",
                4.0,
                lambda plan, case: plan.macronutrient_distribution().get("protein", 0) >= 0.15,
            ),
            OSCERubric(
                "R4", "Sodium within disease-specific cap",
                4.0,
                lambda plan, case: _sodium_within_cap(plan, case),
            ),
            OSCERubric(
                "R5", "Added sugar <= 10% kcal",
                4.0,
                lambda plan, case: (plan.added_sugar_pct or 0.0) <= 0.10,
            ),
        ]


def _energy_appropriate(plan: DietPlan, case: CaseStudy) -> bool:
    from synthdiet.simulation.metabolism import total_daily_energy_expenditure

    tdee = total_daily_energy_expenditure(case.patient)
    return abs(plan.daily_energy_kcal - tdee) <= 500


def _hits_forbidden(plan: DietPlan, case: CaseStudy) -> bool:
    from synthdiet.diseases.base import NutritionalConstraints

    merged = NutritionalConstraints()
    for d in case.patient.diseases:
        merged = merged.merge(d.nutritional_constraints(case.patient))
    return bool(merged.forbidden_foods & plan.forbidden_food_set())


def _sodium_within_cap(plan: DietPlan, case: CaseStudy) -> bool:
    from synthdiet.diseases.base import NutritionalConstraints

    merged = NutritionalConstraints()
    for d in case.patient.diseases:
        merged = merged.merge(d.nutritional_constraints(case.patient))
    cap = merged.sodium_mg_max
    sodium = plan.sodium_mg_per_day or 0
    if cap is None:
        return sodium <= 2300
    return sodium <= cap
