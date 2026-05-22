"""Tests for drug-nutrient interactions."""

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
from synthdiet.diseases import Type2Diabetes
from synthdiet.interactions import (
    INTERACTION_REGISTRY,
    available_medications,
    get_medication,
)


def make_patient() -> Patient:
    return Patient(
        demographics=Demographics(age=60, sex=Sex.FEMALE),
        anthropometrics=Anthropometrics(height_cm=165, weight_kg=78),
        lifestyle=Lifestyle(),
    )


def test_registry_has_20_medications() -> None:
    assert len(INTERACTION_REGISTRY) >= 19


def test_get_metformin_interactions() -> None:
    m = get_medication("metformin")
    assert m.name == "metformin"
    nutrients = [i.nutrient for i in m.interactions]
    assert "vitamin_b12" in nutrients


def test_get_unknown_raises() -> None:
    with pytest.raises(KeyError):
        get_medication("unicornazole")


def test_patient_can_carry_medications() -> None:
    p = make_patient()
    p.add_medication(get_medication("metformin"))
    p.add_medication(get_medication("atorvastatin"))
    assert p.has_medication("metformin")
    assert "atorvastatin" in p.medication_names()
    assert len(p.medications) == 2


def test_simulator_applies_metformin_b12_depletion() -> None:
    p = make_patient()
    p.add_disease(Type2Diabetes())
    p.add_medication(get_medication("metformin"))
    p.biomarkers.set("vitamin_b12_pg_ml", 400)
    sim = DietSimulator()
    result = sim.run(p, mediterranean_diet(), duration_weeks=12)
    final_b12 = result.final_patient.biomarkers.get("vitamin_b12_pg_ml")
    assert final_b12 < 400  # depleted


def test_simulator_warns_on_warfarin_inconsistent_vk() -> None:
    p = make_patient()
    p.add_medication(get_medication("warfarin"))
    diet = standard_diet()
    diet.meals.append(__import__("synthdiet").Meal("test", []))  # not used
    sim = DietSimulator()
    warnings = sim.check_diet_against_constraints(p, diet)
    assert any("warfarin" in w.lower() for w in warnings)


def test_grapefruit_with_statin_warning() -> None:
    p = make_patient()
    p.add_medication(get_medication("atorvastatin"))
    diet = standard_diet()
    # Synthesise a meal that includes grapefruit.
    from synthdiet import FoodServing, Meal
    from synthdiet.nutrition import default_food_database, Food
    from synthdiet.nutrition.nutrients import NutrientProfile

    db = default_food_database()
    db.add(Food(name="grapefruit", category="fruit",
                profile_per_100g=NutrientProfile(energy_kcal=42, nutrients={"fiber_g": 1.6})))
    diet.meals.append(Meal("breakfast", [FoodServing("grapefruit", 200)]))
    diet.food_database = db
    diet._refresh_from_meals()
    sim = DietSimulator()
    warnings = sim.check_diet_against_constraints(p, diet)
    assert any("grapefruit" in w.lower() for w in warnings)


def test_available_medications_returns_list() -> None:
    meds = available_medications()
    assert "metformin" in meds
    assert "atorvastatin" in meds
    assert len(meds) >= 19
