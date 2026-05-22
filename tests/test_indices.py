"""Tests for the diet-quality indices."""

from __future__ import annotations

import pytest

from synthdiet.diets import (
    dash_diet,
    diabetic_diet,
    keto_diet,
    mediterranean_diet,
    standard_diet,
    vegan_diet,
)
from synthdiet.indices import (
    AHEI2010,
    DASHScore,
    DII,
    HEI2020,
    INDEX_REGISTRY,
    MEDAS,
    PHDI,
    compute_all_indices,
)


def test_registry_complete() -> None:
    assert set(INDEX_REGISTRY) == {"hei_2020", "ahei_2010", "medas", "dash", "phdi", "dii"}


def test_hei_returns_score_in_valid_range() -> None:
    s = HEI2020().score(mediterranean_diet())
    assert 0 <= s.total <= s.max_total
    assert len(s.components) > 5


def test_medas_higher_for_mediterranean_than_standard() -> None:
    med = MEDAS().score(mediterranean_diet()).total
    std = MEDAS().score(standard_diet()).total
    assert med > std


def test_dash_score_higher_for_dash_than_keto() -> None:
    d = DASHScore().score(dash_diet()).total
    k = DASHScore().score(keto_diet()).total
    assert d > k


def test_ahei_higher_for_mediterranean_than_standard() -> None:
    med = AHEI2010().score(mediterranean_diet()).total
    std = AHEI2010().score(standard_diet()).total
    assert med > std


def test_phdi_favours_plant_based() -> None:
    vegan = PHDI().score(vegan_diet()).total
    standard = PHDI().score(standard_diet()).total
    assert vegan > standard


def test_dii_mediterranean_less_inflammatory_than_standard() -> None:
    med = DII().score(mediterranean_diet()).total
    std = DII().score(standard_diet()).total
    assert med < std  # DII: lower = more anti-inflammatory


def test_compute_all_indices_returns_all() -> None:
    result = compute_all_indices(mediterranean_diet())
    assert set(result) == {"hei_2020", "ahei_2010", "medas", "dash", "phdi", "dii"}
    for score in result.values():
        assert score.total is not None


def test_pretty_string() -> None:
    s = MEDAS().score(mediterranean_diet())
    text = s.pretty()
    assert "MEDAS" in text
    assert "/" in text


def test_diabetic_diet_scores_reasonably() -> None:
    s = AHEI2010().score(diabetic_diet())
    assert s.total > 30  # diabetic diet shouldn't be terrible
