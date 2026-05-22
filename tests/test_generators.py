"""Tests for the synthetic-patient generators."""

from __future__ import annotations

import numpy as np

from synthdiet import (
    CohortGenerator,
    CohortSpec,
    CopulaPatientGenerator,
    DiseaseSpec,
    DistributionPatientGenerator,
    MarkovProgressionGenerator,
    Patient,
    ProgressionState,
    RandomPatientGenerator,
)


def test_random_generator_seed_reproducible() -> None:
    g1 = RandomPatientGenerator(seed=42)
    g2 = RandomPatientGenerator(seed=42)
    a = g1.sample()
    b = g2.sample()
    assert a.demographics.age == b.demographics.age
    assert a.anthropometrics.height_cm == b.anthropometrics.height_cm


def test_distribution_generator_yields_valid_patient() -> None:
    g = DistributionPatientGenerator(seed=0)
    p = g.sample()
    assert 15.0 <= p.bmi <= 60.0
    assert 18 <= p.age <= 90


def test_copula_generator_induces_correlation() -> None:
    g = CopulaPatientGenerator(seed=0)
    patients = g.sample_many(300)
    bmi = np.array([p.bmi for p in patients])
    tg = np.array([p.biomarkers.get("triglycerides_mg_dl", 0.0) for p in patients])
    hdl = np.array([p.biomarkers.get("hdl_mg_dl", 0.0) for p in patients])
    corr_bmi_tg = np.corrcoef(bmi, tg)[0, 1]
    corr_bmi_hdl = np.corrcoef(bmi, hdl)[0, 1]
    assert corr_bmi_tg > 0.10
    assert corr_bmi_hdl < -0.10


def test_cohort_generator_applies_diseases() -> None:
    spec = CohortSpec(
        size=200,
        diseases=[
            DiseaseSpec("type_2_diabetes", prevalence=0.4,
                        severity_weights={"mild": 1, "moderate": 2, "severe": 1}),
            DiseaseSpec("hypertension", prevalence=0.3),
        ],
    )
    g = CohortGenerator(spec, seed=1)
    cohort = g.generate()
    diabetic_share = np.mean([p.has_disease("type_2_diabetes") for p in cohort])
    hypertensive_share = np.mean([p.has_disease("hypertension") for p in cohort])
    assert 0.25 < diabetic_share < 0.55
    assert 0.20 < hypertensive_share < 0.45
    for p in cohort:
        assert isinstance(p, Patient)


def test_markov_generator_progresses() -> None:
    states = [
        ProgressionState("healthy", transitions={"healthy": 0.7, "prediabetic": 0.3}),
        ProgressionState(
            "prediabetic",
            transitions={"prediabetic": 0.6, "diabetic": 0.4},
            disease_to_attach="prediabetes",
        ),
        ProgressionState(
            "diabetic", transitions={"diabetic": 1.0},
            disease_to_attach="type_2_diabetes",
        ),
    ]
    g = MarkovProgressionGenerator(
        states=states, initial_state="healthy", years_to_simulate=20, seed=2
    )
    cohort = g.sample_many(50)
    final_states = {p.metadata["progression_history"][-1] for p in cohort}
    assert final_states <= {"healthy", "prediabetic", "diabetic"}
