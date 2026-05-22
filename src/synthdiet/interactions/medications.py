"""Medication and interaction data structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Iterable, List, Mapping, Optional, Sequence, Set

if TYPE_CHECKING:
    from synthdiet.patients.patient import Patient


@dataclass
class DrugInteraction:
    """A clinically documented drug-nutrient or drug-food interaction."""

    nutrient: str
    direction: str  # "depletes", "increases", "competes_absorption"
    monthly_biomarker_delta: float = 0.0
    biomarker: Optional[str] = None
    severity: str = "moderate"  # "mild", "moderate", "severe"
    recommendation: str = ""
    forbid_foods: Set[str] = field(default_factory=set)
    timing_advice: str = ""


@dataclass
class Medication:
    """A medication a patient is currently taking."""

    name: str
    drug_class: str
    daily_dose_mg: Optional[float] = None
    interactions: List[DrugInteraction] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "drug_class": self.drug_class,
            "daily_dose_mg": self.daily_dose_mg,
            "interactions": [vars(i) for i in self.interactions],
            "notes": self.notes,
        }


def apply_medication_effects(
    patient: "Patient",
    weeks_elapsed: int = 1,
) -> List[str]:
    """Apply biomarker drift caused by ``patient.medications``.

    Returns a list of safety-concern strings for the simulator to surface.
    Operates *in place* on ``patient.biomarkers``.
    """
    warnings: List[str] = []
    months_elapsed = weeks_elapsed / 4.33
    for med in getattr(patient, "medications", []):
        for interaction in med.interactions:
            if interaction.biomarker and interaction.monthly_biomarker_delta:
                current = patient.biomarkers.get(interaction.biomarker) or 0.0
                patient.biomarkers.set(
                    interaction.biomarker,
                    current + interaction.monthly_biomarker_delta * months_elapsed,
                )
            if interaction.severity in {"severe", "moderate"} and interaction.recommendation:
                warnings.append(
                    f"[{med.name}] {interaction.recommendation}"
                )
    return warnings


def summarise_warnings(
    patient: "Patient",
    diet_foods: Iterable[str] = (),
) -> List[str]:
    """Return a list of warnings for foods that conflict with the patient's
    medications (e.g. grapefruit + statins, leafy greens + warfarin)."""
    warnings: List[str] = []
    food_set = {f.lower() for f in diet_foods}
    for med in getattr(patient, "medications", []):
        for interaction in med.interactions:
            collision = food_set & {f.lower() for f in interaction.forbid_foods}
            if collision:
                warnings.append(
                    f"[{med.name}] avoid {sorted(collision)}: {interaction.recommendation}"
                )
            if interaction.timing_advice:
                warnings.append(
                    f"[{med.name}] timing: {interaction.timing_advice}"
                )
    return warnings
