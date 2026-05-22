"""Tests for noise / missing-data injection."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from synthdiet import (
    Anthropometrics,
    Biomarkers,
    Demographics,
    Lifestyle,
    Patient,
    Sex,
)
from synthdiet.noise import (
    add_lab_measurement_error,
    add_self_report_bias,
    inject_mar_missing,
    inject_mcar_missing,
    inject_mnar_missing,
)


def _patients(n: int = 50) -> list:
    rng = np.random.default_rng(0)
    out = []
    for _ in range(n):
        p = Patient(
            demographics=Demographics(age=50, sex=Sex.MALE),
            anthropometrics=Anthropometrics(height_cm=175, weight_kg=85),
            lifestyle=Lifestyle(),
            biomarkers=Biomarkers(values={
                "hba1c_pct": 5.6 + rng.normal(0, 0.1),
                "ldl_mg_dl": 120 + rng.normal(0, 5),
                "fasting_glucose_mg_dl": 95 + rng.normal(0, 3),
            }),
        )
        out.append(p)
    return out


def test_lab_measurement_error_changes_values() -> None:
    patients = _patients(50)
    originals = [p.biomarkers.get("hba1c_pct") for p in patients]
    add_lab_measurement_error(patients, seed=42)
    perturbed = [p.biomarkers.get("hba1c_pct") for p in patients]
    diffs = np.array(perturbed) - np.array(originals)
    # Some movement but bounded
    assert np.any(diffs != 0)
    assert np.max(np.abs(diffs)) < 1.0


def test_self_report_bias_underestimates_more_at_higher_bmi() -> None:
    rng = np.random.default_rng(0)
    lean = np.mean([add_self_report_bias(2200, bmi=22, rng=rng) for _ in range(200)])
    obese = np.mean([add_self_report_bias(2200, bmi=40, rng=rng) for _ in range(200)])
    assert obese < lean  # higher BMI under-reports more


def test_mcar_missing_creates_nans() -> None:
    df = pd.DataFrame({"a": np.arange(100), "b": np.arange(100) * 2})
    out = inject_mcar_missing(df, ["a"], fraction=0.3, seed=1)
    n_nan = out["a"].isna().sum()
    assert 15 < n_nan < 45


def test_mar_missing_depends_on_covariate() -> None:
    df = pd.DataFrame({
        "age": np.linspace(20, 80, 200),
        "ldl": np.random.default_rng(0).normal(120, 15, 200),
    })
    out = inject_mar_missing(df, ["ldl"], depends_on="age", fraction=0.3, seed=2)
    # Older patients more likely missing
    missing_mask = out["ldl"].isna()
    assert df.loc[missing_mask, "age"].mean() > df.loc[~missing_mask, "age"].mean()


def test_mnar_missing_concentrates_on_high_values() -> None:
    df = pd.DataFrame({"sbp": np.random.default_rng(0).normal(130, 20, 200)})
    out = inject_mnar_missing(df, ["sbp"], fraction=0.30, high_value_bias=True, seed=3)
    missing_mask = out["sbp"].isna()
    observed_high = df.loc[missing_mask, "sbp"].mean()
    overall = df["sbp"].mean()
    assert observed_high > overall
