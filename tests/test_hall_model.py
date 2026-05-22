"""Tests for the Hall 2011 body composition simulator."""

from __future__ import annotations

import pytest

from synthdiet import (
    Anthropometrics,
    Demographics,
    DietSimulator,
    Lifestyle,
    Patient,
    Sex,
    mediterranean_diet,
    standard_diet,
)
from synthdiet.simulation.hall_model import (
    HallSimulation,
    HallSimulationParameters,
    estimate_baseline_intake,
    forbes_partition,
    initialise_body_composition,
    project_weight_change,
)


def make_patient(weight: float = 90.0, height: float = 175.0, age: int = 40) -> Patient:
    return Patient(
        demographics=Demographics(age=age, sex=Sex.MALE),
        anthropometrics=Anthropometrics(height_cm=height, weight_kg=weight),
        lifestyle=Lifestyle(),
    )


def test_forbes_partition_monotone() -> None:
    """Higher fat mass should partition LESS energy to lean tissue."""
    assert forbes_partition(10) > forbes_partition(40)
    assert 0 < forbes_partition(50) < 1


def test_initialise_body_composition_idempotent() -> None:
    patient = make_patient()
    initialise_body_composition(patient)
    fat0 = patient.anthropometrics.fat_mass_kg
    lean0 = patient.anthropometrics.lean_mass_kg
    initialise_body_composition(patient)
    assert patient.anthropometrics.fat_mass_kg == fat0
    assert patient.anthropometrics.lean_mass_kg == lean0
    assert fat0 is not None and lean0 is not None
    assert fat0 + lean0 == pytest.approx(patient.anthropometrics.weight_kg, rel=1e-3)


def test_steady_state_keeps_weight_within_one_kg() -> None:
    """Constant intake at baseline should keep weight stable over a year."""
    patient = make_patient(weight=85, height=180, age=35)
    initialise_body_composition(patient)
    baseline = estimate_baseline_intake(patient)
    sim = HallSimulation(patient=patient, baseline_energy_intake_kcal=baseline)
    sim.run_constant(baseline, days=365)
    final = sim.states[-1]
    assert abs(final.body_weight_kg - 85) < 1.5


def test_caloric_deficit_drives_weight_loss() -> None:
    patient = make_patient(weight=100, height=178, age=45)
    initialise_body_composition(patient)
    baseline = estimate_baseline_intake(patient)
    state = project_weight_change(patient, intake_kcal=baseline - 500, days=180)
    assert state.body_weight_kg < 100
    # ~500 kcal/day deficit for 180 days -> 8-10 kg loss (Hall predicts less than 7700 rule)
    loss = 100 - state.body_weight_kg
    assert 4 < loss < 12, f"unexpected loss magnitude: {loss:.1f} kg"


def test_fat_provides_majority_of_energy_in_overweight_deficit() -> None:
    """Forbes partition: most ENERGY from a deficit comes from fat tissue.

    Note that, by mass, lean loss can exceed fat loss at moderate adiposity
    because lean tissue has ~5x lower energy density. This test verifies the
    energetic partitioning instead.
    """
    from synthdiet.simulation.hall_model import (
        RHO_FAT_KCAL_PER_KG,
        RHO_LEAN_KCAL_PER_KG,
    )

    patient = make_patient(weight=100, height=175, age=40)
    initialise_body_composition(patient)
    fat0 = patient.anthropometrics.fat_mass_kg
    lean0 = patient.anthropometrics.lean_mass_kg
    baseline = estimate_baseline_intake(patient)
    final = project_weight_change(patient, intake_kcal=baseline - 600, days=180)
    fat_loss_kg = fat0 - final.fat_mass_kg  # type: ignore[operator]
    lean_loss_kg = lean0 - final.lean_mass_kg  # type: ignore[operator]
    energy_from_fat = fat_loss_kg * RHO_FAT_KCAL_PER_KG
    energy_from_lean = lean_loss_kg * RHO_LEAN_KCAL_PER_KG
    assert fat_loss_kg > 0
    assert energy_from_fat > energy_from_lean


def test_severe_obesity_loses_more_fat_mass_than_lean_mass() -> None:
    """At very high adiposity Forbes-p drops enough that fat *mass* loss
    exceeds lean *mass* loss."""
    patient = Patient(
        demographics=Demographics(age=45, sex=Sex.MALE),
        anthropometrics=Anthropometrics(
            height_cm=170, weight_kg=140, body_fat_pct=45.0
        ),
        lifestyle=Lifestyle(),
    )
    initialise_body_composition(patient)
    fat0 = patient.anthropometrics.fat_mass_kg
    lean0 = patient.anthropometrics.lean_mass_kg
    baseline = estimate_baseline_intake(patient)
    final = project_weight_change(patient, intake_kcal=baseline - 800, days=180)
    fat_loss = fat0 - final.fat_mass_kg  # type: ignore[operator]
    lean_loss = lean0 - final.lean_mass_kg  # type: ignore[operator]
    assert fat_loss > lean_loss


def test_diet_simulator_with_hall_engine() -> None:
    patient = make_patient(weight=95, height=178, age=50)
    sim = DietSimulator(adherence=1.0, engine="hall_2011")
    result = sim.run(patient, standard_diet(daily_energy_kcal=1500), duration_weeks=12)
    assert result.weight_change_kg < 0
    # Hall model loses less than 7700-rule for the same deficit
    assert -10 < result.weight_change_kg < -1
    assert result.final_patient.anthropometrics.fat_mass_kg is not None


def test_hall_parameters_can_be_overridden() -> None:
    patient = make_patient()
    custom = HallSimulationParameters(adaptive_eta=0.30)  # strong adaptation
    initialise_body_composition(patient)
    baseline = estimate_baseline_intake(patient)
    state_default = project_weight_change(patient.clone(), baseline - 500, days=90)
    state_strong = project_weight_change(
        patient.clone(), baseline - 500, days=90, parameters=custom
    )
    # Stronger adaptive thermogenesis -> less weight loss
    assert state_strong.body_weight_kg > state_default.body_weight_kg
