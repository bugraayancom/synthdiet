"""Forest plot of subgroup effects."""

from __future__ import annotations

from typing import Mapping, Optional, Tuple

from synthdiet.viz._mpl import get_matplotlib


def forest_plot(
    subgroup_estimates: Mapping[str, Tuple[float, float, float]],
    *,
    title: Optional[str] = None,
    xlabel: str = "Effect size",
    null_line: float = 0.0,
    ax=None,
):
    """Forest plot from a mapping ``label -> (estimate, ci_low, ci_high)``."""
    plt = get_matplotlib()
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, max(3, 0.45 * len(subgroup_estimates))))

    labels = list(subgroup_estimates.keys())
    ys = list(range(len(labels)))[::-1]
    for y, label in zip(ys, labels):
        est, lo, hi = subgroup_estimates[label]
        ax.errorbar(est, y, xerr=[[est - lo], [hi - est]], fmt="o",
                    capsize=5, linewidth=1.5)

    ax.set_yticks(ys)
    ax.set_yticklabels(labels)
    ax.axvline(null_line, color="grey", linestyle="--", linewidth=1)
    ax.set_xlabel(xlabel)
    if title:
        ax.set_title(title)
    return ax
