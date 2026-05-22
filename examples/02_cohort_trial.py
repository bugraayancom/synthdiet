"""Run a virtual diet trial on a synthetic cohort and compare two diets."""

from __future__ import annotations

from synthdiet import (
    CohortGenerator,
    CohortSpec,
    DietSimulator,
    DiseaseSpec,
    aggregate_cohort_results,
    dash_diet,
    evaluate_simulation,
    mediterranean_diet,
    summarise_cohort,
)


def main() -> None:
    spec = CohortSpec(
        size=200,
        diseases=[
            DiseaseSpec("hypertension", prevalence=0.45,
                        severity_weights={"mild": 4, "moderate": 4, "severe": 2}),
            DiseaseSpec("type_2_diabetes", prevalence=0.30,
                        severity_weights={"mild": 3, "moderate": 5, "severe": 2}),
            DiseaseSpec("dyslipidemia", prevalence=0.40),
            DiseaseSpec("obesity", prevalence=0.35,
                        fixed_kwargs={"bmi_class": "I"}),
        ],
    )
    cohort = CohortGenerator(spec, seed=2026).generate()

    sim = DietSimulator(adherence=0.75)

    for diet_builder in (mediterranean_diet, dash_diet):
        diet = diet_builder()
        evaluations = []
        for patient in cohort:
            result = sim.run(patient, diet, duration_weeks=12)
            warnings = sim.check_diet_against_constraints(patient, diet)
            evaluations.append(evaluate_simulation(result, constraint_warnings=warnings))

        print(f"\n=== {diet.name.upper()} ===")
        print(summarise_cohort(evaluations).to_string(index=False))

        per_patient = aggregate_cohort_results(evaluations)
        delta_a1c_col = "delta_hba1c_pct"
        if delta_a1c_col in per_patient.columns:
            print(f"Mean delta HbA1c: {per_patient[delta_a1c_col].mean():+.2f}")


if __name__ == "__main__":
    main()
