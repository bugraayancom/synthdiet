"""Clinical laboratory biomarkers tracked for each patient.

Reference ranges are approximate adult values from common clinical sources;
they are used to drive disease modifiers and to evaluate diet outcomes.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Mapping, Optional

# Reference ranges expressed as (low, high). ``None`` means open-ended.
ADULT_REFERENCE_RANGES: Mapping[str, tuple] = {
    # Glycaemic
    "fasting_glucose_mg_dl": (70.0, 99.0),
    "hba1c_pct": (4.0, 5.6),
    "fasting_insulin_uIU_ml": (2.6, 24.9),
    "homa_ir": (0.5, 1.9),
    # Lipids
    "total_cholesterol_mg_dl": (None, 200.0),
    "ldl_mg_dl": (None, 100.0),
    "hdl_mg_dl": (40.0, None),
    "triglycerides_mg_dl": (None, 150.0),
    # Renal
    "creatinine_mg_dl": (0.6, 1.3),
    "egfr_ml_min_1_73m2": (90.0, None),
    "bun_mg_dl": (7.0, 20.0),
    "uric_acid_mg_dl": (3.5, 7.2),
    # Liver
    "alt_u_l": (7.0, 56.0),
    "ast_u_l": (10.0, 40.0),
    "ggt_u_l": (9.0, 48.0),
    "alk_phos_u_l": (44.0, 147.0),
    # Electrolytes
    "sodium_mmol_l": (135.0, 145.0),
    "potassium_mmol_l": (3.5, 5.1),
    "calcium_mg_dl": (8.6, 10.3),
    "phosphate_mg_dl": (2.5, 4.5),
    "magnesium_mg_dl": (1.7, 2.2),
    # Haematology / iron
    "hemoglobin_g_dl": (12.0, 17.5),
    "ferritin_ng_ml": (24.0, 336.0),
    "transferrin_saturation_pct": (15.0, 50.0),
    # Vitamins
    "vitamin_d_25oh_ng_ml": (30.0, 100.0),
    "vitamin_b12_pg_ml": (200.0, 900.0),
    "folate_ng_ml": (3.0, 17.0),
    # Inflammation / hormones
    "crp_mg_l": (None, 3.0),
    "tsh_uIU_ml": (0.4, 4.0),
    "free_t4_ng_dl": (0.8, 1.8),
    # Blood pressure (mmHg)
    "systolic_bp_mmhg": (90.0, 120.0),
    "diastolic_bp_mmhg": (60.0, 80.0),
}


@dataclass
class Biomarkers:
    """A flexible container for laboratory values.

    Values are stored in a dictionary keyed by canonical biomarker name. Use
    :meth:`set` / :meth:`get` for typed access or assign through :attr:`values`
    directly.
    """

    values: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.values = {str(k): float(v) for k, v in self.values.items()}

    # Mapping-style helpers ------------------------------------------------
    def get(self, name: str, default: Optional[float] = None) -> Optional[float]:
        return self.values.get(name, default)

    def set(self, name: str, value: float) -> None:
        self.values[name] = float(value)

    def update(self, mapping: Mapping[str, float]) -> None:
        self.values.update({k: float(v) for k, v in mapping.items()})

    def __contains__(self, name: object) -> bool:
        return name in self.values

    def __iter__(self) -> Iterable[str]:
        return iter(self.values)

    # Interpretation -------------------------------------------------------
    def is_within_reference(self, name: str) -> Optional[bool]:
        """Return True/False if value is within the reference range, else ``None``."""
        value = self.values.get(name)
        if value is None or name not in ADULT_REFERENCE_RANGES:
            return None
        low, high = ADULT_REFERENCE_RANGES[name]
        if low is not None and value < low:
            return False
        if high is not None and value > high:
            return False
        return True

    def abnormal(self) -> Dict[str, float]:
        """Return all stored biomarkers that fall outside their reference range."""
        return {k: v for k, v in self.values.items() if self.is_within_reference(k) is False}
