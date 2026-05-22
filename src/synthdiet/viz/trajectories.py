"""Spaghetti and ribbon trajectory plots."""

from __future__ import annotations

from typing import Iterable, Optional, Sequence

import numpy as np

from synthdiet.simulation import SimulationResult
from synthdiet.viz._mpl import get_matplotlib


def trajectory_plot(
    results: Sequence[SimulationResult],
    *,
    variable: str = "weight_kg",
    show_individual: bool = True,
    show_ribbon: bool = True,
    title: Optional[str] = None,
    ax=None,
):
    """Plot per-patient trajectories with an optional median ribbon."""
    plt = get_matplotlib()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    if not results:
        raise ValueError("results must not be empty")

    weeks = sorted({tp.week for r in results for tp in r.timeline})
    matrix = []
    for r in results:
        values = []
        for w in weeks:
            tp = next((t for t in r.timeline if t.week == w), None)
            if tp is None:
                values.append(np.nan)
            elif variable in {"weight_kg", "bmi"}:
                values.append(getattr(tp, variable))
            else:
                values.append(tp.biomarkers.get(variable, np.nan))
        matrix.append(values)
    arr = np.array(matrix, dtype=float)

    if show_individual:
        for row in arr:
            ax.plot(weeks, row, alpha=0.15, linewidth=0.8)

    if show_ribbon:
        median = np.nanmedian(arr, axis=0)
        p25 = np.nanpercentile(arr, 25, axis=0)
        p75 = np.nanpercentile(arr, 75, axis=0)
        ax.fill_between(weeks, p25, p75, alpha=0.3, label="IQR")
        ax.plot(weeks, median, linewidth=2, label="median")

    ax.set_xlabel("Week")
    ax.set_ylabel(variable)
    ax.set_title(title or f"Trajectory of {variable}")
    ax.legend(loc="best")
    return ax
