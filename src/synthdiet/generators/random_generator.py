"""Simple uniform-random patient generator.

Useful for smoke tests and unit testing. Not intended for realistic cohorts.
"""

from __future__ import annotations

from typing import Optional, Sequence

from synthdiet.generators.base import PatientGenerator
from synthdiet.patients.anthropometrics import Anthropometrics
from synthdiet.patients.demographics import Demographics, Sex
from synthdiet.patients.lifestyle import ActivityLevel, Lifestyle
from synthdiet.patients.patient import Patient


class RandomPatientGenerator(PatientGenerator):
    """Generate patients by drawing each attribute from uniform ranges."""

    def __init__(
        self,
        age_range: tuple = (18, 80),
        height_cm_range: tuple = (150.0, 200.0),
        weight_kg_range: tuple = (45.0, 130.0),
        sexes: Sequence[Sex] = (Sex.FEMALE, Sex.MALE),
        activity_levels: Optional[Sequence[ActivityLevel]] = None,
        seed=None,
    ) -> None:
        super().__init__(seed=seed)
        self.age_range = age_range
        self.height_cm_range = height_cm_range
        self.weight_kg_range = weight_kg_range
        self.sexes = list(sexes)
        self.activity_levels = list(activity_levels or list(ActivityLevel))

    def sample(self) -> Patient:
        age = int(self.rng.integers(self.age_range[0], self.age_range[1] + 1))
        sex = Sex(self.rng.choice([s.value for s in self.sexes]))
        height = float(self.rng.uniform(*self.height_cm_range))
        weight = float(self.rng.uniform(*self.weight_kg_range))
        activity = ActivityLevel(self.rng.choice([a.value for a in self.activity_levels]))
        return Patient(
            demographics=Demographics(age=age, sex=sex),
            anthropometrics=Anthropometrics(height_cm=height, weight_kg=weight),
            lifestyle=Lifestyle(activity_level=activity),
        )
