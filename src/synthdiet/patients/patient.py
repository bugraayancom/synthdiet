"""The central :class:`Patient` aggregate."""

from __future__ import annotations

import copy
import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional

from synthdiet.patients.anthropometrics import Anthropometrics
from synthdiet.patients.biomarkers import Biomarkers
from synthdiet.patients.demographics import Demographics, Sex
from synthdiet.patients.lifestyle import Lifestyle

if TYPE_CHECKING:  # avoid a circular import at runtime
    from synthdiet.diseases.base import Disease
    from synthdiet.interactions.medications import Medication


@dataclass
class Patient:
    """A complete synthetic patient profile.

    Patients are intentionally mutable so that the simulation engine can
    project anthropometric and biomarker changes over time.
    """

    demographics: Demographics
    anthropometrics: Anthropometrics
    lifestyle: Lifestyle = field(default_factory=Lifestyle)
    biomarkers: Biomarkers = field(default_factory=Biomarkers)
    diseases: List["Disease"] = field(default_factory=list)
    medications: List["Medication"] = field(default_factory=list)
    patient_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)

    # Convenience accessors ------------------------------------------------
    @property
    def age(self) -> int:
        return self.demographics.age

    @property
    def sex(self) -> Sex:
        return self.demographics.sex

    @property
    def weight_kg(self) -> float:
        return self.anthropometrics.weight_kg

    @property
    def height_cm(self) -> float:
        return self.anthropometrics.height_cm

    @property
    def bmi(self) -> float:
        return self.anthropometrics.bmi

    # Disease management ---------------------------------------------------
    def add_disease(self, disease: "Disease") -> None:
        self.diseases.append(disease)
        disease.on_attach(self)

    def remove_disease(self, name: str) -> Optional["Disease"]:
        for i, d in enumerate(self.diseases):
            if d.name == name:
                return self.diseases.pop(i)
        return None

    def has_disease(self, name: str) -> bool:
        return any(d.name == name for d in self.diseases)

    def disease_names(self) -> List[str]:
        return [d.name for d in self.diseases]

    # Medication management ------------------------------------------------
    def add_medication(self, medication: "Medication") -> None:
        self.medications.append(medication)

    def remove_medication(self, name: str) -> Optional["Medication"]:
        for i, m in enumerate(self.medications):
            if m.name == name:
                return self.medications.pop(i)
        return None

    def has_medication(self, name: str) -> bool:
        return any(m.name == name for m in self.medications)

    def medication_names(self) -> List[str]:
        return [m.name for m in self.medications]

    # Cloning --------------------------------------------------------------
    def clone(self, new_id: bool = True) -> "Patient":
        """Return a deep copy of this patient, optionally with a fresh id."""
        copied = copy.deepcopy(self)
        if new_id:
            copied.patient_id = str(uuid.uuid4())
        return copied

    # Serialisation --------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "patient_id": self.patient_id,
            "demographics": {
                "age": self.demographics.age,
                "sex": self.demographics.sex.value,
                "ethnicity": self.demographics.ethnicity,
                "pregnancy_trimester": self.demographics.pregnancy_trimester,
                "lactating": self.demographics.lactating,
                "country": self.demographics.country,
                "occupation": self.demographics.occupation,
                "notes": self.demographics.notes,
            },
            "anthropometrics": {
                "height_cm": self.anthropometrics.height_cm,
                "weight_kg": self.anthropometrics.weight_kg,
                "bmi": self.anthropometrics.bmi,
                "bmi_category": self.anthropometrics.bmi_category,
                "waist_cm": self.anthropometrics.waist_cm,
                "hip_cm": self.anthropometrics.hip_cm,
                "body_fat_pct": self.anthropometrics.body_fat_pct,
            },
            "lifestyle": {
                "activity_level": self.lifestyle.activity_level.value,
                "smoking_status": self.lifestyle.smoking_status.value,
                "alcohol_units_per_week": self.lifestyle.alcohol_units_per_week,
                "sleep_hours_per_night": self.lifestyle.sleep_hours_per_night,
                "stress_level": self.lifestyle.stress_level,
                "dietary_preferences": list(self.lifestyle.dietary_preferences),
                "food_allergies": list(self.lifestyle.food_allergies),
                "food_intolerances": list(self.lifestyle.food_intolerances),
            },
            "biomarkers": dict(self.biomarkers.values),
            "diseases": [d.to_dict() for d in self.diseases],
            "medications": [m.to_dict() for m in self.medications],
            "metadata": dict(self.metadata),
        }

    def summary(self) -> str:
        """Return a short human-readable summary, useful for debugging."""
        disease_str = ", ".join(self.disease_names()) or "no recorded diagnoses"
        return (
            f"Patient {self.patient_id[:8]} | "
            f"{self.demographics.age}y {self.demographics.sex.value} | "
            f"BMI {self.anthropometrics.bmi:.1f} ({self.anthropometrics.bmi_category}) | "
            f"{disease_str}"
        )

    # Bulk operations ------------------------------------------------------
    @classmethod
    def from_dicts(cls, records: Iterable[Dict[str, Any]]) -> List["Patient"]:
        """Build a list of :class:`Patient` objects from plain dictionaries."""
        return [_patient_from_dict(rec) for rec in records]


def _patient_from_dict(record: Dict[str, Any]) -> Patient:
    demo = record["demographics"]
    anthro = record["anthropometrics"]
    life = record.get("lifestyle", {})
    return Patient(
        demographics=Demographics(
            age=demo["age"],
            sex=Sex(demo["sex"]),
            ethnicity=demo.get("ethnicity"),
            pregnancy_trimester=demo.get("pregnancy_trimester"),
            lactating=demo.get("lactating", False),
            country=demo.get("country"),
            occupation=demo.get("occupation"),
            notes=demo.get("notes", ""),
        ),
        anthropometrics=Anthropometrics(
            height_cm=anthro["height_cm"],
            weight_kg=anthro["weight_kg"],
            waist_cm=anthro.get("waist_cm"),
            hip_cm=anthro.get("hip_cm"),
            body_fat_pct=anthro.get("body_fat_pct"),
        ),
        lifestyle=Lifestyle(**life) if life else Lifestyle(),
        biomarkers=Biomarkers(values=dict(record.get("biomarkers", {}))),
        patient_id=record.get("patient_id", str(uuid.uuid4())),
        metadata=dict(record.get("metadata", {})),
    )
