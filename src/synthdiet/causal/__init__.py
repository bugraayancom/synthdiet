"""Causal inference utilities for diet research.

Synthetic patients are uniquely suited to causal inference because the data
generating process (DGP) is fully known. This module provides:

* :func:`counterfactual_run` to evaluate the *same* patient under two diets;
* :class:`ATEEstimator` for Average Treatment Effects;
* :func:`cate_by_subgroup` to estimate Conditional ATE across strata;
* :class:`ConfoundingExperiment` to inject confounders and demonstrate
  IPTW / g-computation adjustment;
* :class:`DietDAG`, a thin wrapper around NetworkX for visualising assumed
  causal graphs between diet, biomarkers, and outcomes.
"""

from synthdiet.causal.confounding import ConfoundingExperiment
from synthdiet.causal.counterfactual import (
    CounterfactualPair,
    counterfactual_run,
)
from synthdiet.causal.dag import DietDAG
from synthdiet.causal.effects import (
    ATEEstimator,
    ATEResult,
    cate_by_subgroup,
)

__all__ = [
    "ATEEstimator",
    "ATEResult",
    "ConfoundingExperiment",
    "CounterfactualPair",
    "DietDAG",
    "cate_by_subgroup",
    "counterfactual_run",
]
