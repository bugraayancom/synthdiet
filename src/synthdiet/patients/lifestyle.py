"""Lifestyle attributes that influence energy needs and disease modifiers."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from synthdiet.utils.constants import ACTIVITY_FACTORS


class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHT = "light"
    MODERATE = "moderate"
    ACTIVE = "active"
    VERY_ACTIVE = "very_active"
    ATHLETE = "athlete"

    @property
    def factor(self) -> float:
        return ACTIVITY_FACTORS[self.value]


class SmokingStatus(str, Enum):
    NEVER = "never"
    FORMER = "former"
    CURRENT = "current"


@dataclass
class Lifestyle:
    activity_level: ActivityLevel = ActivityLevel.SEDENTARY
    smoking_status: SmokingStatus = SmokingStatus.NEVER
    alcohol_units_per_week: float = 0.0
    sleep_hours_per_night: float = 7.5
    stress_level: int = 3  # 1 (low) to 5 (high)
    dietary_preferences: List[str] = field(default_factory=list)
    food_allergies: List[str] = field(default_factory=list)
    food_intolerances: List[str] = field(default_factory=list)
    cultural_restrictions: List[str] = field(default_factory=list)
    typical_meals_per_day: int = 3
    cooking_skill: Optional[str] = None  # "low", "medium", "high"

    def __post_init__(self) -> None:
        if not isinstance(self.activity_level, ActivityLevel):
            self.activity_level = ActivityLevel(self.activity_level)
        if not isinstance(self.smoking_status, SmokingStatus):
            self.smoking_status = SmokingStatus(self.smoking_status)
        if not (1 <= self.stress_level <= 5):
            raise ValueError("stress_level must be in the inclusive range [1, 5]")
        if self.alcohol_units_per_week < 0:
            raise ValueError("alcohol_units_per_week must be >= 0")
