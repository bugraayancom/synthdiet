"""Randomised controlled trial (RCT) simulation engine.

Build a virtual trial from a synthetic cohort, randomise patients to one or
more diet arms, simulate adherence and dropout, and analyse the results with
intention-to-treat (ITT), per-protocol (PP), or as-treated (AT) strategies.

Quick start
-----------

>>> from synthdiet import CohortGenerator, CohortSpec, DiseaseSpec
>>> from synthdiet.trials import ParallelTrial
>>> from synthdiet.diets import mediterranean_diet, standard_diet
>>>
>>> cohort = CohortGenerator(
...     CohortSpec(size=100, diseases=[DiseaseSpec("type_2_diabetes", 0.4)]),
...     seed=1,
... ).generate()
>>> trial = ParallelTrial(
...     cohort=cohort,
...     arms={"control": standard_diet(), "intervention": mediterranean_diet()},
...     duration_weeks=12,
...     primary_outcome="hba1c_pct",
... )
>>> result = trial.run(seed=42)  # doctest: +SKIP
>>> print(result.intention_to_treat())  # doctest: +SKIP
"""

from synthdiet.trials.analysis import (
    AnalysisResult,
    TrialResult,
    as_treated,
    intention_to_treat,
    per_protocol,
)
from synthdiet.trials.design import CrossoverTrial, FactorialTrial, ParallelTrial
from synthdiet.trials.dropout import (
    LogNormalDropout,
    NoDropout,
    WeibullDropout,
)
from synthdiet.trials.randomization import (
    block_randomization,
    minimization,
    simple_randomization,
    stratified_randomization,
)

__all__ = [
    "AnalysisResult",
    "CrossoverTrial",
    "FactorialTrial",
    "LogNormalDropout",
    "NoDropout",
    "ParallelTrial",
    "TrialResult",
    "WeibullDropout",
    "as_treated",
    "block_randomization",
    "intention_to_treat",
    "minimization",
    "per_protocol",
    "simple_randomization",
    "stratified_randomization",
]
