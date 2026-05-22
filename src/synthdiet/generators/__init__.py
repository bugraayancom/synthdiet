"""Synthetic patient generators.

Each generator is callable and returns either a single :class:`Patient` or a
cohort of them. Generators differ in the assumptions they make about the joint
distribution of demographics, anthropometrics, biomarkers, and diseases.
"""

from synthdiet.generators.base import PatientGenerator
from synthdiet.generators.cohort_generator import (
    CohortGenerator,
    CohortSpec,
    DiseaseSpec,
)
from synthdiet.generators.copula_generator import CopulaPatientGenerator
from synthdiet.generators.distribution_generator import DistributionPatientGenerator
from synthdiet.generators.markov_generator import (
    MarkovProgressionGenerator,
    ProgressionState,
)
from synthdiet.generators.random_generator import RandomPatientGenerator

__all__ = [
    "CohortGenerator",
    "CohortSpec",
    "CopulaPatientGenerator",
    "DiseaseSpec",
    "DistributionPatientGenerator",
    "MarkovProgressionGenerator",
    "PatientGenerator",
    "ProgressionState",
    "RandomPatientGenerator",
]
