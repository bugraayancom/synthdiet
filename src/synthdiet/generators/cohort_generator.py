"""Cohort generator that injects disease prevalences and demographics.

A :class:`CohortGenerator` wraps any base
:class:`~synthdiet.generators.base.PatientGenerator` and, for each sampled
patient, draws diseases according to user-specified prevalences. This is the
recommended high-level entry point for testing a diet across a virtual cohort.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

from synthdiet.diseases.base import Disease
from synthdiet.diseases.registry import get_disease
from synthdiet.generators.base import PatientGenerator
from synthdiet.generators.distribution_generator import DistributionPatientGenerator
from synthdiet.patients.patient import Patient


@dataclass
class DiseaseSpec:
    """How frequently and with which arguments to attach a disease."""

    name: str
    prevalence: float
    severity_weights: Optional[Mapping[str, float]] = None
    fixed_kwargs: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0.0 <= self.prevalence <= 1.0:
            raise ValueError("prevalence must be in [0, 1]")


@dataclass
class CohortSpec:
    """Describes a virtual cohort.

    Parameters
    ----------
    size:
        Default cohort size when calling ``generate()`` without arguments.
    diseases:
        Disease prevalence specifications applied independently.
    base_generator:
        The underlying generator used for demographics/anthropometrics. Defaults
        to :class:`DistributionPatientGenerator`.
    """

    size: int = 100
    diseases: List[DiseaseSpec] = field(default_factory=list)
    base_generator: Optional[PatientGenerator] = None


class CohortGenerator(PatientGenerator):
    """Generate a cohort of synthetic patients with realistic disease mix."""

    def __init__(self, spec: CohortSpec, seed=None) -> None:
        super().__init__(seed=seed)
        self.spec = spec
        self.base = spec.base_generator or DistributionPatientGenerator(seed=seed)

    def sample(self) -> Patient:
        patient = self.base.sample()
        for disease_spec in self.spec.diseases:
            if self.rng.random() < disease_spec.prevalence:
                cls = get_disease(disease_spec.name)
                kwargs = dict(disease_spec.fixed_kwargs)
                if disease_spec.severity_weights and "severity" not in kwargs:
                    severities = list(disease_spec.severity_weights.keys())
                    weights = list(disease_spec.severity_weights.values())
                    total = sum(weights)
                    if total <= 0:
                        raise ValueError("severity_weights must sum to > 0")
                    probs = [w / total for w in weights]
                    kwargs["severity"] = str(self.rng.choice(severities, p=probs))
                disease: Disease = cls(**kwargs)
                patient.add_disease(disease)
        return patient

    def generate(self, size: Optional[int] = None) -> List[Patient]:
        n = size if size is not None else self.spec.size
        return self.sample_many(n)
