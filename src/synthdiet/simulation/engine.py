"""The diet simulation engine.

The simulator advances a :class:`~synthdiet.patients.Patient` week by week
on a given :class:`~synthdiet.diets.DietPlan`. Each tick:

* Updates body weight from net energy balance using the rule
  1 kg fat ≈ 7700 kcal (configurable).
* Updates biomarkers using each attached disease's ``response_to_diet`` hook
  *plus* a baseline drift toward reference values for any diet whose macros
  fall within the patient's overall constraints.

The simulator stays deliberately simple: it is intended for *what-if* trials
and teaching, not for clinical decision support.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Union

import pandas as pd

from synthdiet.behavior.adherence import AdherenceModel, ConstantAdherence
from synthdiet.diets.base import DietPlan
from synthdiet.diseases.base import NutritionalConstraints
from synthdiet.interactions.medications import (
    apply_medication_effects,
    summarise_warnings,
)
from synthdiet.patients.patient import Patient
from synthdiet.simulation.hall_model import (
    HallSimulation,
    HallSimulationParameters,
    estimate_baseline_intake,
)
from synthdiet.simulation.metabolism import total_daily_energy_expenditure
from synthdiet.utils.constants import KCAL_PER_KG_BODY_FAT


@dataclass
class TimePoint:
    """A snapshot of patient state at a given simulation week."""

    week: int
    weight_kg: float
    bmi: float
    biomarkers: Dict[str, float] = field(default_factory=dict)
    energy_balance_kcal_per_day: float = 0.0
    adherence: float = 1.0
    notes: List[str] = field(default_factory=list)


@dataclass
class SimulationResult:
    """The outcome of running a diet simulation on a patient."""

    patient_id: str
    diet_name: str
    duration_weeks: int
    timeline: List[TimePoint] = field(default_factory=list)
    final_patient: Optional[Patient] = None

    # Convenience -----------------------------------------------------------
    def as_dataframe(self) -> pd.DataFrame:
        """Return the simulation timeline as a tidy pandas DataFrame."""
        rows: List[Dict[str, Any]] = []
        for tp in self.timeline:
            row: Dict[str, Any] = {
                "week": tp.week,
                "weight_kg": tp.weight_kg,
                "bmi": tp.bmi,
                "energy_balance_kcal_per_day": tp.energy_balance_kcal_per_day,
                "adherence": tp.adherence,
            }
            row.update({f"bm_{k}": v for k, v in tp.biomarkers.items()})
            rows.append(row)
        return pd.DataFrame(rows)

    @property
    def weight_change_kg(self) -> float:
        if not self.timeline:
            return 0.0
        return self.timeline[-1].weight_kg - self.timeline[0].weight_kg


class DietSimulator:
    """Apply a :class:`DietPlan` to a :class:`Patient` over time."""

    def __init__(
        self,
        adherence: Union[float, AdherenceModel] = 1.0,
        sampling_weeks: int = 4,
        bmr_equation: str = "mifflin_st_jeor",
        engine: str = "simple",
        hall_parameters: Optional[HallSimulationParameters] = None,
    ) -> None:
        if engine not in {"simple", "hall_2011"}:
            raise ValueError("engine must be 'simple' or 'hall_2011'")
        if isinstance(adherence, AdherenceModel):
            self.adherence_model: AdherenceModel = adherence
        elif isinstance(adherence, (int, float)):
            if not 0.0 <= float(adherence) <= 1.0:
                raise ValueError("adherence must be in [0, 1]")
            self.adherence_model = ConstantAdherence(value=float(adherence))
        else:
            raise TypeError("adherence must be float or AdherenceModel")
        self.sampling_weeks = max(1, int(sampling_weeks))
        self.bmr_equation = bmr_equation
        self.engine = engine
        self.hall_parameters = hall_parameters or HallSimulationParameters()
        self._hall_sim: Optional[HallSimulation] = None
        self._current_week: int = 0

    @property
    def adherence(self) -> float:
        """Backwards-compatible shortcut returning the current adherence."""
        return self._current_adherence

    @property
    def _current_adherence(self) -> float:
        # Used for snapshot reporting and the simple legacy code path.
        return float(getattr(self, "_last_adherence", 1.0))

    def run(
        self,
        patient: Patient,
        diet: DietPlan,
        duration_weeks: int = 12,
        in_place: bool = False,
    ) -> SimulationResult:
        """Simulate ``patient`` on ``diet`` for ``duration_weeks``.

        Set ``in_place=True`` to mutate the original patient; otherwise the
        function operates on a deep copy.
        """
        if duration_weeks <= 0:
            raise ValueError("duration_weeks must be > 0")
        target = patient if in_place else copy.deepcopy(patient)
        result = SimulationResult(
            patient_id=target.patient_id,
            diet_name=diet.name,
            duration_weeks=duration_weeks,
        )

        if self.engine == "hall_2011":
            self._hall_sim = HallSimulation(
                patient=target,
                baseline_energy_intake_kcal=estimate_baseline_intake(target),
                parameters=self.hall_parameters,
            )
        else:
            self._hall_sim = None
        self.adherence_model.reset()

        self._last_adherence = self.adherence_model.adherence_for_week(0, target)
        result.timeline.append(self._snapshot(target, week=0, energy_balance=0.0))
        for week in range(1, duration_weeks + 1):
            self._current_week = week
            self._last_adherence = self.adherence_model.adherence_for_week(week, target)
            energy_balance = self._step(target, diet)
            if week % self.sampling_weeks == 0 or week == duration_weeks:
                result.timeline.append(
                    self._snapshot(target, week=week, energy_balance=energy_balance)
                )

        result.final_patient = target
        return result

    # Internals ------------------------------------------------------------
    def _step(self, patient: Patient, diet: DietPlan) -> float:
        tdee = total_daily_energy_expenditure(patient, equation=self.bmr_equation)
        adherence = self._last_adherence
        # Expose the prescribed intake to perceived-burden adherence models.
        setattr(patient, "_prescribed_kcal", diet.daily_energy_kcal)
        consumed = diet.daily_energy_kcal * adherence + tdee * (1.0 - adherence)
        balance = consumed - tdee

        if self.engine == "hall_2011" and self._hall_sim is not None:
            for _ in range(7):
                self._hall_sim.step(consumed)
            last = self._hall_sim.states[-1]
            patient.anthropometrics.weight_kg = last.body_weight_kg
            patient.anthropometrics.fat_mass_kg = last.fat_mass_kg
            patient.anthropometrics.lean_mass_kg = last.lean_mass_kg
            patient.anthropometrics.body_fat_pct = last.body_fat_pct
        else:
            weekly_balance_kcal = balance * 7
            weight_delta = weekly_balance_kcal / KCAL_PER_KG_BODY_FAT
            patient.anthropometrics.weight_kg = max(
                30.0, patient.anthropometrics.weight_kg + weight_delta
            )

        deltas = self._biomarker_deltas(patient, diet, duration_weeks=1)
        for name, delta in deltas.items():
            if name == "weight_kg":
                if self.engine != "hall_2011":
                    patient.anthropometrics.weight_kg += float(delta)
                continue
            current = patient.biomarkers.get(name) or 0.0
            patient.biomarkers.set(name, current + float(delta) * adherence)

        # Apply medication-induced biomarker drift.
        if getattr(patient, "medications", None):
            apply_medication_effects(patient, weeks_elapsed=1)

        return balance

    def _biomarker_deltas(
        self,
        patient: Patient,
        diet: DietPlan,
        duration_weeks: int,
    ) -> Mapping[str, float]:
        deltas: Dict[str, float] = {}
        for disease in patient.diseases:
            for k, v in disease.response_to_diet(patient, diet, duration_weeks).items():
                deltas[k] = deltas.get(k, 0.0) + float(v)
        return deltas

    def _snapshot(
        self, patient: Patient, *, week: int, energy_balance: float
    ) -> TimePoint:
        return TimePoint(
            week=week,
            weight_kg=patient.anthropometrics.weight_kg,
            bmi=patient.anthropometrics.bmi,
            biomarkers=dict(patient.biomarkers.values),
            energy_balance_kcal_per_day=energy_balance,
            adherence=self._current_adherence,
        )

    # Validation helpers ---------------------------------------------------
    def check_diet_against_constraints(
        self, patient: Patient, diet: DietPlan
    ) -> List[str]:
        """Return a list of human-readable warnings if ``diet`` violates any
        disease-specific :class:`NutritionalConstraints`.
        """
        warnings: List[str] = []
        macros = diet.macronutrient_distribution()
        merged = NutritionalConstraints()
        for disease in patient.diseases:
            merged = merged.merge(disease.nutritional_constraints(patient))

        for macro in ("carbohydrate", "protein", "fat"):
            attr = f"{macro}_pct_range"
            limits = getattr(merged, attr)
            if limits is None:
                continue
            low, high = limits
            value = macros.get(macro, 0.0)
            if value < low:
                warnings.append(
                    f"{macro} share {value:.2f} below recommended {low:.2f}"
                )
            elif value > high:
                warnings.append(
                    f"{macro} share {value:.2f} above recommended {high:.2f}"
                )

        if merged.sodium_mg_max is not None and (diet.sodium_mg_per_day or 0) > merged.sodium_mg_max:
            warnings.append(
                f"sodium {diet.sodium_mg_per_day:.0f} mg exceeds limit {merged.sodium_mg_max:.0f} mg"
            )
        if merged.added_sugar_pct_max is not None and (diet.added_sugar_pct or 0) > merged.added_sugar_pct_max:
            warnings.append(
                f"added-sugar share {diet.added_sugar_pct:.2f} exceeds limit {merged.added_sugar_pct_max:.2f}"
            )
        if merged.saturated_fat_pct_max is not None and (diet.saturated_fat_pct or 0) > merged.saturated_fat_pct_max:
            warnings.append(
                f"saturated fat share {diet.saturated_fat_pct:.2f} exceeds limit {merged.saturated_fat_pct_max:.2f}"
            )
        if merged.fiber_g_min is not None and (diet.fiber_g_per_day or 0) < merged.fiber_g_min:
            warnings.append(
                f"fibre {diet.fiber_g_per_day:.0f} g below minimum {merged.fiber_g_min:.0f} g"
            )
        forbidden_used = merged.forbidden_foods & diet.forbidden_food_set()
        if forbidden_used:
            warnings.append(
                f"diet uses forbidden foods: {sorted(forbidden_used)}"
            )
        # Medication-food collisions.
        if getattr(patient, "medications", None):
            warnings.extend(
                summarise_warnings(patient, diet_foods=diet.forbidden_food_set())
            )
        return warnings
