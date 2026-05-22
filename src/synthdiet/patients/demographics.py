"""Demographic attributes of a synthetic patient."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from synthdiet.utils.validators import ensure_in_range


class Sex(str, Enum):
    """Biological sex used for energy-expenditure equations and lab references."""

    FEMALE = "female"
    MALE = "male"
    INTERSEX = "intersex"


@dataclass
class Demographics:
    """Patient demographics."""

    age: int
    sex: Sex
    ethnicity: Optional[str] = None
    pregnancy_trimester: Optional[int] = None  # 1, 2, or 3 (None if not pregnant)
    lactating: bool = False
    country: Optional[str] = None
    occupation: Optional[str] = None
    notes: str = field(default="")

    def __post_init__(self) -> None:
        ensure_in_range(self.age, "age", minimum=0, maximum=120)
        if not isinstance(self.sex, Sex):
            self.sex = Sex(self.sex)
        if self.pregnancy_trimester is not None:
            ensure_in_range(
                self.pregnancy_trimester,
                "pregnancy_trimester",
                minimum=1,
                maximum=3,
            )
            if self.sex is Sex.MALE:
                raise ValueError("pregnancy_trimester cannot be set when sex is male")

    @property
    def is_pediatric(self) -> bool:
        return self.age < 18

    @property
    def is_geriatric(self) -> bool:
        return self.age >= 65
