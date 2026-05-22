"""Use a Markov progression model to generate prediabetic and diabetic patients."""

from __future__ import annotations

from collections import Counter

from synthdiet import MarkovProgressionGenerator, ProgressionState


def main() -> None:
    states = [
        ProgressionState("healthy",
                         transitions={"healthy": 0.85, "prediabetic": 0.15}),
        ProgressionState(
            "prediabetic",
            transitions={
                "prediabetic": 0.65,
                "healthy": 0.10,
                "diabetic": 0.25,
            },
            disease_to_attach="prediabetes",
        ),
        ProgressionState(
            "diabetic",
            transitions={"diabetic": 0.95, "diabetic_complications": 0.05},
            disease_to_attach="type_2_diabetes",
        ),
        ProgressionState(
            "diabetic_complications",
            transitions={"diabetic_complications": 1.0},
            disease_to_attach="type_2_diabetes",
        ),
    ]

    generator = MarkovProgressionGenerator(
        states=states,
        initial_state="healthy",
        years_to_simulate=15,
        seed=7,
    )
    cohort = generator.sample_many(500)
    final_states = Counter(p.metadata["progression_history"][-1] for p in cohort)
    print("Final state distribution after 15 simulated years:")
    for state, count in final_states.most_common():
        print(f"  {state:<28s} {count:4d} ({count / len(cohort) * 100:.1f}%)")


if __name__ == "__main__":
    main()
