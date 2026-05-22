"""Trial designs: parallel, crossover, factorial."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Union

import numpy as np
import pandas as pd

from synthdiet.behavior.adherence import (
    AdherenceModel,
    ConstantAdherence,
    WeibullDropoutAdherence,
)
from synthdiet.diets.base import DietPlan
from synthdiet.patients.patient import Patient
from synthdiet.simulation import DietSimulator, SimulationResult
from synthdiet.trials.analysis import TrialResult
from synthdiet.trials.dropout import DropoutModel, NoDropout
from synthdiet.trials.randomization import (
    block_randomization,
    minimization,
    simple_randomization,
    stratified_randomization,
)
from synthdiet.utils.random_state import RandomState, as_random_state


def _make_adherence_model(value: Union[float, AdherenceModel]) -> AdherenceModel:
    if isinstance(value, AdherenceModel):
        return value
    return ConstantAdherence(value=float(value))


@dataclass
class ParallelTrial:
    """A parallel-arm randomised controlled trial.

    Patients are randomised once at baseline to a single arm and remain there
    for the duration of the trial.

    Parameters
    ----------
    cohort:
        Sequence of synthetic :class:`Patient` instances (typically generated
        via :class:`synthdiet.CohortGenerator`).
    arms:
        Mapping arm name -> :class:`DietPlan` to be applied during the trial.
    duration_weeks:
        Total length of the trial in weeks.
    primary_outcome:
        Biomarker key whose change is the primary outcome (e.g. ``"hba1c_pct"``).
        ``"weight_kg"`` and ``"bmi"`` are also recognised.
    secondary_outcomes:
        Other biomarker keys to report.
    randomization:
        One of ``"simple"``, ``"block"``, ``"stratified"``, or ``"minimization"``.
    strata:
        Required when randomization is ``"stratified"`` or ``"minimization"``.
    adherence:
        Either a fixed adherence value or an :class:`AdherenceModel`.
    dropout:
        A :class:`DropoutModel` that draws a per-patient dropout week.
    engine:
        ``"simple"`` or ``"hall_2011"`` body composition model.
    """

    cohort: Sequence[Patient]
    arms: Mapping[str, DietPlan]
    duration_weeks: int = 12
    primary_outcome: str = "weight_kg"
    secondary_outcomes: List[str] = field(default_factory=list)
    randomization: str = "block"
    strata: Optional[Sequence[Callable[[Patient], object]]] = None
    adherence: Union[float, AdherenceModel] = 0.85
    dropout: DropoutModel = field(default_factory=NoDropout)
    engine: str = "simple"

    def __post_init__(self) -> None:
        if len(self.arms) < 2:
            raise ValueError("trial requires at least 2 arms")

    # Core run -------------------------------------------------------------
    def run(self, seed: RandomState = None) -> TrialResult:
        rng = as_random_state(seed)
        assignments = self._randomise(rng)
        arm_names = list(self.arms.keys())

        rows: List[Dict[str, Any]] = []
        adherence_by_arm: Dict[str, List[float]] = {a: [] for a in arm_names}
        dropout_weeks: Dict[str, int] = {}

        for patient in self.cohort:
            arm = assignments[patient.patient_id]
            diet = self.arms[arm]
            dropout_week = self.dropout.sample_dropout_week(self.duration_weeks)
            effective_weeks = min(self.duration_weeks, dropout_week - 1)
            if effective_weeks <= 0:
                # Patient drops out at week 0 -> no follow-up data.
                row = self._make_zero_row(patient, arm)
                rows.append(row)
                dropout_weeks[patient.patient_id] = 0
                continue

            adherence_model = _make_adherence_model(self.adherence)
            sim = DietSimulator(
                adherence=adherence_model,
                sampling_weeks=max(1, effective_weeks),
                engine=self.engine,
            )
            result = sim.run(patient.clone(), diet, duration_weeks=effective_weeks)
            row = self._row_from_result(patient, arm, result, dropout_week)
            rows.append(row)
            adherence_by_arm[arm].append(row["mean_adherence"])
            dropout_weeks[patient.patient_id] = dropout_week

        outcomes = pd.DataFrame(rows)
        adherence_summary = {
            arm: float(np.mean(values)) if values else float("nan")
            for arm, values in adherence_by_arm.items()
        }
        return TrialResult(
            arms=assignments,
            arm_diets={a: d for a, d in self.arms.items()},
            outcomes=outcomes,
            duration_weeks=self.duration_weeks,
            primary_outcome=self.primary_outcome,
            secondary_outcomes=list(self.secondary_outcomes),
            dropout_weeks=dropout_weeks,
            adherence_summary=adherence_summary,
        )

    # Internals ------------------------------------------------------------
    def _randomise(self, rng: np.random.Generator) -> Dict[str, str]:
        arms = list(self.arms.keys())
        sub_seed = int(rng.integers(0, 1 << 32))
        if self.randomization == "simple":
            return simple_randomization(self.cohort, arms, seed=sub_seed)
        if self.randomization == "block":
            return block_randomization(self.cohort, arms, seed=sub_seed)
        if self.randomization == "stratified":
            if not self.strata:
                raise ValueError("strata required for stratified randomization")
            return stratified_randomization(
                self.cohort, arms, strata=self.strata, seed=sub_seed
            )
        if self.randomization == "minimization":
            if not self.strata:
                raise ValueError("strata (treated as factors) required for minimization")
            return minimization(
                self.cohort, arms, factors=self.strata, seed=sub_seed
            )
        raise ValueError(f"unknown randomization {self.randomization!r}")

    def _row_from_result(
        self,
        patient: Patient,
        arm: str,
        result: SimulationResult,
        dropout_week: int,
    ) -> Dict[str, Any]:
        first = result.timeline[0]
        last = result.timeline[-1]
        row: Dict[str, Any] = {
            "patient_id": patient.patient_id,
            "arm": arm,
            "dropout_week": dropout_week,
            "mean_adherence": float(np.mean([tp.adherence for tp in result.timeline])),
            "baseline_weight_kg": first.weight_kg,
            "final_weight_kg": last.weight_kg,
            "delta_weight_kg": last.weight_kg - first.weight_kg,
            "baseline_bmi": first.bmi,
            "final_bmi": last.bmi,
            "delta_bmi": last.bmi - first.bmi,
        }
        for outcome in [self.primary_outcome, *self.secondary_outcomes]:
            if outcome in {"weight_kg", "bmi"}:
                continue
            baseline = first.biomarkers.get(outcome)
            final = last.biomarkers.get(outcome)
            row[f"baseline_{outcome}"] = baseline
            row[f"final_{outcome}"] = final
            if baseline is not None and final is not None:
                row[f"delta_{outcome}"] = final - baseline
            else:
                row[f"delta_{outcome}"] = np.nan
        return row

    def _make_zero_row(self, patient: Patient, arm: str) -> Dict[str, Any]:
        row: Dict[str, Any] = {
            "patient_id": patient.patient_id,
            "arm": arm,
            "dropout_week": 0,
            "mean_adherence": 0.0,
            "baseline_weight_kg": patient.weight_kg,
            "final_weight_kg": patient.weight_kg,
            "delta_weight_kg": 0.0,
            "baseline_bmi": patient.bmi,
            "final_bmi": patient.bmi,
            "delta_bmi": 0.0,
        }
        for outcome in [self.primary_outcome, *self.secondary_outcomes]:
            if outcome in {"weight_kg", "bmi"}:
                continue
            baseline = patient.biomarkers.get(outcome)
            row[f"baseline_{outcome}"] = baseline
            row[f"final_{outcome}"] = baseline
            row[f"delta_{outcome}"] = 0.0
        return row


@dataclass
class CrossoverTrial:
    """Two-period crossover (AB / BA), each patient receives both diets.

    Assumes a wash-out is sufficient to clear carry-over effects (a stronger
    model would account for residual effects via a period-by-treatment
    interaction term — left as an extension).
    """

    cohort: Sequence[Patient]
    diet_a: DietPlan
    diet_b: DietPlan
    period_weeks: int = 8
    washout_weeks: int = 2
    primary_outcome: str = "weight_kg"
    secondary_outcomes: List[str] = field(default_factory=list)
    adherence: Union[float, AdherenceModel] = 0.85
    engine: str = "simple"

    def run(self, seed: RandomState = None) -> TrialResult:
        rng = as_random_state(seed)
        assignments: Dict[str, str] = {}
        rows: List[Dict[str, Any]] = []
        adherence_total: List[float] = []

        for patient in self.cohort:
            sequence = "AB" if rng.random() < 0.5 else "BA"
            assignments[patient.patient_id] = sequence

            first_diet, second_diet = (
                (self.diet_a, self.diet_b)
                if sequence == "AB"
                else (self.diet_b, self.diet_a)
            )

            sim = DietSimulator(
                adherence=_make_adherence_model(self.adherence),
                engine=self.engine,
                sampling_weeks=self.period_weeks,
            )
            r1 = sim.run(patient.clone(), first_diet, duration_weeks=self.period_weeks)
            mid = r1.final_patient
            # Apply washout as a "standard" intake period — simplified to a
            # constant maintenance phase.
            sim2 = DietSimulator(
                adherence=_make_adherence_model(self.adherence),
                engine=self.engine,
            )
            r2 = sim2.run(mid.clone(), second_diet, duration_weeks=self.period_weeks)

            row = {
                "patient_id": patient.patient_id,
                "arm": sequence,
                "dropout_week": self.period_weeks * 2 + 1,
                "mean_adherence": float(
                    np.mean([tp.adherence for tp in r1.timeline + r2.timeline])
                ),
                "baseline_weight_kg": r1.timeline[0].weight_kg,
                "final_weight_kg": r2.timeline[-1].weight_kg,
                "delta_weight_kg": r2.timeline[-1].weight_kg - r1.timeline[0].weight_kg,
                "baseline_bmi": r1.timeline[0].bmi,
                "final_bmi": r2.timeline[-1].bmi,
                "delta_bmi": r2.timeline[-1].bmi - r1.timeline[0].bmi,
            }
            for outcome in [self.primary_outcome, *self.secondary_outcomes]:
                if outcome in {"weight_kg", "bmi"}:
                    continue
                base = r1.timeline[0].biomarkers.get(outcome)
                end = r2.timeline[-1].biomarkers.get(outcome)
                row[f"baseline_{outcome}"] = base
                row[f"final_{outcome}"] = end
                row[f"delta_{outcome}"] = (
                    end - base if (base is not None and end is not None) else np.nan
                )
            rows.append(row)
            adherence_total.append(row["mean_adherence"])

        outcomes = pd.DataFrame(rows)
        return TrialResult(
            arms=assignments,
            arm_diets={"A": self.diet_a, "B": self.diet_b},
            outcomes=outcomes,
            duration_weeks=self.period_weeks * 2 + self.washout_weeks,
            primary_outcome=self.primary_outcome,
            secondary_outcomes=list(self.secondary_outcomes),
            adherence_summary={"crossover": float(np.mean(adherence_total))},
        )


@dataclass
class FactorialTrial:
    """2 x 2 factorial trial that crosses two interventions.

    Each patient is randomised to one of four arms formed by the Cartesian
    product of the two intervention factors. ``arms`` must be exactly four
    items whose keys are tuples like ``("med", "low_sodium")``.
    """

    cohort: Sequence[Patient]
    factor_arms: Mapping[tuple, DietPlan]
    duration_weeks: int = 12
    primary_outcome: str = "systolic_bp_mmhg"
    secondary_outcomes: List[str] = field(default_factory=list)
    adherence: Union[float, AdherenceModel] = 0.85
    engine: str = "simple"

    def __post_init__(self) -> None:
        if len(self.factor_arms) != 4:
            raise ValueError("FactorialTrial expects 4 arms")

    def run(self, seed: RandomState = None) -> TrialResult:
        # Re-use ParallelTrial by flattening the factor tuple key into a name.
        flat_arms = {"_x_".join(map(str, k)): v for k, v in self.factor_arms.items()}
        inner = ParallelTrial(
            cohort=self.cohort,
            arms=flat_arms,
            duration_weeks=self.duration_weeks,
            primary_outcome=self.primary_outcome,
            secondary_outcomes=self.secondary_outcomes,
            randomization="block",
            adherence=self.adherence,
            engine=self.engine,
        )
        return inner.run(seed=seed)
