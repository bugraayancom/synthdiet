"""Human-readable report formatters."""

from __future__ import annotations

from typing import Iterable, List

import pandas as pd

from synthdiet.evaluation.metrics import DietEvaluation


def format_evaluation_report(evaluation: DietEvaluation) -> str:
    """Return a printable text report for a single diet evaluation."""
    lines: List[str] = []
    lines.append(f"=== Diet evaluation: {evaluation.diet_name} ===")
    lines.append(f"Patient: {evaluation.patient_id[:8]}")
    lines.append(f"Duration: {evaluation.duration_weeks} weeks")
    lines.append(
        f"Weight change: {evaluation.weight_change_kg:+.2f} kg "
        f"(BMI {evaluation.bmi_change:+.2f})"
    )

    if evaluation.biomarker_changes:
        lines.append("\nKey biomarker changes:")
        items = sorted(
            evaluation.biomarker_changes.items(),
            key=lambda kv: abs(kv[1]),
            reverse=True,
        )
        for k, v in items[:8]:
            if abs(v) < 1e-6:
                continue
            lines.append(f"  {k:<30s} {v:+.2f}")

    if evaluation.achieved_goals:
        lines.append("\nGoals achieved:")
        for goal in evaluation.achieved_goals:
            lines.append(f"  + {goal}")

    if evaluation.constraint_warnings:
        lines.append("\nConstraint warnings:")
        for w in evaluation.constraint_warnings:
            lines.append(f"  ! {w}")

    if evaluation.safety_concerns:
        lines.append("\nSafety concerns:")
        for c in evaluation.safety_concerns:
            lines.append(f"  * {c}")

    return "\n".join(lines)


def summarise_cohort(evaluations: Iterable[DietEvaluation]) -> pd.DataFrame:
    """Return a cohort-level summary (means, percentiles) as a DataFrame."""
    evaluations = list(evaluations)
    if not evaluations:
        return pd.DataFrame()
    weights = pd.Series([e.weight_change_kg for e in evaluations])
    bmis = pd.Series([e.bmi_change for e in evaluations])
    pct_loss = (weights <= -0.05).mean() * 100  # share with absolute >=5 kg loss
    return pd.DataFrame(
        [
            {
                "n_patients": len(evaluations),
                "mean_weight_change_kg": weights.mean(),
                "median_weight_change_kg": weights.median(),
                "p10_weight_change_kg": weights.quantile(0.10),
                "p90_weight_change_kg": weights.quantile(0.90),
                "mean_bmi_change": bmis.mean(),
                "share_>=5kg_loss_pct": pct_loss,
                "mean_warnings": sum(len(e.constraint_warnings) for e in evaluations) / len(evaluations),
                "mean_goals_achieved": sum(len(e.achieved_goals) for e in evaluations) / len(evaluations),
            }
        ]
    )
