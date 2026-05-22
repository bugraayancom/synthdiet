"""Diet-evaluation metrics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List

import pandas as pd

from synthdiet.simulation.engine import SimulationResult


@dataclass
class DietEvaluation:
    """Structured outcomes from a single simulation."""

    patient_id: str
    diet_name: str
    duration_weeks: int
    weight_change_kg: float
    bmi_change: float
    biomarker_changes: Dict[str, float] = field(default_factory=dict)
    constraint_warnings: List[str] = field(default_factory=list)
    achieved_goals: List[str] = field(default_factory=list)
    safety_concerns: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "patient_id": self.patient_id,
            "diet_name": self.diet_name,
            "duration_weeks": self.duration_weeks,
            "weight_change_kg": self.weight_change_kg,
            "bmi_change": self.bmi_change,
            "biomarker_changes": dict(self.biomarker_changes),
            "constraint_warnings": list(self.constraint_warnings),
            "achieved_goals": list(self.achieved_goals),
            "safety_concerns": list(self.safety_concerns),
        }


def evaluate_simulation(
    result: SimulationResult,
    constraint_warnings: List[str] | None = None,
) -> DietEvaluation:
    """Compute outcome metrics for a finished simulation."""
    if not result.timeline:
        raise ValueError("simulation result has no timeline points")
    first = result.timeline[0]
    last = result.timeline[-1]
    biomarker_changes = {
        k: last.biomarkers.get(k, 0.0) - first.biomarkers.get(k, 0.0)
        for k in set(first.biomarkers) | set(last.biomarkers)
    }

    achieved: List[str] = []
    concerns: List[str] = []
    weight_change = last.weight_kg - first.weight_kg
    if weight_change <= -0.05 * first.weight_kg:
        achieved.append("≥5% weight loss achieved")
    if biomarker_changes.get("hba1c_pct", 0.0) <= -0.5:
        achieved.append("HbA1c dropped by ≥ 0.5 percentage points")
    if biomarker_changes.get("ldl_mg_dl", 0.0) <= -20.0:
        achieved.append("LDL dropped by ≥ 20 mg/dL")
    if biomarker_changes.get("systolic_bp_mmhg", 0.0) <= -5.0:
        achieved.append("Systolic BP dropped by ≥ 5 mmHg")

    if weight_change <= -0.10 * first.weight_kg and result.duration_weeks < 12:
        concerns.append("Weight loss exceeded 10% in under 12 weeks — overly aggressive")
    if biomarker_changes.get("potassium_mmol_l", 0.0) >= 0.5:
        concerns.append("Potassium rose by ≥ 0.5 mmol/L")

    return DietEvaluation(
        patient_id=result.patient_id,
        diet_name=result.diet_name,
        duration_weeks=result.duration_weeks,
        weight_change_kg=weight_change,
        bmi_change=last.bmi - first.bmi,
        biomarker_changes=biomarker_changes,
        constraint_warnings=list(constraint_warnings or []),
        achieved_goals=achieved,
        safety_concerns=concerns,
    )


def aggregate_cohort_results(
    evaluations: Iterable[DietEvaluation],
) -> pd.DataFrame:
    """Combine per-patient evaluations into a single DataFrame."""
    rows = []
    for ev in evaluations:
        row = {
            "patient_id": ev.patient_id,
            "diet_name": ev.diet_name,
            "duration_weeks": ev.duration_weeks,
            "weight_change_kg": ev.weight_change_kg,
            "bmi_change": ev.bmi_change,
            "n_warnings": len(ev.constraint_warnings),
            "n_goals_achieved": len(ev.achieved_goals),
            "n_safety_concerns": len(ev.safety_concerns),
        }
        row.update({f"delta_{k}": v for k, v in ev.biomarker_changes.items()})
        rows.append(row)
    return pd.DataFrame(rows)
