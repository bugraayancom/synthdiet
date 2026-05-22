"""Counterfactual simulation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union

from synthdiet.behavior.adherence import AdherenceModel
from synthdiet.diets.base import DietPlan
from synthdiet.patients.patient import Patient
from synthdiet.simulation import DietSimulator, SimulationResult


@dataclass
class CounterfactualPair:
    """Same patient evaluated under two diets."""

    patient_id: str
    treatment: SimulationResult
    control: SimulationResult

    def individual_effect(self, outcome: str = "weight_kg") -> float:
        """Difference of final values (treatment - control) for an outcome."""
        first = lambda r: getattr(r.timeline[0], outcome, None) or r.timeline[0].biomarkers.get(outcome)
        last = lambda r: getattr(r.timeline[-1], outcome, None) or r.timeline[-1].biomarkers.get(outcome)
        delta_t = last(self.treatment) - first(self.treatment)
        delta_c = last(self.control) - first(self.control)
        return float(delta_t - delta_c)


def counterfactual_run(
    patient: Patient,
    treatment_diet: DietPlan,
    control_diet: DietPlan,
    duration_weeks: int = 12,
    adherence: Union[float, AdherenceModel] = 1.0,
    engine: str = "simple",
) -> CounterfactualPair:
    """Evaluate the same patient under ``treatment_diet`` and ``control_diet``.

    Two independent :class:`DietSimulator` runs are executed, each on a deep
    clone of the input patient (so the original is unchanged).
    """
    sim = DietSimulator(adherence=adherence, engine=engine, sampling_weeks=max(1, duration_weeks // 4))
    treatment_result = sim.run(patient.clone(), treatment_diet, duration_weeks=duration_weeks)
    sim2 = DietSimulator(adherence=adherence, engine=engine, sampling_weeks=max(1, duration_weeks // 4))
    control_result = sim2.run(patient.clone(), control_diet, duration_weeks=duration_weeks)
    return CounterfactualPair(
        patient_id=patient.patient_id,
        treatment=treatment_result,
        control=control_result,
    )
