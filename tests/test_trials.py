"""Tests for the RCT trial engine."""

from __future__ import annotations

from collections import Counter

import pytest

from synthdiet import (
    CohortGenerator,
    CohortSpec,
    DiseaseSpec,
    mediterranean_diet,
    standard_diet,
)
from synthdiet.diets.presets import dash_diet
from synthdiet.trials import (
    CrossoverTrial,
    FactorialTrial,
    ParallelTrial,
    WeibullDropout,
    block_randomization,
    minimization,
    simple_randomization,
    stratified_randomization,
)


@pytest.fixture
def cohort():
    spec = CohortSpec(
        size=80,
        diseases=[
            DiseaseSpec("type_2_diabetes", prevalence=0.5),
            DiseaseSpec("hypertension", prevalence=0.5),
        ],
    )
    return CohortGenerator(spec, seed=2024).generate()


def test_block_randomization_balanced(cohort) -> None:
    arms = block_randomization(cohort, ["A", "B"], block_size=4, seed=1)
    counts = Counter(arms.values())
    assert abs(counts["A"] - counts["B"]) <= 2


def test_simple_randomization_seed_reproducible(cohort) -> None:
    a = simple_randomization(cohort, ["A", "B"], seed=1)
    b = simple_randomization(cohort, ["A", "B"], seed=1)
    assert a == b


def test_stratified_balances_within_sex(cohort) -> None:
    arms = stratified_randomization(
        cohort, ["A", "B"], strata=[lambda p: p.demographics.sex], seed=7
    )
    male_counts = Counter()
    female_counts = Counter()
    for p in cohort:
        if p.demographics.sex.value == "male":
            male_counts[arms[p.patient_id]] += 1
        else:
            female_counts[arms[p.patient_id]] += 1
    assert abs(male_counts["A"] - male_counts["B"]) <= 2
    assert abs(female_counts["A"] - female_counts["B"]) <= 2


def test_minimization_balances_factors(cohort) -> None:
    arms = minimization(
        cohort,
        ["A", "B"],
        factors=[
            lambda p: p.demographics.sex,
            lambda p: p.has_disease("type_2_diabetes"),
        ],
        seed=3,
    )
    counts = Counter(arms.values())
    assert abs(counts["A"] - counts["B"]) <= 4


def test_parallel_trial_runs_and_produces_outcomes(cohort) -> None:
    trial = ParallelTrial(
        cohort=cohort,
        arms={"control": standard_diet(), "intervention": mediterranean_diet()},
        duration_weeks=12,
        primary_outcome="hba1c_pct",
        secondary_outcomes=["ldl_mg_dl"],
        randomization="block",
    )
    result = trial.run(seed=1)
    assert "delta_hba1c_pct" in result.outcomes.columns
    assert "delta_ldl_mg_dl" in result.outcomes.columns
    assert len(result.outcomes) == len(cohort)
    consort = result.consort_diagram()
    assert "Arm 'control'" in consort
    assert "Arm 'intervention'" in consort


def test_intention_to_treat_returns_signed_diff(cohort) -> None:
    trial = ParallelTrial(
        cohort=cohort,
        arms={"control": standard_diet(), "med": mediterranean_diet()},
        duration_weeks=12,
        primary_outcome="hba1c_pct",
        randomization="block",
    )
    result = trial.run(seed=1)
    itt = result.intention_to_treat(method="t_test")
    assert itt.outcome == "hba1c_pct"
    assert itt.n_a > 0 and itt.n_b > 0
    assert itt.method.startswith("ITT")


def test_per_protocol_excludes_low_adherence(cohort) -> None:
    trial = ParallelTrial(
        cohort=cohort,
        arms={"control": standard_diet(), "intervention": mediterranean_diet()},
        duration_weeks=12,
        primary_outcome="weight_kg",
        adherence=0.5,
    )
    result = trial.run(seed=1)
    pp = result.per_protocol(adherence_threshold=0.80)
    assert pp.n_a == 0 and pp.n_b == 0


def test_trial_with_weibull_dropout(cohort) -> None:
    trial = ParallelTrial(
        cohort=cohort,
        arms={"a": standard_diet(), "b": dash_diet()},
        duration_weeks=24,
        primary_outcome="systolic_bp_mmhg",
        dropout=WeibullDropout(shape=1.5, scale_weeks=12, seed=99),
    )
    result = trial.run(seed=1)
    dropouts = sum(
        1 for w in result.dropout_weeks.values() if w <= result.duration_weeks
    )
    assert dropouts > 0


def test_crossover_trial_runs(cohort) -> None:
    small = cohort[:20]
    trial = CrossoverTrial(
        cohort=small,
        diet_a=standard_diet(),
        diet_b=dash_diet(),
        period_weeks=4,
        primary_outcome="systolic_bp_mmhg",
    )
    result = trial.run(seed=4)
    assert len(result.outcomes) == 20
    assert "delta_systolic_bp_mmhg" in result.outcomes.columns


def test_factorial_2x2(cohort) -> None:
    small = cohort[:40]
    trial = FactorialTrial(
        cohort=small,
        factor_arms={
            ("med", "low_na"): dash_diet(),
            ("med", "std_na"): mediterranean_diet(),
            ("ctrl", "low_na"): dash_diet(),
            ("ctrl", "std_na"): standard_diet(),
        },
        duration_weeks=8,
        primary_outcome="systolic_bp_mmhg",
    )
    result = trial.run(seed=5)
    assert len(result.arm_names) == 4
