"""Small input validators used by data classes across the library."""

from __future__ import annotations

from typing import Optional


def ensure_positive(value: float, name: str) -> float:
    if value <= 0:
        raise ValueError(f"{name} must be > 0, got {value!r}")
    return value


def ensure_non_negative(value: float, name: str) -> float:
    if value < 0:
        raise ValueError(f"{name} must be >= 0, got {value!r}")
    return value


def ensure_in_range(
    value: float,
    name: str,
    *,
    minimum: Optional[float] = None,
    maximum: Optional[float] = None,
) -> float:
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be >= {minimum}, got {value!r}")
    if maximum is not None and value > maximum:
        raise ValueError(f"{name} must be <= {maximum}, got {value!r}")
    return value
