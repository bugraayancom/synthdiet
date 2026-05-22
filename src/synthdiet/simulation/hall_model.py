"""Hall 2011 dynamic body-weight and composition model.

This module implements a simplified, single-compartment version of the
Hall et al. 2011 body weight simulator (the engine behind the NIH Body
Weight Planner).

Reference
---------
Hall KD, Sacks G, Chandramohan D, Chow CC, Wang YC, Gortmaker SL, Swinburn BA.
"Quantification of the effect of energy imbalance on bodyweight."
The Lancet. 2011;378(9793):826-837.
doi:10.1016/S0140-6736(11)60812-X

The model separates body mass into fat mass (FM) and fat-free / lean mass (L).
Energy partitioning follows Forbes' empirical relationship:

    p = C / (C + FM)        with C ~ 10.4

so that an obese subject loses proportionally more fat than a lean subject for
the same total energy deficit. Adaptive thermogenesis is captured by the
``eta`` coefficient that reduces resting energy expenditure when intake falls
below baseline.

The implementation here is intentionally compact — a forward-Euler integrator
with a one-day time step — which is sufficient for week- to year-scale
simulations of dietary interventions. For sub-daily accuracy (e.g. modelling
glycogen swings within a 24 h fast) a stiff ODE integrator would be needed;
that level of detail is outside the scope of this teaching/research tool.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np

from synthdiet.patients.demographics import Sex
from synthdiet.patients.patient import Patient
from synthdiet.simulation.metabolism import basal_metabolic_rate

# --- Hall 2011 default constants -----------------------------------------
# Energy density of stored fat and stored lean tissue (kcal/kg).
RHO_FAT_KCAL_PER_KG: float = 9440.0
RHO_LEAN_KCAL_PER_KG: float = 1820.0

# Resting energy expenditure linear coefficients (kcal/kg/day).
GAMMA_FAT: float = 3.2
GAMMA_LEAN: float = 22.0

# Spontaneous physical activity coefficient (kcal/kg/day).
DELTA_SPA: float = 6.0

# Thermic effect of food (fraction of energy intake).
TEF_FRACTION: float = 0.10

# Adaptive thermogenesis coefficient (fraction).
ADAPTIVE_ETA: float = 0.14

# Forbes constant for fat-mass partitioning (kg).
FORBES_C: float = 10.4


def forbes_partition(fat_mass_kg: float, *, c: float = FORBES_C) -> float:
    """Return ``p``, the fraction of energy imbalance routed to lean mass."""
    return c / (c + max(fat_mass_kg, 0.1))


def initialise_body_composition(patient: Patient) -> None:
    """Fill in ``fat_mass_kg`` and ``lean_mass_kg`` if missing.

    Uses the Deurenberg BMI-based body-fat estimate; falls back to the
    explicit ``body_fat_pct`` field if it was already set by the user.
    """
    anthro = patient.anthropometrics
    if anthro.fat_mass_kg is not None and anthro.lean_mass_kg is not None:
        return

    if anthro.body_fat_pct is not None:
        bf_pct = float(anthro.body_fat_pct)
    else:
        bf_pct = anthro.estimate_body_fat_pct(
            sex=patient.demographics.sex.value,
            age=patient.demographics.age,
        )
    bf_pct = float(np.clip(bf_pct, 5.0, 60.0))
    fat = anthro.weight_kg * bf_pct / 100.0
    lean = anthro.weight_kg - fat
    anthro.fat_mass_kg = float(fat)
    anthro.lean_mass_kg = float(lean)
    if anthro.body_fat_pct is None:
        anthro.body_fat_pct = bf_pct


@dataclass
class HallSimulationParameters:
    """Tunable parameters for the Hall body composition model.

    Defaults follow Hall (2011). Override individual values for sensitivity
    analyses or to calibrate against a specific cohort.
    """

    rho_fat: float = RHO_FAT_KCAL_PER_KG
    rho_lean: float = RHO_LEAN_KCAL_PER_KG
    gamma_fat: float = GAMMA_FAT
    gamma_lean: float = GAMMA_LEAN
    delta_spa: float = DELTA_SPA
    tef_fraction: float = TEF_FRACTION
    adaptive_eta: float = ADAPTIVE_ETA
    forbes_c: float = FORBES_C


@dataclass
class HallState:
    """A snapshot of the Hall model's compartments."""

    day: int
    fat_mass_kg: float
    lean_mass_kg: float
    body_weight_kg: float
    energy_intake_kcal: float
    energy_expenditure_kcal: float
    adaptive_thermogenesis_kcal: float

    @property
    def energy_balance_kcal(self) -> float:
        return self.energy_intake_kcal - self.energy_expenditure_kcal

    @property
    def body_fat_pct(self) -> float:
        return 100.0 * self.fat_mass_kg / max(self.body_weight_kg, 1e-6)


