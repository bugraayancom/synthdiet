"""Base interface for synthetic patient generators."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

import numpy as np

from synthdiet.patients.patient import Patient
from synthdiet.utils.random_state import RandomState, as_random_state


class PatientGenerator(ABC):
    """All generators implement :meth:`sample` for a single patient.

    :meth:`sample_many` defaults to repeated calls of :meth:`sample`; subclasses
    may override for efficiency or to produce correlated batches.
    """

    def __init__(self, seed: RandomState = None) -> None:
        self.rng: np.random.Generator = as_random_state(seed)

    @abstractmethod
    def sample(self) -> Patient:
        ...

    def sample_many(self, n: int) -> List[Patient]:
        if n <= 0:
            raise ValueError("n must be > 0")
        return [self.sample() for _ in range(n)]
