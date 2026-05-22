"""Statistical helpers for trial design and analysis."""

from synthdiet.stats.ancova import ancova_baseline_adjusted
from synthdiet.stats.inference import (
    bootstrap_ci,
    fdr_bh,
    holm_bonferroni,
    permutation_test,
)
from synthdiet.stats.power import (
    sample_size_binary,
    sample_size_continuous,
)

__all__ = [
    "ancova_baseline_adjusted",
    "bootstrap_ci",
    "fdr_bh",
    "holm_bonferroni",
    "permutation_test",
    "sample_size_binary",
    "sample_size_continuous",
]
