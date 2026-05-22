"""Quickstart: simulate a Mediterranean diet on a single type-2 diabetic patient."""

from __future__ import annotations

from synthdiet import (
    Anthropometrics,
    Demographics,
    DietSimulator,
    Lifestyle,
    Patient,
    Sex,
    evaluate_simulation,
    format_evaluation_report,
    mediterranean_diet,
)
from synthdiet.diseases import Type2Diabetes
from synthdiet.patients.lifestyle import ActivityLevel


def main() -> None:
    patient = Patient(
        demographics=Demographics(age=57, sex=Sex.MALE, country="TR"),
        anthropometrics=Anthropometrics(height_cm=176, weight_kg=98, waist_cm=108),
        lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT),
    )
    patient.add_disease(Type2Diabetes(severity="moderate"))
    print(patient.summary())

    sim = DietSimulator(adherence=0.85, sampling_weeks=4)
    diet = mediterranean_diet(daily_energy_kcal=1800)
    warnings = sim.check_diet_against_constraints(patient, diet)
    if warnings:
        print("\nConstraint warnings:")
        for w in warnings:
            print(f"  - {w}")

    result = sim.run(patient, diet, duration_weeks=24)
    evaluation = evaluate_simulation(result, constraint_warnings=warnings)
    print("\n" + format_evaluation_report(evaluation))


if __name__ == "__main__":
    main()
