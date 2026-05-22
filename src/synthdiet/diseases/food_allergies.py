"""Food allergies and intolerances."""

from __future__ import annotations

from typing import TYPE_CHECKING

from synthdiet.diseases.base import Disease, NutritionalConstraints
from synthdiet.diseases.registry import register

if TYPE_CHECKING:
    from synthdiet.patients.patient import Patient


class _AllergyBase(Disease):
    category = "allergy"
    forbidden: set = set()
    avoid_notes: tuple = ()

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            forbidden_foods=set(self.forbidden),
            notes=list(self.avoid_notes),
        )


@register
class PeanutAllergy(_AllergyBase):
    name = "peanut_allergy"
    icd10 = "T78.01"
    forbidden = {"peanut", "peanut_butter", "peanut_oil"}
    avoid_notes = ("Strict avoidance; check labels for cross-contamination warnings.",)


@register
class TreeNutAllergy(_AllergyBase):
    name = "tree_nut_allergy"
    icd10 = "T78.05"
    forbidden = {"almond", "walnut", "cashew", "pecan", "pistachio", "hazelnut", "brazil_nut"}
    avoid_notes = ("Carry epinephrine auto-injector; cross-reactivity common between tree nuts.",)


@register
class EggAllergy(_AllergyBase):
    name = "egg_allergy"
    icd10 = "T78.07"
    forbidden = {"egg", "mayonnaise", "egg_white", "egg_yolk"}
    avoid_notes = ("Check vaccine ingredients; consider egg-replacer for baking.",)


@register
class SoyAllergy(_AllergyBase):
    name = "soy_allergy"
    icd10 = "T78.08"
    forbidden = {"soy", "soy_milk", "tofu", "edamame", "soy_sauce", "tempeh"}
    avoid_notes = ("Soy lecithin is generally tolerated by most soy-allergic patients.",)


@register
class LactoseIntolerance(Disease):
    name = "lactose_intolerance"
    icd10 = "E73"
    category = "allergy"
    default_severity = "moderate"

    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        return NutritionalConstraints(
            limited_foods={"milk", "soft_cheese", "ice_cream"},
            encouraged_foods={"lactose_free_milk", "hard_cheese", "fortified_plant_milk"},
            notes=[
                "Most tolerate up to 12 g lactose with meals.",
                "Ensure calcium intake from non-dairy sources (≥1000 mg/day).",
            ],
        )
