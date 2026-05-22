"""Macronutrient and micronutrient definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Mapping

MACRONUTRIENTS = (
    "protein_g",
    "carbohydrate_g",
    "fat_g",
    "saturated_fat_g",
    "monounsaturated_fat_g",
    "polyunsaturated_fat_g",
    "trans_fat_g",
    "fiber_g",
    "added_sugar_g",
    "alcohol_g",
    "water_ml",
)

MICRONUTRIENTS = (
    # Minerals (mg unless noted)
    "sodium_mg",
    "potassium_mg",
    "calcium_mg",
    "magnesium_mg",
    "iron_mg",
    "zinc_mg",
    "copper_mg",
    "selenium_ug",
    "iodine_ug",
    "phosphorus_mg",
    "chromium_ug",
    # Vitamins
    "vitamin_a_ug",
    "vitamin_c_mg",
    "vitamin_d_iu",
    "vitamin_e_mg",
    "vitamin_k_ug",
    "thiamin_mg",
    "riboflavin_mg",
    "niacin_mg",
    "vitamin_b6_mg",
    "folate_ug",
    "vitamin_b12_ug",
    "choline_mg",
)


@dataclass
class NutrientProfile:
    """A bag of nutrient values keyed by canonical nutrient name.

    Two profiles can be added together to combine the nutrient contributions
    of multiple foods or meals.
    """

    energy_kcal: float = 0.0
    nutrients: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.nutrients = {k: float(v) for k, v in self.nutrients.items()}

    def get(self, name: str, default: float = 0.0) -> float:
        return self.nutrients.get(name, default)

    def set(self, name: str, value: float) -> None:
        self.nutrients[name] = float(value)

    def scale(self, factor: float) -> "NutrientProfile":
        return NutrientProfile(
            energy_kcal=self.energy_kcal * factor,
            nutrients={k: v * factor for k, v in self.nutrients.items()},
        )

    def __add__(self, other: "NutrientProfile") -> "NutrientProfile":
        if not isinstance(other, NutrientProfile):
            return NotImplemented
        merged_keys = set(self.nutrients) | set(other.nutrients)
        return NutrientProfile(
            energy_kcal=self.energy_kcal + other.energy_kcal,
            nutrients={k: self.get(k) + other.get(k) for k in merged_keys},
        )

    def __radd__(self, other: object) -> "NutrientProfile":
        if other == 0:
            return self
        return self.__add__(other)  # type: ignore[arg-type]

    def as_dict(self) -> Dict[str, float]:
        return {"energy_kcal": self.energy_kcal, **self.nutrients}

    @classmethod
    def from_dict(cls, data: Mapping[str, float]) -> "NutrientProfile":
        nutrients = {k: float(v) for k, v in data.items() if k != "energy_kcal"}
        return cls(energy_kcal=float(data.get("energy_kcal", 0.0)), nutrients=nutrients)
