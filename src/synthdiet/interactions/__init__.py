"""Drug-nutrient and drug-food interactions.

Adds a :class:`Medication` data class plus a registry of clinically important
interactions used by the simulation engine to flag safety concerns and adjust
biomarkers (e.g. metformin-induced B12 depletion).
"""

from synthdiet.interactions.medications import (
    DrugInteraction,
    Medication,
    apply_medication_effects,
    summarise_warnings,
)
from synthdiet.interactions.registry import (
    INTERACTION_REGISTRY,
    available_medications,
    get_medication,
)

__all__ = [
    "DrugInteraction",
    "INTERACTION_REGISTRY",
    "Medication",
    "apply_medication_effects",
    "available_medications",
    "get_medication",
    "summarise_warnings",
]
