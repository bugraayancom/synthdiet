"""Markov-chain based disease-progression generator.

Patients start in an initial state (e.g. ``healthy`` or ``prediabetic``) and
transition each simulated year according to a user-supplied transition matrix.
Each terminal state can be associated with a disease class to be attached to
the resulting patient.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np

from synthdiet.diseases.registry import get_disease
from synthdiet.generators.base import PatientGenerator
from synthdiet.generators.distribution_generator import DistributionPatientGenerator
from synthdiet.patients.patient import Patient


@dataclass
class ProgressionState:
    """A node in the Markov disease-progression graph."""

    name: str
    transitions: Dict[str, float] = field(default_factory=dict)  # next_state -> probability
    disease_to_attach: Optional[str] = None  # disease registry name


class MarkovProgressionGenerator(PatientGenerator):
    """Sample patients whose disease state is the result of a Markov walk."""

    def __init__(
        self,
        states: List[ProgressionState],
        initial_state: str,
        years_to_simulate: int = 10,
        base_generator: Optional[PatientGenerator] = None,
        seed=None,
    ) -> None:
        super().__init__(seed=seed)
        self.states: Dict[str, ProgressionState] = {s.name: s for s in states}
        if initial_state not in self.states:
            raise KeyError(f"initial_state {initial_state!r} not in states")
        self.initial_state = initial_state
        self.years_to_simulate = int(years_to_simulate)
        self.base = base_generator or DistributionPatientGenerator(seed=seed)

    def _walk(self) -> Tuple[str, List[str]]:
        history = [self.initial_state]
        current = self.initial_state
        for _ in range(self.years_to_simulate):
            node = self.states[current]
            if not node.transitions:
                break
            destinations = list(node.transitions.keys())
            probs = np.array(list(node.transitions.values()), dtype=float)
            if not np.isclose(probs.sum(), 1.0):
                probs = probs / probs.sum()
            current = str(self.rng.choice(destinations, p=probs))
            history.append(current)
            if current not in self.states:
                raise KeyError(f"Markov walked to unknown state {current!r}")
        return current, history

    def sample(self) -> Patient:
        final_state, history = self._walk()
        patient = self.base.sample()
        patient.metadata["progression_history"] = history
        node = self.states[final_state]
        if node.disease_to_attach:
            disease_cls = get_disease(node.disease_to_attach)
            patient.add_disease(disease_cls())
        return patient
