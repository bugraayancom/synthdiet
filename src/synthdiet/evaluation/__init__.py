"""Evaluation and reporting utilities."""

from synthdiet.evaluation.metrics import (
    DietEvaluation,
    aggregate_cohort_results,
    evaluate_simulation,
)
from synthdiet.evaluation.reports import format_evaluation_report, summarise_cohort

__all__ = [
    "DietEvaluation",
    "aggregate_cohort_results",
    "evaluate_simulation",
    "format_evaluation_report",
    "summarise_cohort",
]
