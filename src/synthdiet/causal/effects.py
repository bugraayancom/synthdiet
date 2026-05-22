"""Average and conditional treatment effect estimators."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence

import numpy as np

from synthdiet.behavior.adherence import AdherenceModel
from synthdiet.causal.counterfactual import counterfactual_run
from synthdiet.diets.base import DietPlan
from synthdiet.patients.patient import Patient


@dataclass
class ATEResult:
    outcome: str
    n: int
    ate: float
    se: float
    ci_95: tuple
    individual_effects: List[float]

    def pretty(self) -> str:
        lo, hi = self.ci_95
        return (
            f"ATE on '{self.outcome}': {self.ate:+.3f} (95% CI {lo:+.3f}, {hi:+.3f}), n={self.n}"
        )


@dataclass
class ATEEstimator:
    """Estimate the average treatment effect by running counterfactuals."""

    treatment_diet: DietPlan
    control_diet: DietPlan
    duration_weeks: int = 12
    adherence: Any = 1.0
    engine: str = "simple"

    def estimate(
        self,
        cohort: Sequence[Patient],
        outcome: str = "weight_kg",
    ) -> ATEResult:
        if len(cohort) == 0:
            raise ValueError("cohort must not be empty")
        effects = []
        for patient in cohort:
            pair = counterfactual_run(
                patient,
                self.treatment_diet,
                self.control_diet,
                duration_weeks=self.duration_weeks,
                adherence=self.adherence,
                engine=self.engine,
            )
            effects.append(pair.individual_effect(outcome=outcome))
        effects_arr = np.asarray(effects)
        ate = float(np.mean(effects_arr))
        se = float(np.std(effects_arr, ddof=1) / np.sqrt(len(effects_arr)))
        ci = (ate - 1.96 * se, ate + 1.96 * se)
        return ATEResult(
            outcome=outcome,
            n=len(effects_arr),
            ate=ate,
            se=se,
            ci_95=ci,
            individual_effects=effects,
        )


def cate_by_subgroup(
    cohort: Sequence[Patient],
    treatment_diet: DietPlan,
    control_diet: DietPlan,
    subgroup_fn: Callable[[Patient], Any],
    outcome: str = "weight_kg",
    duration_weeks: int = 12,
    adherence: Any = 1.0,
    engine: str = "simple",
) -> Dict[Any, ATEResult]:
    """Stratify the cohort by ``subgroup_fn`` and return per-stratum ATEs."""
    strata: Dict[Any, List[Patient]] = {}
    for p in cohort:
        key = subgroup_fn(p)
        strata.setdefault(key, []).append(p)
    out: Dict[Any, ATEResult] = {}
    for key, patients in strata.items():
        if not patients:
            continue
        est = ATEEstimator(
            treatment_diet=treatment_diet,
            control_diet=control_diet,
            duration_weeks=duration_weeks,
            adherence=adherence,
            engine=engine,
        )
        out[key] = est.estimate(patients, outcome=outcome)
    return out
