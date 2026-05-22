"""Tests for the causal inference module."""

from __future__ import annotations

import pytest

from synthdiet import (
    CohortGenerator,
    CohortSpec,
    DiseaseSpec,
    mediterranean_diet,
    standard_diet,
)
from synthdiet.causal import (
    ATEEstimator,
    ConfoundingExperiment,
    DietDAG,
    cate_by_subgroup,
    counterfactual_run,
)
from synthdiet.causal.dag import default_diet_dag


@pytest.fixture
def cohort():
    spec = CohortSpec(
        size=40,
        diseases=[DiseaseSpec("type_2_diabetes", prevalence=0.6)],
    )
    return CohortGenerator(spec, seed=2025).generate()


def test_counterfactual_run_returns_two_results(cohort) -> None:
    patient = cohort[0]
    pair = counterfactual_run(
        patient, mediterranean_diet(), standard_diet(), duration_weeks=8
    )
    assert pair.patient_id == patient.patient_id
    effect = pair.individual_effect("weight_kg")
    assert isinstance(effect, float)


def test_ate_estimator_returns_ci(cohort) -> None:
    est = ATEEstimator(
        treatment_diet=mediterranean_diet(),
        control_diet=standard_diet(),
        duration_weeks=8,
    )
    result = est.estimate(cohort, outcome="weight_kg")
    assert result.n == len(cohort)
    assert isinstance(result.ate, float)
    lo, hi = result.ci_95
    assert lo < result.ate < hi or lo <= result.ate <= hi  # CI brackets ATE


def test_cate_by_subgroup_returns_per_stratum_results(cohort) -> None:
    cate = cate_by_subgroup(
        cohort=cohort[:20],
        treatment_diet=mediterranean_diet(),
        control_diet=standard_diet(),
        subgroup_fn=lambda p: p.demographics.sex.value,
        outcome="weight_kg",
        duration_weeks=4,
    )
    assert all(k in {"male", "female", "intersex"} for k in cate)
    assert all(isinstance(v.ate, float) for v in cate.values())


def test_confounding_experiment_separates_true_from_naive(cohort) -> None:
    # Confound: heavier patients more likely to be assigned to Mediterranean.
    exp = ConfoundingExperiment(
        treatment_diet=mediterranean_diet(),
        control_diet=standard_diet(),
        propensity=lambda p: float(min(0.95, max(0.05, (p.bmi - 18) / 35.0))),
        duration_weeks=6,
    )
    out = exp.run(cohort, outcome="weight_kg", seed=1)
    assert "true_ate" in out and "naive" in out and "iptw" in out


def test_dag_builds_and_is_acyclic() -> None:
    dag = default_diet_dag()
    assert dag.is_acyclic()
    assert "bmi" in dag.nodes
    assert ("diet", "bmi") in dag.edges
    mermaid = dag.to_mermaid()
    assert mermaid.startswith("flowchart LR")
    parents_of_t2d = dag.parents("type_2_diabetes")
    assert "bmi" in parents_of_t2d


def test_dag_detects_cycle() -> None:
    dag = DietDAG()
    dag.add_edge("a", "b").add_edge("b", "c").add_edge("c", "a")
    assert not dag.is_acyclic()
