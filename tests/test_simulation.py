"""Tests for the diet simulation engine."""

from __future__ import annotations

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
from synthdiet.diseases import Hypertension, Type2Diabetes
from synthdiet.simulation.metabolism import (
    mifflin_st_jeor,
    total_daily_energy_expenditure,
)


def make_patient() -> Patient:
    return Patient(
        demographics=Demographics(age=50, sex=Sex.MALE),
        anthropometrics=Anthropometrics(height_cm=178, weight_kg=95),
        lifestyle=Lifestyle(),
    )


def test_mifflin_st_jeor_known_value() -> None:
    # Male 80 kg, 180 cm, 30 y -> ~1780 kcal
    bmr = mifflin_st_jeor(80, 180, 30, Sex.MALE)
    assert 1750 < bmr < 1830


def test_tdee_uses_activity_factor() -> None:
    p = make_patient()
    tdee = total_daily_energy_expenditure(p)
    assert tdee > 0
    assert tdee > mifflin_st_jeor(95, 178, 50, Sex.MALE)


def test_simulator_weight_loss_on_hypocaloric_diet() -> None:
    p = make_patient()
    sim = DietSimulator(adherence=1.0)
    diet = standard_diet(daily_energy_kcal=1500)
    result = sim.run(p, diet, duration_weeks=8)
    assert result.weight_change_kg < 0
    assert len(result.timeline) >= 2
    assert result.final_patient is not None
    assert result.final_patient.anthropometrics.weight_kg < 95


def test_constraint_warnings_for_diabetic_on_high_sodium() -> None:
    p = make_patient()
    p.add_disease(Type2Diabetes(severity="moderate"))
    p.add_disease(Hypertension(severity="severe"))
    sim = DietSimulator()
    diet = standard_diet()
    diet.sodium_mg_per_day = 4000
    warnings = sim.check_diet_against_constraints(p, diet)
    assert any("sodium" in w for w in warnings)


def test_mediterranean_lowers_hba1c_in_t2dm() -> None:
    p = make_patient()
    p.add_disease(Type2Diabetes(severity="moderate"))
    baseline_a1c = p.biomarkers.get("hba1c_pct")
    sim = DietSimulator(adherence=1.0)
    result = sim.run(p, mediterranean_diet(), duration_weeks=12)
    final_a1c = result.final_patient.biomarkers.get("hba1c_pct")
    assert final_a1c < baseline_a1c
