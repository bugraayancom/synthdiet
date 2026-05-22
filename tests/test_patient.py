"""Tests for the core Patient data model."""

from __future__ import annotations

import pytest

from synthdiet import (
    Anthropometrics,
    Biomarkers,
    Demographics,
    Lifestyle,
    Patient,
    Sex,
)
from synthdiet.diseases import Hypertension, Type2Diabetes


def make_patient() -> Patient:
    return Patient(
        demographics=Demographics(age=55, sex=Sex.MALE),
        anthropometrics=Anthropometrics(height_cm=178, weight_kg=92),
        lifestyle=Lifestyle(),
        biomarkers=Biomarkers(values={"hba1c_pct": 5.4}),
    )


def test_bmi_computed_correctly() -> None:
    p = make_patient()
    assert p.bmi == pytest.approx(92 / (1.78 ** 2), rel=1e-6)
    assert p.anthropometrics.bmi_category in {"overweight", "obesity_class_I"}


def test_adding_disease_updates_biomarkers() -> None:
    p = make_patient()
    p.add_disease(Type2Diabetes(severity="moderate"))
    assert p.has_disease("type_2_diabetes")
    assert p.biomarkers.get("hba1c_pct") > 5.4


def test_demographics_pregnancy_validation() -> None:
    with pytest.raises(ValueError):
        Demographics(age=30, sex=Sex.MALE, pregnancy_trimester=2)


def test_multiple_diseases_stack() -> None:
    p = make_patient()
    p.add_disease(Type2Diabetes(severity="mild"))
    p.add_disease(Hypertension(severity="mild"))
    assert set(p.disease_names()) == {"type_2_diabetes", "hypertension"}
    assert p.biomarkers.get("systolic_bp_mmhg") is not None


def test_clone_independent() -> None:
    p = make_patient()
    p.add_disease(Hypertension(severity="moderate"))
    twin = p.clone()
    twin.anthropometrics.weight_kg = 70
    assert p.anthropometrics.weight_kg == 92
    assert twin.patient_id != p.patient_id
