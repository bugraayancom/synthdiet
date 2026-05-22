"""Base classes shared by every disease."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Set

if TYPE_CHECKING:
    from synthdiet.diets.base import DietPlan
    from synthdiet.patients.patient import Patient


@dataclass
class NutritionalConstraints:
    """Soft and hard dietary limits associated with a disease."""

    # Macronutrient targets are expressed as a fraction of total daily energy
    # (e.g. ``0.45`` means 45% of kcal). ``None`` means "no recommendation".
    carbohydrate_pct_range: Optional[tuple] = None
    protein_pct_range: Optional[tuple] = None
    fat_pct_range: Optional[tuple] = None
    saturated_fat_pct_max: Optional[float] = None
    added_sugar_pct_max: Optional[float] = None

    # Absolute daily limits in grams / milligrams.
    sodium_mg_max: Optional[float] = None
    potassium_mg_max: Optional[float] = None
    phosphorus_mg_max: Optional[float] = None
    fiber_g_min: Optional[float] = None
    cholesterol_mg_max: Optional[float] = None
    fluid_ml_max: Optional[float] = None

    # Whole-food restrictions.
    forbidden_foods: Set[str] = field(default_factory=set)
    limited_foods: Set[str] = field(default_factory=set)
    encouraged_foods: Set[str] = field(default_factory=set)

    # Free-form notes (printed by reports).
    notes: List[str] = field(default_factory=list)

    def merge(self, other: "NutritionalConstraints") -> "NutritionalConstraints":
        """Combine two sets of constraints, keeping the stricter value."""
        return NutritionalConstraints(
            carbohydrate_pct_range=_tighter_range(
                self.carbohydrate_pct_range, other.carbohydrate_pct_range
            ),
            protein_pct_range=_tighter_range(
                self.protein_pct_range, other.protein_pct_range
            ),
            fat_pct_range=_tighter_range(self.fat_pct_range, other.fat_pct_range),
            saturated_fat_pct_max=_min_optional(
                self.saturated_fat_pct_max, other.saturated_fat_pct_max
            ),
            added_sugar_pct_max=_min_optional(
                self.added_sugar_pct_max, other.added_sugar_pct_max
            ),
            sodium_mg_max=_min_optional(self.sodium_mg_max, other.sodium_mg_max),
            potassium_mg_max=_min_optional(
                self.potassium_mg_max, other.potassium_mg_max
            ),
            phosphorus_mg_max=_min_optional(
                self.phosphorus_mg_max, other.phosphorus_mg_max
            ),
            fiber_g_min=_max_optional(self.fiber_g_min, other.fiber_g_min),
            cholesterol_mg_max=_min_optional(
                self.cholesterol_mg_max, other.cholesterol_mg_max
            ),
            fluid_ml_max=_min_optional(self.fluid_ml_max, other.fluid_ml_max),
            forbidden_foods=set(self.forbidden_foods) | set(other.forbidden_foods),
            limited_foods=set(self.limited_foods) | set(other.limited_foods),
            encouraged_foods=set(self.encouraged_foods) | set(other.encouraged_foods),
            notes=list(self.notes) + list(other.notes),
        )


def _min_optional(a: Optional[float], b: Optional[float]) -> Optional[float]:
    if a is None:
        return b
    if b is None:
        return a
    return min(a, b)


def _max_optional(a: Optional[float], b: Optional[float]) -> Optional[float]:
    if a is None:
        return b
    if b is None:
        return a
    return max(a, b)


def _tighter_range(a: Optional[tuple], b: Optional[tuple]) -> Optional[tuple]:
    if a is None:
        return b
    if b is None:
        return a
    return (max(a[0], b[0]), min(a[1], b[1]))


class Disease:
    """Abstract base class for all diseases.

    Subclasses should set :attr:`name` and ``severity`` defaults and override
    :meth:`nutritional_constraints` (returning a
    :class:`NutritionalConstraints` instance) and :meth:`apply_biomarker_modifiers`.
    """

    name: str = "disease"
    icd10: Optional[str] = None
    category: str = "general"
    default_severity: str = "moderate"
    severity_levels: tuple = ("mild", "moderate", "severe")

    def __init__(
        self,
        severity: Optional[str] = None,
        onset_age: Optional[int] = None,
        notes: str = "",
        **details: Any,
    ) -> None:
        self.severity = severity or self.default_severity
        if self.severity not in self.severity_levels:
            raise ValueError(
                f"severity must be one of {self.severity_levels}, got {severity!r}"
            )
        self.onset_age = onset_age
        self.notes = notes
        self.details: Dict[str, Any] = dict(details)

    # Lifecycle hooks ------------------------------------------------------
    def on_attach(self, patient: "Patient") -> None:
        """Called automatically when the disease is added to a :class:`Patient`.

        Default behaviour: nudge a few baseline biomarkers using
        :meth:`apply_biomarker_modifiers`.
        """
        modifiers = self.apply_biomarker_modifiers(patient)
        if modifiers:
            for key, delta in modifiers.items():
                current = patient.biomarkers.get(key)
                if current is None:
                    patient.biomarkers.set(key, float(delta))
                else:
                    patient.biomarkers.set(key, float(current + delta))

    # Hooks meant to be overridden ----------------------------------------
    def nutritional_constraints(self, patient: "Patient") -> NutritionalConstraints:
        """Return dietary limits/recommendations for this patient."""
        return NutritionalConstraints()

    def apply_biomarker_modifiers(self, patient: "Patient") -> Mapping[str, float]:
        """Return a mapping of biomarker -> additive offset applied at onset."""
        return {}

    def response_to_diet(
        self,
        patient: "Patient",
        diet: "DietPlan",
        duration_weeks: int,
    ) -> Dict[str, float]:
        """Return projected biomarker deltas after ``duration_weeks`` on ``diet``.

        Subclasses may override this to model disease-specific responses
        (e.g. HbA1c lowering on a low-carb diet for type 2 diabetes).
        Default: no specific response.
        """
        return {}

    # Reporting ------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "icd10": self.icd10,
            "category": self.category,
            "severity": self.severity,
            "onset_age": self.onset_age,
            "notes": self.notes,
            "details": dict(self.details),
        }

    def __repr__(self) -> str:  # pragma: no cover - cosmetic
        return f"{self.__class__.__name__}(severity={self.severity!r})"
