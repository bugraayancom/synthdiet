"""Registry of all built-in diseases for name-based look-ups."""

from __future__ import annotations

from typing import Dict, List, Type

from synthdiet.diseases.base import Disease

DISEASE_REGISTRY: Dict[str, Type[Disease]] = {}


def register(cls: Type[Disease]) -> Type[Disease]:
    """Decorator that registers a disease subclass under its canonical name."""
    DISEASE_REGISTRY[cls.name.lower()] = cls
    return cls


def get_disease(name: str) -> Type[Disease]:
    """Look up a disease class by case-insensitive name."""
    try:
        return DISEASE_REGISTRY[name.lower()]
    except KeyError as exc:
        raise KeyError(
            f"Unknown disease: {name!r}. Known: {sorted(DISEASE_REGISTRY)}"
        ) from exc


def available_diseases() -> List[str]:
    """List all registered disease names."""
    return sorted(DISEASE_REGISTRY)
