"""Physiological and nutritional constants used throughout the library.

All values follow widely cited dietetic conventions. They are intentionally
conservative defaults; advanced users can override them at any time.
"""

from __future__ import annotations

from typing import Mapping

# Atwater factors (kcal per gram of macronutrient).
KCAL_PER_GRAM: Mapping[str, float] = {
    "protein": 4.0,
    "carbohydrate": 4.0,
    "fat": 9.0,
    "alcohol": 7.0,
    "fiber": 2.0,  # mixed-fibre approximation
}

# Physical Activity Level (PAL) multipliers commonly used with the
# Mifflin-St Jeor / Harris-Benedict equations.
ACTIVITY_FACTORS: Mapping[str, float] = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
    "athlete": 2.1,
}

# Approximate energy value of stored body tissue. Used when projecting
# weight change from cumulative energy balance.
KCAL_PER_KG_BODY_FAT: float = 7700.0

# Default daily fluid requirement multipliers (mL per kcal consumed).
ML_FLUID_PER_KCAL: float = 1.0

# Conversion helpers
LBS_PER_KG: float = 2.20462
INCHES_PER_CM: float = 0.393701
