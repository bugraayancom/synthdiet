"""Diet quality indices (HEI-2020, AHEI-2010, MEDAS, DASH, PHDI, DII).

Every index implements the :class:`DietQualityIndex` protocol with a single
``score(diet, patient=None)`` method returning an :class:`IndexScore`. Indices
operate on either a food-based :class:`~synthdiet.DietPlan` (using the meal
breakdown) or a target-based plan (using macro/sodium/fibre fields).
"""

from synthdiet.indices.ahei_2010 import AHEI2010
from synthdiet.indices.base import DietQualityIndex, IndexComponent, IndexScore
from synthdiet.indices.dash_score import DASHScore
from synthdiet.indices.dii import DII
from synthdiet.indices.hei_2020 import HEI2020
from synthdiet.indices.medas import MEDAS
from synthdiet.indices.phdi import PHDI

INDEX_REGISTRY = {
    "hei_2020": HEI2020,
    "ahei_2010": AHEI2010,
    "medas": MEDAS,
    "dash": DASHScore,
    "phdi": PHDI,
    "dii": DII,
}


def compute_all_indices(diet, patient=None):
    """Compute every registered index and return a dict of scores."""
    return {name: cls().score(diet, patient) for name, cls in INDEX_REGISTRY.items()}


__all__ = [
    "AHEI2010",
    "DASHScore",
    "DII",
    "DietQualityIndex",
    "HEI2020",
    "INDEX_REGISTRY",
    "IndexComponent",
    "IndexScore",
    "MEDAS",
    "PHDI",
    "compute_all_indices",
]
