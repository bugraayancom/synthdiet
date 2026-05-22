"""CONSORT-style flow diagram of a trial."""

from __future__ import annotations

from typing import Optional

from synthdiet.trials.analysis import TrialResult
from synthdiet.viz._mpl import get_matplotlib


def consort_diagram(
    result: TrialResult,
    *,
    title: Optional[str] = None,
    ax=None,
):
    """Draw a minimal CONSORT flow diagram."""
    plt = get_matplotlib()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    n_total = len(result.arms)
    arm_names = result.arm_names
    n_arms = len(arm_names)

    ax.axis("off")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    ax.text(5, 9, f"Randomised\nn = {n_total}",
            ha="center", va="center",
            bbox=dict(boxstyle="round", facecolor="lightgrey", edgecolor="black"))

    x_step = 10 / (n_arms + 1)
    for i, arm in enumerate(arm_names, start=1):
        x = i * x_step
        n_arm = sum(1 for a in result.arms.values() if a == arm)
        n_completed = (result.outcomes.query("arm == @arm")["dropout_week"]
                       > result.duration_weeks).sum()
        n_dropped = n_arm - n_completed
        ax.annotate("", xy=(x, 7.2), xytext=(5, 8.5),
                    arrowprops=dict(arrowstyle="->", color="black"))
        ax.text(x, 6.5, f"{arm}\nn = {n_arm}",
                ha="center", va="center",
                bbox=dict(boxstyle="round", facecolor="lightblue",
                          edgecolor="black"))
        ax.text(x, 4.2, f"Completed\nn = {n_completed}",
                ha="center", va="center",
                bbox=dict(boxstyle="round", facecolor="lightgreen",
                          edgecolor="black"))
        ax.text(x, 2.0, f"Withdrew\nn = {n_dropped}",
                ha="center", va="center",
                bbox=dict(boxstyle="round", facecolor="mistyrose",
                          edgecolor="black"))
        ax.annotate("", xy=(x, 4.8), xytext=(x, 5.8),
                    arrowprops=dict(arrowstyle="->", color="black"))
        ax.annotate("", xy=(x, 2.6), xytext=(x, 3.6),
                    arrowprops=dict(arrowstyle="->", color="black"))

    if title:
        ax.set_title(title)
    return ax