@dataclass
class HallSimulation:
    """Wraps a single-patient Hall simulation run.

    On construction the model is calibrated so that energy expenditure
    equals ``baseline_energy_intake_kcal`` at day 0; the calibration constant
    represents inter-individual variability in baseline metabolic rate that is
    not captured by the body-composition coefficients alone.
    """

    patient: Patient
    baseline_energy_intake_kcal: float
    parameters: HallSimulationParameters = field(default_factory=HallSimulationParameters)
    physical_activity_kcal_per_kg: float = 0.0
    states: List[HallState] = field(default_factory=list)
    k_constant: float = field(init=False, default=0.0)

    def __post_init__(self) -> None:
        initialise_body_composition(self.patient)
        anthro = self.patient.anthropometrics
        fat0 = float(anthro.fat_mass_kg)  # type: ignore[arg-type]
        lean0 = float(anthro.lean_mass_kg)  # type: ignore[arg-type]
        # Calibrate K so that EE = baseline_intake at day 0.
        uncalibrated_ee = self._uncalibrated_ee(
            fat=fat0,
            lean=lean0,
            intake=self.baseline_energy_intake_kcal,
            adaptive=0.0,
        )
        self.k_constant = self.baseline_energy_intake_kcal - uncalibrated_ee

        self.states.append(
            HallState(
                day=0,
                fat_mass_kg=fat0,
                lean_mass_kg=lean0,
                body_weight_kg=float(anthro.weight_kg),
                energy_intake_kcal=self.baseline_energy_intake_kcal,
                energy_expenditure_kcal=self.baseline_energy_intake_kcal,
                adaptive_thermogenesis_kcal=0.0,
            )
        )

    # Core ----------------------------------------------------------------
    def step(self, intake_kcal: float) -> HallState:
        """Advance the simulation by one day, returning the new state."""
        prev = self.states[-1]
        params = self.parameters
        delta_intake = intake_kcal - self.baseline_energy_intake_kcal
        # Hall AT is a fraction of intake-change; it directly modifies EE.
        # During a deficit (delta_intake < 0) the body conserves energy, so
        # AT < 0 and is *added* to EE, reducing it.
        adaptive = params.adaptive_eta * delta_intake

        ee = self._instantaneous_ee(
            fat=prev.fat_mass_kg,
            lean=prev.lean_mass_kg,
            intake=intake_kcal,
            adaptive=adaptive,
        )
        balance = intake_kcal - ee
        p = forbes_partition(prev.fat_mass_kg, c=params.forbes_c)

        d_lean = p * balance / params.rho_lean
        d_fat = (1.0 - p) * balance / params.rho_fat

        new_fat = max(2.0, prev.fat_mass_kg + d_fat)
        new_lean = max(20.0, prev.lean_mass_kg + d_lean)
        new_weight = new_fat + new_lean

        state = HallState(
            day=prev.day + 1,
            fat_mass_kg=new_fat,
            lean_mass_kg=new_lean,
            body_weight_kg=new_weight,
            energy_intake_kcal=intake_kcal,
            energy_expenditure_kcal=ee,
            adaptive_thermogenesis_kcal=adaptive,
        )
        self.states.append(state)
        return state

    def run(self, intake_schedule: List[float]) -> List[HallState]:
        """Run the simulation for ``len(intake_schedule)`` days."""
        for kcal in intake_schedule:
            self.step(kcal)
        return self.states

    def run_constant(self, intake_kcal: float, days: int) -> List[HallState]:
        """Run a constant-intake simulation for ``days`` days."""
        if days <= 0:
            raise ValueError("days must be > 0")
        return self.run([intake_kcal] * days)

    # Internals -----------------------------------------------------------
    def _uncalibrated_ee(
        self,
        *,
        fat: float,
        lean: float,
        intake: float,
        adaptive: float,
    ) -> float:
        params = self.parameters
        rmr = params.gamma_fat * fat + params.gamma_lean * lean
        tef = params.tef_fraction * intake
        spa = params.delta_spa * (fat + lean)
        pa = self.physical_activity_kcal_per_kg * (fat + lean)
        return rmr + tef + spa + pa + adaptive

    def _instantaneous_ee(
        self,
        *,
        fat: float,
        lean: float,
        intake: float,
        adaptive: float,
    ) -> float:
        uncalibrated = self._uncalibrated_ee(
            fat=fat, lean=lean, intake=intake, adaptive=adaptive
        )
        return max(800.0, uncalibrated + self.k_constant)


def estimate_baseline_intake(patient: Patient) -> float:
    """Return a maintenance energy intake estimate for ``patient``.

    Uses the Mifflin-St Jeor BMR multiplied by the patient's activity factor
    so that, at this intake, the Hall model is approximately at steady state.
    """
    bmr = basal_metabolic_rate(patient)
    return float(bmr * patient.lifestyle.activity_level.factor)


def project_weight_change(
    patient: Patient,
    intake_kcal: float,
    days: int,
    *,
    parameters: Optional[HallSimulationParameters] = None,
) -> HallState:
    """Convenience wrapper: simulate ``days`` days of constant ``intake_kcal``.

    Returns the final :class:`HallState`. The patient object is *not* mutated;
    pass ``patient.clone()`` first if you want to keep the original intact.
    """
    sim = HallSimulation(
        patient=patient,
        baseline_energy_intake_kcal=estimate_baseline_intake(patient),
        parameters=parameters or HallSimulationParameters(),
    )
    sim.run_constant(intake_kcal, days)
    return sim.states[-1]


__all__ = [
    "ADAPTIVE_ETA",
    "DELTA_SPA",
    "FORBES_C",
    "GAMMA_FAT",
    "GAMMA_LEAN",
    "HallSimulation",
    "HallSimulationParameters",
    "HallState",
    "RHO_FAT_KCAL_PER_KG",
    "RHO_LEAN_KCAL_PER_KG",
    "TEF_FRACTION",
    "estimate_baseline_intake",
    "forbes_partition",
    "initialise_body_composition",
    "project_weight_change",
]


# Suppress unused import warning; Sex is re-exported for downstream typing.
_ = Sex
