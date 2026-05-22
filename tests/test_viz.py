"""Tests for the visualisation utilities."""

from __future__ import annotations

import pytest

from synthdiet import CohortGenerator, CohortSpec, DiseaseSpec
from synthdiet.viz import describe_cohort, table1

mpl = pytest.importorskip("matplotlib", reason="matplotlib not installed", exc_type=ImportError)
mpl.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from synthdiet.diets import mediterranean_diet, standard_diet  # noqa: E402
from synthdiet.simulation import DietSimulator  # noqa: E402
from synthdiet.trials import ParallelTrial  # noqa: E402
from synthdiet.viz import consort_diagram, forest_plot, trajectory_plot  # noqa: E402


@pytest.fixture
def cohort():
    spec = CohortSpec(
        size=40,
        diseases=[DiseaseSpec("type_2_diabetes", prevalence=0.5)],
    )
    return CohortGenerator(spec, seed=2026).generate()


def test_describe_cohort_returns_dataframe(cohort) -> None:
    df = describe_cohort(cohort)
    assert len(df) == len(cohort)
    assert "bmi" in df.columns


def test_table1_overall(cohort) -> None:
    t1 = table1(cohort)
    assert "overall" in t1.columns


def test_table1_grouped_by_sex(cohort) -> None:
    t1 = table1(cohort, group_by="sex")
    assert "male" in t1.columns or "female" in t1.columns


def test_trajectory_plot_runs(cohort) -> None:
    sim = DietSimulator()
    results = [sim.run(p, mediterranean_diet(), duration_weeks=12) for p in cohort[:8]]
    ax = trajectory_plot(results, variable="weight_kg")
    assert ax is not None


def test_forest_plot_runs() -> None:
    ax = forest_plot({"M": (-0.3, -0.5, -0.1), "F": (-0.2, -0.4, 0.0)})
    assert ax is not None


def test_consort_runs(cohort) -> None:
    trial = ParallelTrial(
        cohort=cohort,
        arms={"a": standard_diet(), "b": mediterranean_diet()},
        duration_weeks=8,
        primary_outcome="weight_kg",
    )
    result = trial.run(seed=1)
    ax = consort_diagram(result)
    assert ax is not None
