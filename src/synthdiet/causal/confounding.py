"""Synthetic confounding and adjustment demonstrations.

This module lets you take a synthdiet cohort, induce *observed* confounding
(e.g. healthier patients are more likely to receive the Mediterranean diet),
and then show how the naive comparison vs. the adjusted (IPTW / g-computation)
estimate diverge.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Sequence, Tuple

import numpy as np

from synthdiet.causal.counterfactual import counterfactual_run
from synthdiet.diets.base import DietPlan
from synthdiet.patients.patient import Patient


@dataclass
class ConfoundingExperiment:
    """Simulate confounded observational assignment + adjustment.

    Each patient receives treatment with probability ``propensity(patient)``.
    Two estimators are then computed:

    * naive: mean(treated outcome) - mean(control outcome)
    * IPTW:  weighted mean using inverse propensities
    * g-formula: average over counterfactual potential outcomes

    Because synthdiet knows the *true* counterfactual for every patient (via
    :func:`counterfactual_run`), we also report the ground-truth ATE for
    comparison.
    """

    treatment_diet: DietPlan
    control_diet: DietPlan
    propensity: Callable[[Patient], float]
    duration_weeks: int = 12

    def run(
        self,
        cohort: Sequence[Patient],
        outcome: str = "weight_kg",
        seed: int = 0,
    ) -> Dict[str, float]:
        rng = np.random.default_rng(seed)
        pairs = [
            counterfactual_run(p, self.treatment_diet, self.control_diet,
                               duration_weeks=self.duration_weeks)
            for p in cohort
        ]
        true_ate = float(np.mean([pair.individual_effect(outcome) for pair in pairs]))

        propensities = np.array([self.propensity(p) for p in cohort])
        propensities = np.clip(propensities, 0.05, 0.95)
        treated = rng.binomial(1, propensities)

        outcomes_t = np.array([
            (pair.treatment.timeline[-1].weight_kg
             if outcome == "weight_kg"
             else pair.treatment.timeline[-1].biomarkers.get(outcome, 0.0))
            for pair in pairs
        ])
        outcomes_c = np.array([
            (pair.control.timeline[-1].weight_kg
             if outcome == "weight_kg"
             else pair.control.timeline[-1].biomarkers.get(outcome, 0.0))
            for pair in pairs
        ])
        observed = np.where(treated == 1, outcomes_t, outcomes_c)

        if treated.sum() == 0 or (1 - treated).sum() == 0:
            return {
                "true_ate": true_ate,
                "naive": float("nan"),
                "iptw": float("nan"),
                "g_formula": true_ate,
            }

        naive = float(observed[treated == 1].mean() - observed[treated == 0].mean())

        weights = np.where(treated == 1, 1.0 / propensities, 1.0 / (1.0 - propensities))
        iptw_t = (observed * treated * weights).sum() / (treated * weights).sum()
        iptw_c = (observed * (1 - treated) * weights).sum() / ((1 - treated) * weights).sum()
        iptw = float(iptw_t - iptw_c)

        # g-formula: average potential outcomes (we know both for every patient).
        g_formula = float(outcomes_t.mean() - outcomes_c.mean())

        return {
            "true_ate": true_ate,
            "naive": naive,
            "iptw": iptw,
            "g_formula": g_formula,
            "n_treated": int(treated.sum()),
            "n_control": int((1 - treated).sum()),
        }
