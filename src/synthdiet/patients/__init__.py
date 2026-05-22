"""Synthetic patient data model.

The :class:`Patient` class is the central object manipulated by everything
else in the library. It bundles demographics, anthropometrics, lifestyle
information, lab biomarkers, and a list of :class:`~synthdiet.diseases.Disease`
diagnoses.
"""

from synthdiet.patients.anthropometrics import Anthropometrics
from synthdiet.patients.biomarkers import Biomarkers
from synthdiet.patients.demographics import Demographics, Sex
from synthdiet.patients.lifestyle import ActivityLevel, Lifestyle, SmokingStatus
from synthdiet.patients.patient import Patient

__all__ = [
    "ActivityLevel",
    "Anthropometrics",
    "Biomarkers",
    "Demographics",
    "Lifestyle",
    "Patient",
    "Sex",
    "SmokingStatus",
]
