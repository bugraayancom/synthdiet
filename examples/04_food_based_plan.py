"""Build a food-based daily plan and check it against a CKD patient's limits."""

from __future__ import annotations

from synthdiet import (
    Anthropometrics,
    Demographics,
    DietPlan,
    DietSimulator,
    FoodServing,
    Lifestyle,
    Meal,
    Patient,
    Sex,
)
from synthdiet.diseases import ChronicKidneyDisease
from synthdiet.nutrition import default_food_database


def main() -> None:
    patient = Patient(
        demographics=Demographics(age=68, sex=Sex.FEMALE),
        anthropometrics=Anthropometrics(height_cm=160, weight_kg=72),
        lifestyle=Lifestyle(),
    )
    patient.add_disease(ChronicKidneyDisease(stage=4))

    db = default_food_database()
    meals = [
        Meal("breakfast", [
            FoodServing("white_bread", 60),
            FoodServing("egg", 50),
            FoodServing("apple", 150),
        ]),
        Meal("lunch", [
            FoodServing("chicken_breast", 90),
            FoodServing("white_rice", 200),
            FoodServing("carrot", 100),
            FoodServing("olive_oil", 8),
        ]),
        Meal("dinner", [
            FoodServing("white_bread", 40),
            FoodServing("cottage_cheese", 80),
            FoodServing("broccoli", 100),
            FoodServing("blueberries", 60),
        ]),
    ]
    plan = DietPlan(name="ckd_test", meals=meals, food_database=db)
    print(plan.summary())

    sim = DietSimulator(adherence=1.0)
    warnings = sim.check_diet_against_constraints(patient, plan)
    print("\nConstraint warnings:")
    for w in warnings or ["(none)"]:
        print(f"  - {w}")


if __name__ == "__main__":
    main()
