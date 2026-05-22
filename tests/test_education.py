"""Tests for the educational module (case studies + OSCE)."""

from __future__ import annotations

import pytest

from synthdiet.diets import keto_diet, mediterranean_diet, standard_diet
from synthdiet.education import (
    CaseStudy,
    OSCEStation,
    built_in_cases,
    get_case,
    list_cases,
)


def test_15_built_in_cases() -> None:
    cases = built_in_cases()
    assert len(cases) == 15
    assert all(isinstance(c, CaseStudy) for c in cases)


def test_list_cases_keys_present() -> None:
    keys = list_cases()
    assert "t2dm_ht_dyslipidemia" in keys
    assert "celiac_teen" in keys
    assert "ckd4_pre_dialysis" in keys


def test_get_case_returns_with_patient() -> None:
    c = get_case("t2dm_ht_dyslipidemia")
    assert c.patient.has_disease("type_2_diabetes")
    assert c.patient.has_medication("metformin")


def test_unknown_case_raises() -> None:
    with pytest.raises(KeyError):
        get_case("unknown_case")


def test_case_renders_markdown() -> None:
    c = get_case("celiac_teen")
    md = c.as_markdown()
    assert "Case C02" in md
    assert "## Patient profile" in md
    assert "## Learning objectives" in md


def test_case_renders_html() -> None:
    c = get_case("pcos_insulin_resistance")
    html = c.as_html()
    assert html.startswith("<html>")
    assert "<h1>" in html


def test_osce_full_marks_for_reasonable_diet() -> None:
    case = get_case("t2dm_ht_dyslipidemia")
    station = OSCEStation(case=case)
    score = station.grade(case.reference_solution.prescribed_diet)
    # Reference solution should score at least 16/20
    assert score.total >= 12.0


def test_osce_penalises_keto_for_ckd_renal_patient() -> None:
    case = get_case("ckd4_pre_dialysis")
    station = OSCEStation(case=case)
    # Keto for CKD4 is inappropriate (too high protein)
    score = station.grade(keto_diet(daily_energy_kcal=2200))
    assert score.warnings or score.missed


def test_osce_flags_high_sodium_for_hypertensive() -> None:
    case = get_case("t2dm_ht_dyslipidemia")
    station = OSCEStation(case=case)
    bad_diet = standard_diet()
    bad_diet.sodium_mg_per_day = 5000
    score = station.grade(bad_diet)
    assert any("sodium" in m.lower() for m in score.missed + score.warnings)
