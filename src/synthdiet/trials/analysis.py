"""Trial result container and ITT/PP/AT analysis helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

import numpy as np
import pandas as pd
from scipy import stats

from synthdiet.patients.patient import Patient


@dataclass
class AnalysisResult:
    """Result of one analysis comparison between two arms."""

    method: str
    arm_a: str
    arm_b: str
    outcome: str
    mean_a: float
    mean_b: float
    diff: float
    se: float
    ci_95: tuple
    p_value: float
    n_a: int
    n_b: int

    def pretty(self) -> str:
        lo, hi = self.ci_95
        return (
            f"[{self.method}] {self.outcome}: {self.arm_b} - {self.arm_a} = "
            f"{self.diff:+.3f} (95% CI {lo:+.3f}, {hi:+.3f}), p={self.p_value:.4f} "
            f"(n_a={self.n_a}, n_b={self.n_b})"
        )


@dataclass
class TrialResult:
    """Container for a finished trial."""

    arms: Mapping[str, str]  # patient_id -> arm name
    arm_diets: Mapping[str, Any]  # arm name -> diet
    outcomes: pd.DataFrame  # rows = patients, cols = baseline_/final_/delta_<outcome>
    duration_weeks: int
    primary_outcome: str
    secondary_outcomes: List[str] = field(default_factory=list)
    dropout_weeks: Dict[str, int] = field(default_factory=dict)
    adherence_summary: Dict[str, float] = field(default_factory=dict)

    @property
    def arm_names(self) -> List[str]:
        return sorted(set(self.arms.values()))

    def assigned(self, arm: str) -> pd.DataFrame:
        ids = [pid for pid, a in self.arms.items() if a == arm]
        return self.outcomes[self.outcomes["patient_id"].isin(ids)]

    def consort_diagram(self) -> str:
        """Return a text-art CONSORT flow diagram."""
        lines = ["CONSORT flow diagram", "===================="]
        for arm in self.arm_names:
            patients = self.assigned(arm)
            n_total = len(patients)
            n_completed = (patients["dropout_week"] > self.duration_weeks).sum()
            n_dropped = n_total - n_completed
            lines.append(f"Arm '{arm}':")
            lines.append(f"  Randomised: n = {n_total}")
            lines.append(f"  Completed:  n = {n_completed}")
            lines.append(f"  Withdrew:   n = {n_dropped}")
        return "\n".join(lines)

    # Convenience analyses -------------------------------------------------
    def intention_to_treat(
        self,
        outcome: Optional[str] = None,
        method: str = "ancova",
    ) -> AnalysisResult:
        return intention_to_treat(self, outcome=outcome, method=method)

    def per_protocol(
        self,
        outcome: Optional[str] = None,
        adherence_threshold: float = 0.80,
    ) -> AnalysisResult:
        return per_protocol(self, outcome=outcome, adherence_threshold=adherence_threshold)

    def as_treated(self, outcome: Optional[str] = None) -> AnalysisResult:
        return as_treated(self, outcome=outcome)


# --- Analysis functions ---------------------------------------------------
def _select_outcome(result: TrialResult, outcome: Optional[str]) -> str:
    return outcome or result.primary_outcome


def _two_arm_data(result: TrialResult, outcome: str) -> tuple:
    if len(result.arm_names) != 2:
        raise NotImplementedError("Multi-arm analyses not yet supported")
    arm_a, arm_b = result.arm_names
    delta_col = f"delta_{outcome}"
    if delta_col not in result.outcomes.columns:
        raise KeyError(
            f"outcome '{outcome}' not in trial results. "
            f"Available: {list(result.outcomes.columns)}"
        )
    return arm_a, arm_b, delta_col


def _two_sample_test(values_a: np.ndarray, values_b: np.ndarray, method: str) -> tuple:
    if method == "ancova":
        # Simplified: independent t-test on delta values.
        # ANCOVA proper requires baseline as covariate; statsmodels integration
        # lives in synthdiet.stats.ancova.
        t, p = stats.ttest_ind(values_b, values_a, equal_var=False)
    elif method == "t_test":
        t, p = stats.ttest_ind(values_b, values_a, equal_var=False)
    elif method == "mann_whitney":
        u, p = stats.mannwhitneyu(values_b, values_a, alternative="two-sided")
        t = u
    else:
        raise ValueError(f"unknown method {method!r}")
    diff = float(np.mean(values_b) - np.mean(values_a))
    n_a, n_b = len(values_a), len(values_b)
    pooled_var = (np.var(values_a, ddof=1) / n_a + np.var(values_b, ddof=1) / n_b)
    se = float(np.sqrt(max(pooled_var, 1e-12)))
    ci = (diff - 1.96 * se, diff + 1.96 * se)
    return diff, se, ci, float(p), t


def intention_to_treat(
    result: TrialResult,
    outcome: Optional[str] = None,
    method: str = "ancova",
) -> AnalysisResult:
    """ITT analysis: include every randomised patient regardless of adherence."""
    outcome = _select_outcome(result, outcome)
    arm_a, arm_b, delta_col = _two_arm_data(result, outcome)
    values_a = result.assigned(arm_a)[delta_col].to_numpy()
    values_b = result.assigned(arm_b)[delta_col].to_numpy()
    diff, se, ci, p, _ = _two_sample_test(values_a, values_b, method)
    return AnalysisResult(
        method=f"ITT ({method})",
        arm_a=arm_a,
        arm_b=arm_b,
        outcome=outcome,
        mean_a=float(np.mean(values_a)),
        mean_b=float(np.mean(values_b)),
        diff=diff,
        se=se,
        ci_95=ci,
        p_value=p,
        n_a=len(values_a),
        n_b=len(values_b),
    )


def per_protocol(
    result: TrialResult,
    outcome: Optional[str] = None,
    adherence_threshold: float = 0.80,
) -> AnalysisResult:
    """PP analysis: only patients above ``adherence_threshold``."""
    outcome = _select_outcome(result, outcome)
    arm_a, arm_b, delta_col = _two_arm_data(result, outcome)
    df = result.outcomes
    eligible = df[df["mean_adherence"] >= adherence_threshold]
    a_vals = eligible[eligible["patient_id"].isin(
        [pid for pid, a in result.arms.items() if a == arm_a])][delta_col].to_numpy()
    b_vals = eligible[eligible["patient_id"].isin(
        [pid for pid, a in result.arms.items() if a == arm_b])][delta_col].to_numpy()
    diff, se, ci, p, _ = _two_sample_test(a_vals, b_vals, method="t_test")
    return AnalysisResult(
        method=f"PP (>={adherence_threshold:.0%} adherence)",
        arm_a=arm_a,
        arm_b=arm_b,
        outcome=outcome,
        mean_a=float(np.mean(a_vals)) if len(a_vals) else float("nan"),
        mean_b=float(np.mean(b_vals)) if len(b_vals) else float("nan"),
        diff=diff,
        se=se,
        ci_95=ci,
        p_value=p,
        n_a=len(a_vals),
        n_b=len(b_vals),
    )


def as_treated(
    result: TrialResult,
    outcome: Optional[str] = None,
) -> AnalysisResult:
    """AT analysis: assign to the arm the patient actually adhered to.

    For this minimal implementation, an "as-treated" analysis is identical to
    ITT — a fully fleshed-out implementation would require modelling cross-over
    behaviour between arms, which is outside the scope of v0.1.
    """
    outcome = _select_outcome(result, outcome)
    ar = intention_to_treat(result, outcome=outcome, method="t_test")
    return AnalysisResult(
        method="AT (alias of ITT in v0.1)",
        arm_a=ar.arm_a,
        arm_b=ar.arm_b,
        outcome=ar.outcome,
        mean_a=ar.mean_a,
        mean_b=ar.mean_b,
        diff=ar.diff,
        se=ar.se,
        ci_95=ar.ci_95,
        p_value=ar.p_value,
        n_a=ar.n_a,
        n_b=ar.n_b,
    )


# Required for type signatures referencing Patient at runtime (test).
_ = Patient
