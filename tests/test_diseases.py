"""Tests for the disease registry and constraints."""

from __future__ import annotations

import pytest

from synthdiet import (
    Anthropometrics,
    Demographics,
    Patient,
    Sex,
    available_diseases,
    get_disease,
)
from synthdiet.diseases import ChronicKidneyDisease, Cirrhosis, LactoseIntolerance


def _patient() -> Patient:
    return Patient(
        demographics=Demographics(age=60, sex=Sex.FEMALE),
        anthropometrics=Anthropometrics(height_cm=165, weight_kg=78),
    )


def test_registry_contains_core_diseases() -> None:
    names = set(available_diseases())
    expected = {
        "type_1_diabetes",
        "type_2_diabetes",
        "prediabetes",
        "hypertension",
        "dyslipidemia",
        "nafld",
        "chronic_kidney_disease",
        "celiac_disease",
        "ibs",
        "hypothyroidism",
        "hyperthyroidism",
        "pcos",
        "obesity",
        "gout",
    }
    assert expected.issubset(names)


def test_get_disease_case_insensitive() -> None:
    cls = get_disease("Type_2_Diabetes")
    assert cls.__name__ == "Type2Diabetes"


def test_unknown_disease_raises() -> None:
    with pytest.raises(KeyError):
        get_disease("xyz_disease")


def test_ckd_stage_tunes_constraints() -> None:
    p = _patient()
    disease = ChronicKidneyDisease(stage=4)
    p.add_disease(disease)
    constraints = disease.nutritional_constraints(p)
    assert constraints.protein_pct_range is not None
    assert constraints.protein_pct_range[1] <= 0.15
    assert constraints.sodium_mg_max is not None
    assert constraints.potassium_mg_max is not None


def test_cirrhosis_class_c_more_restrictive() -> None:
    p = _patient()
    mild = Cirrhosis(child_pugh_class="A")
    severe = Cirrhosis(child_pugh_class="C", ascites=True)
    cm = mild.nutritional_constraints(p)
    cs = severe.nutritional_constraints(p)
    assert cs.sodium_mg_max <= cm.sodium_mg_max
    assert cs.fluid_ml_max is not None and cm.fluid_ml_max is None


def test_lactose_intolerance_lists_dairy() -> None:
    p = _patient()
    d = LactoseIntolerance()
    p.add_disease(d)
    constraints = d.nutritional_constraints(p)
    assert "milk" in constraints.limited_foods
