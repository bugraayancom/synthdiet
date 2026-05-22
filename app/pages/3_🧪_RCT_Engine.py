"""RCT Engine page.

Run a parallel-arm randomised controlled trial on the active cohort,
configure dropout, and analyse with ITT / per-protocol methods. Visualise
CONSORT flow, per-arm distributions and forest plots.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

APP_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_DIR))

from components import (  # noqa: E402
    DIET_META,
    callout,
    disclaimer,
    hero,
    metric_grid,
    page_setup,
    section,
)

from synthdiet.diets import (  # noqa: E402
    dash_diet,
    diabetic_diet,
    keto_diet,
    list_presets,
    low_fodmap_diet,
    low_sodium_renal_diet,
    mediterranean_diet,
    standard_diet,
    vegan_diet,
)
from synthdiet.trials import (  # noqa: E402
    NoDropout,
    ParallelTrial,
    WeibullDropout,
)

PRIMARY = "#0EA5E9"
PRIMARY_STRONG = "#0284C7"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"
GRID = "#E2E8F0"

ARM_COLOURS = {
    "control": "#94A3B8",
    "intervention": PRIMARY_STRONG,
}

DIET_CONSTRUCTORS = {
    "mediterranean": mediterranean_diet,
    "dash": dash_diet,
    "keto": keto_diet,
    "low_fodmap": low_fodmap_diet,
    "low_sodium_renal": low_sodium_renal_diet,
    "diabetic": diabetic_diet,
    "vegan": vegan_diet,
    "standard": standard_diet,
}

OUTCOME_LABELS = {
    "systolic_bp_mmhg": ("Systolic BP", "mmHg"),
    "diastolic_bp_mmhg": ("Diastolic BP", "mmHg"),
    "weight_kg": ("Weight", "kg"),
    "bmi": ("BMI", ""),
    "ldl_mg_dl": ("LDL cholesterol", "mg/dL"),
    "hdl_mg_dl": ("HDL cholesterol", "mg/dL"),
    "triglycerides_mg_dl": ("Triglycerides", "mg/dL"),
    "hba1c_pct": ("HbA1c", "%"),
    "fasting_glucose_mg_dl": ("Fasting glucose", "mg/dL"),
}


def _adherence(result) -> dict:
    """Return adherence summary as a dict, regardless of attribute / method API."""
    s = getattr(result, "adherence_summary", {})
    return s() if callable(s) else (s or {})


# ---------------------------------------------------------------------------
# Plotly polish
# ---------------------------------------------------------------------------
def _polish(fig: go.Figure, *, height: int = 360) -> go.Figure:
    fig.update_layout(
        height=height,
        margin=dict(l=12, r=12, t=24, b=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, system-ui, sans-serif", size=12, color="#0F172A"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
        ),
        hoverlabel=dict(
            bgcolor="#0F172A",
            bordercolor="#0F172A",
            font=dict(family="Inter", color="white"),
        ),
    )
    fig.update_xaxes(gridcolor=GRID, zeroline=False, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zeroline=False, linecolor=GRID)
    return fig


# ---------------------------------------------------------------------------
# CONSORT flow diagram (custom Plotly Sankey-like)
# ---------------------------------------------------------------------------
def _consort_diagram(
    arm_a: str,
    arm_b: str,
    n_a_rand: int,
    n_b_rand: int,
    n_a_compl: int,
    n_b_compl: int,
) -> go.Figure:
    """Render a clean CONSORT flow chart using shapes + annotations."""
    n_screened = n_a_rand + n_b_rand

    fig = go.Figure()

    boxes = [
        # (x0, y0, x1, y1, label, fill, border)
        (0.30, 0.85, 0.70, 0.95, f"Assessed for eligibility (n = {n_screened})",
         "#F1F5F9", "#CBD5E1"),
        (0.30, 0.65, 0.70, 0.75,
         f"Randomised (n = {n_screened})", "#E0F2FE", PRIMARY),
        (0.05, 0.40, 0.45, 0.50,
         f"Allocated to <b>{arm_a}</b> (n = {n_a_rand})", "#F8FAFC", "#94A3B8"),
        (0.55, 0.40, 0.95, 0.50,
         f"Allocated to <b>{arm_b}</b> (n = {n_b_rand})", "#E0F2FE", PRIMARY_STRONG),
        (0.05, 0.20, 0.45, 0.30,
         f"Withdrew (n = {n_a_rand - n_a_compl})", "#FEF3C7", WARNING),
        (0.55, 0.20, 0.95, 0.30,
         f"Withdrew (n = {n_b_rand - n_b_compl})", "#FEF3C7", WARNING),
        (0.05, 0.02, 0.45, 0.12,
         f"Analysed (n = {n_a_compl})", "#D1FAE5", SUCCESS),
        (0.55, 0.02, 0.95, 0.12,
         f"Analysed (n = {n_b_compl})", "#D1FAE5", SUCCESS),
    ]
    for x0, y0, x1, y1, label, fill, border in boxes:
        fig.add_shape(
            type="rect", xref="paper", yref="paper",
            x0=x0, y0=y0, x1=x1, y1=y1,
            fillcolor=fill,
            line=dict(color=border, width=1.5),
        )
        fig.add_annotation(
            xref="paper", yref="paper",
            x=(x0 + x1) / 2, y=(y0 + y1) / 2,
            text=label,
            showarrow=False,
            font=dict(size=12, color="#0F172A"),
            align="center",
        )

    # Connectors: simple straight lines + a small triangle marker at the
    # tail to act as an arrow. Avoids the Plotly 6.x deprecation of
    # ``axref="paper"`` on annotations.
    connectors = [
        # (x0, y0, x1, y1)
        (0.5, 0.85, 0.5, 0.75),   # eligibility -> randomised
        (0.5, 0.65, 0.25, 0.50),  # randomised -> arm A
        (0.5, 0.65, 0.75, 0.50),  # randomised -> arm B
        (0.25, 0.40, 0.25, 0.30),  # arm A -> withdrew
        (0.75, 0.40, 0.75, 0.30),  # arm B -> withdrew
        (0.25, 0.20, 0.25, 0.12),  # arm A -> analysed
        (0.75, 0.20, 0.75, 0.12),  # arm B -> analysed
    ]
    arrow_xs: list[float] = []
    arrow_ys: list[float] = []
    for x0, y0, x1, y1 in connectors:
        fig.add_shape(
            type="line", xref="paper", yref="paper",
            x0=x0, y0=y0, x1=x1, y1=y1,
            line=dict(color="#94A3B8", width=1.5),
        )
        arrow_xs.append(x1)
        arrow_ys.append(y1)
    fig.add_trace(
        go.Scatter(
            x=arrow_xs,
            y=arrow_ys,
            xaxis="x",
            yaxis="y",
            mode="markers",
            marker=dict(symbol="triangle-down", size=10, color="#94A3B8"),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    fig.update_xaxes(visible=False, range=[0, 1])
    fig.update_yaxes(visible=False, range=[-0.05, 1.05])
    fig.update_layout(
        showlegend=False,
        height=520,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig


# ---------------------------------------------------------------------------
# Forest plot
# ---------------------------------------------------------------------------
def _forest_plot(rows: list[dict[str, Any]]) -> go.Figure:
    """Render a forest plot from analysis rows.

    Each row must have keys: ``label``, ``diff``, ``ci_lo``, ``ci_hi``, ``unit``.
    Negative ``diff`` is plotted as 'favours intervention' (left side).
    """
    fig = go.Figure()
    if not rows:
        fig.add_annotation(text="No outcomes available", showarrow=False)
        return _polish(fig, height=240)

    labels = [r["label"] for r in rows]
    diffs = [r["diff"] for r in rows]
    ci_lo = [r["ci_lo"] for r in rows]
    ci_hi = [r["ci_hi"] for r in rows]
    units = [r["unit"] for r in rows]

    y = list(range(len(rows)))[::-1]  # top-down ordering

    # Confidence interval lines
    for yi, lo, hi in zip(y, ci_lo, ci_hi):
        fig.add_shape(
            type="line",
            x0=lo, x1=hi, y0=yi, y1=yi,
            line=dict(color="#64748B", width=2),
        )
        # Caps
        for x in (lo, hi):
            fig.add_shape(
                type="line", x0=x, x1=x,
                y0=yi - 0.15, y1=yi + 0.15,
                line=dict(color="#64748B", width=2),
            )

    # Point estimates
    fig.add_trace(
        go.Scatter(
            x=diffs,
            y=y,
            mode="markers",
            marker=dict(
                size=12,
                color=[
                    SUCCESS if d < 0 else DANGER
                    for d in diffs
                ],
                line=dict(color="white", width=2),
            ),
            customdata=list(zip(labels, ci_lo, ci_hi, units)),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Δ = %{x:.2f} %{customdata[3]}<br>"
                "95%% CI [%{customdata[1]:.2f}, %{customdata[2]:.2f}]"
                "<extra></extra>"
            ),
            showlegend=False,
        )
    )

    # Reference line at 0 (no effect)
    fig.add_vline(x=0, line_dash="dash", line_color="#CBD5E1", line_width=1)

    # Annotations: "favours intervention" / "favours control"
    fig.add_annotation(
        xref="paper", x=0.02, yref="paper", y=1.06,
        text="◀ favours <b>intervention</b>",
        showarrow=False, font=dict(size=11, color=SUCCESS),
    )
    fig.add_annotation(
        xref="paper", x=0.98, yref="paper", y=1.06,
        text="favours <b>control</b> ▶",
        showarrow=False, font=dict(size=11, color=DANGER), xanchor="right",
    )

    fig.update_yaxes(
        tickmode="array",
        tickvals=y,
        ticktext=labels,
        showgrid=False,
    )
    fig.update_xaxes(title="Treatment effect (intervention − control)")
    fig.update_layout(
        showlegend=False,
        height=max(260, 60 * len(rows) + 80),
    )
    return _polish(fig, height=max(260, 60 * len(rows) + 80))


# ---------------------------------------------------------------------------
# Box plot per arm
# ---------------------------------------------------------------------------
def _arm_box(
    df: pd.DataFrame,
    column: str,
    label: str,
    unit: str,
    arms_order: list[str],
) -> go.Figure:
    fig = go.Figure()
    for arm in arms_order:
        sub = df[df["arm"] == arm][column].dropna()
        colour = ARM_COLOURS["control"] if arm == arms_order[0] else ARM_COLOURS["intervention"]
        fig.add_trace(
            go.Box(
                y=sub,
                name=arm,
                marker_color=colour,
                boxmean="sd",
                boxpoints="outliers",
                line=dict(width=1.5),
                hovertemplate=f"<b>{arm}</b><br>{label}: %{{y:.2f}} {unit}<extra></extra>",
            )
        )
    fig.update_yaxes(title=f"Δ {label} ({unit})")
    fig.update_xaxes(title="Arm")
    fig.update_layout(showlegend=False)
    return _polish(fig, height=300)


# ---------------------------------------------------------------------------
# Cached trial run
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def _run_trial(
    cohort_signature: tuple[Any, ...],
    control_diet: str,
    intervention_diet: str,
    daily_kcal: int,
    duration_weeks: int,
    primary: str,
    secondaries: tuple[str, ...],
    randomization: str,
    adherence: float,
    dropout_kind: str,
    dropout_seed: int,
    engine: str,
    trial_seed: int,
):
    patients = st.session_state.get("cohort_patients")
    if not patients:
        return None

    arms = {
        "control": DIET_CONSTRUCTORS[control_diet](daily_energy_kcal=daily_kcal),
        "intervention": DIET_CONSTRUCTORS[intervention_diet](daily_energy_kcal=daily_kcal),
    }
    if dropout_kind == "weibull":
        dropout = WeibullDropout(shape=1.5, scale_weeks=40, seed=dropout_seed)
    else:
        dropout = NoDropout()

    trial = ParallelTrial(
        cohort=patients,
        arms=arms,
        duration_weeks=duration_weeks,
        primary_outcome=primary,
        secondary_outcomes=list(secondaries),
        randomization=randomization,
        adherence=adherence,
        dropout=dropout,
        engine=engine,
    )
    return trial.run(seed=trial_seed)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    page_setup(title="RCT Engine", icon="🧪")

    hero(
        eyebrow="step 3 · virtual randomised trial",
        title_html=(
            "Compare two diets with a "
            "<span class='accent'>full RCT pipeline</span>."
        ),
        subtitle=(
            "Pick the active cohort, assign control vs intervention diets, "
            "configure dropout and adherence, then read the trial through "
            "ITT, per-protocol and as-treated lenses — with a CONSORT flow "
            "diagram and forest plot."
        ),
    )

    patients = st.session_state.get("cohort_patients")
    df_cohort = st.session_state.get("cohort_df")
    if not patients or df_cohort is None or df_cohort.empty:
        callout(
            "You need to generate a cohort first. Open "
            "<strong>Cohort Builder</strong> from the sidebar.",
            tone="warning",
        )
        st.stop()

    # ------------------------------------------------------------------
    # Sidebar
    # ------------------------------------------------------------------
    with st.sidebar:
        st.markdown("### Trial design")

        presets = list_presets()
        control_diet = st.selectbox(
            "Control arm diet",
            options=presets,
            index=presets.index("standard"),
            format_func=lambda k: DIET_META.get(k, {}).get("name", k),
        )
        intervention_diet = st.selectbox(
            "Intervention arm diet",
            options=presets,
            index=presets.index("dash"),
            format_func=lambda k: DIET_META.get(k, {}).get("name", k),
        )

        duration_weeks = st.slider("Duration (weeks)", 8, 52, 24, step=4)
        daily_kcal = st.slider("Daily energy (kcal)", 1200, 2800, 1800, step=100)

        st.markdown("### Outcomes")
        primary = st.selectbox(
            "Primary outcome",
            options=list(OUTCOME_LABELS.keys()),
            index=0,
            format_func=lambda k: f"{OUTCOME_LABELS[k][0]} ({OUTCOME_LABELS[k][1]})",
        )
        secondaries_raw = st.multiselect(
            "Secondary outcomes",
            options=[k for k in OUTCOME_LABELS if k != primary],
            default=[k for k in ("weight_kg", "ldl_mg_dl", "hba1c_pct") if k != primary],
            format_func=lambda k: f"{OUTCOME_LABELS[k][0]} ({OUTCOME_LABELS[k][1]})",
        )

        st.markdown("### Statistical & behavioural")
        randomization = st.selectbox(
            "Randomisation",
            options=["block", "simple", "stratified", "minimization"],
            index=0,
        )
        adherence = st.slider("Adherence (mean)", 0.4, 1.0, 0.85, step=0.05)
        dropout_kind = st.radio(
            "Dropout model",
            options=["weibull", "none"],
            format_func=lambda k: {
                "weibull": "Weibull (realistic)",
                "none": "None (best case)",
            }[k],
            horizontal=True,
        )
        engine = st.radio(
            "Engine",
            options=["hall_2011", "simple"],
            format_func=lambda k: {
                "hall_2011": "Hall 2011",
                "simple": "Simple",
            }[k],
            horizontal=True,
        )

        st.markdown("### Reproducibility")
        trial_seed = st.number_input("Trial seed", 0, 10_000, 42, step=1)
        dropout_seed = st.number_input("Dropout seed", 0, 10_000, 7, step=1)

        st.markdown("---")
        run_clicked = st.button(
            "🧪 Run trial",
            type="primary",
            use_container_width=True,
        )

    if control_diet == intervention_diet:
        callout(
            "Pick <strong>different diets</strong> for the two arms — "
            "comparing a diet to itself yields no effect.",
            tone="warning",
        )
        st.stop()

    # ------------------------------------------------------------------
    # Run trial
    # ------------------------------------------------------------------
    if "trial_signature" not in st.session_state:
        st.session_state.trial_signature = None

    signature = (
        st.session_state.get("cohort_spec", {}).get("seed"),
        len(df_cohort),
        tuple(st.session_state.get("cohort_spec", {}).get("diseases", [])),
        control_diet,
        intervention_diet,
        int(daily_kcal),
        int(duration_weeks),
        primary,
        tuple(secondaries_raw),
        randomization,
        float(adherence),
        dropout_kind,
        int(dropout_seed),
        engine,
        int(trial_seed),
    )

    if run_clicked or st.session_state.trial_signature != signature:
        with st.spinner("Running RCT…"):
            cohort_sig = signature[:3]
            result = _run_trial(cohort_sig, *signature[3:])
        st.session_state.trial_result = result
        st.session_state.trial_signature = signature

    result = st.session_state.get("trial_result")
    if result is None:
        callout("Press <strong>Run trial</strong> in the sidebar to start.", tone="info")
        st.stop()

    df = result.outcomes
    arm_counts = df["arm"].value_counts()
    n_a_rand = int(arm_counts.get("control", 0))
    n_b_rand = int(arm_counts.get("intervention", 0))
    # A patient "completed" the trial iff their dropout_week is missing
    # OR exceeds the planned duration (the engine writes duration_weeks + 1
    # for completers).
    dw = df["dropout_week"]
    completed_mask = dw.isna() | (dw > int(duration_weeks))
    completed = df[completed_mask]
    n_a_compl = int((completed["arm"] == "control").sum())
    n_b_compl = int((completed["arm"] == "intervention").sum())

    # ------------------------------------------------------------------
    # Top metrics
    # ------------------------------------------------------------------
    section("Trial overview")

    itt = result.intention_to_treat()
    pp = result.per_protocol(adherence_threshold=0.7)

    primary_label, primary_unit = OUTCOME_LABELS[primary]

    metric_grid(
        [
            (
                "Randomised",
                f"{n_a_rand + n_b_rand}",
                f"control {n_a_rand} · intervention {n_b_rand}",
                "primary",
            ),
            (
                "Completed",
                f"{n_a_compl + n_b_compl}",
                (
                    f"dropout "
                    f"{100 * (1 - (n_a_compl + n_b_compl) / max(1, n_a_rand + n_b_rand)):.0f}%"
                ),
                "warning" if (n_a_rand + n_b_rand - n_a_compl - n_b_compl) > 0 else "",
            ),
            (
                f"ITT Δ {primary_label}",
                f"{itt.diff:+.2f} {primary_unit}",
                f"95% CI [{itt.ci_95[0]:+.2f}, {itt.ci_95[1]:+.2f}]",
                "success" if itt.diff < 0 else "danger",
            ),
            (
                "p-value (ITT)",
                f"{itt.p_value:.4f}",
                "significant" if itt.p_value < 0.05 else "ns",
                "success" if itt.p_value < 0.05 else "",
            ),
            (
                f"PP Δ {primary_label}",
                f"{pp.diff:+.2f} {primary_unit}",
                f"95% CI [{pp.ci_95[0]:+.2f}, {pp.ci_95[1]:+.2f}]",
                "success" if pp.diff < 0 else "danger",
            ),
            (
                "Mean adherence",
                f"{_adherence(result).get('intervention', 0):.0%}",
                "intervention arm",
                "",
            ),
        ]
    )

    # ------------------------------------------------------------------
    # CONSORT
    # ------------------------------------------------------------------
    section("CONSORT flow", meta="randomised → allocated → analysed")
    st.plotly_chart(
        _consort_diagram(
            arm_a="control",
            arm_b="intervention",
            n_a_rand=n_a_rand,
            n_b_rand=n_b_rand,
            n_a_compl=n_a_compl,
            n_b_compl=n_b_compl,
        ),
        use_container_width=True,
    )

    # ------------------------------------------------------------------
    # Forest plot
    # ------------------------------------------------------------------
    section("Forest plot", meta="primary + secondary outcomes")

    from synthdiet.trials import intention_to_treat as _itt

    forest_rows: list[dict[str, Any]] = []
    all_outcomes = [primary] + list(secondaries_raw)
    for oc in all_outcomes:
        if oc not in OUTCOME_LABELS:
            continue
        delta_col = f"delta_{oc}"
        if delta_col not in df.columns:
            continue
        try:
            ar = _itt(result, outcome=oc)
        except Exception:
            continue
        forest_rows.append(
            {
                "label": OUTCOME_LABELS[oc][0],
                "diff": ar.diff,
                "ci_lo": ar.ci_95[0],
                "ci_hi": ar.ci_95[1],
                "unit": OUTCOME_LABELS[oc][1],
            }
        )

    if forest_rows:
        st.plotly_chart(_forest_plot(forest_rows), use_container_width=True)
    else:
        callout("No analysable outcomes for the forest plot.", tone="warning")

    # ------------------------------------------------------------------
    # Per-arm distributions
    # ------------------------------------------------------------------
    section("Per-arm Δ distributions")

    cols = st.columns(2)
    arms_order = ["control", "intervention"]
    plot_outcomes = [primary] + list(secondaries_raw)[:3]
    for i, oc in enumerate(plot_outcomes):
        delta_col = f"delta_{oc}"
        if delta_col not in df.columns:
            continue
        label, unit = OUTCOME_LABELS.get(oc, (oc, ""))
        with cols[i % 2]:
            st.markdown(f"**{label}**")
            st.plotly_chart(
                _arm_box(df, delta_col, label, unit, arms_order),
                use_container_width=True,
            )

    # ------------------------------------------------------------------
    # Analysis details
    # ------------------------------------------------------------------
    section("Analysis details")

    tabs = st.tabs(["ITT", "Per-protocol", "As-treated", "Raw data"])
    with tabs[0]:
        st.code(itt.pretty(), language="text")
    with tabs[1]:
        st.code(pp.pretty(), language="text")
    with tabs[2]:
        try:
            at = result.as_treated()
            st.code(at.pretty(), language="text")
        except Exception as exc:
            st.write(f"As-treated analysis unavailable: {exc}")
    with tabs[3]:
        st.dataframe(df, use_container_width=True, height=320)

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    col_dl, col_text = st.columns([1, 3])
    with col_dl:
        st.download_button(
            "📥 Download trial results (CSV)",
            data=csv_bytes,
            file_name=(
                f"synthdiet_rct_{control_diet}_vs_{intervention_diet}_"
                f"{duration_weeks}w_seed{trial_seed}.csv"
            ),
            mime="text/csv",
            type="primary",
            use_container_width=True,
        )
    with col_text:
        st.markdown(
            "<div style='padding-top:6px; color:#475569; font-size:14px;'>"
            "Tip: change the trial seed in the sidebar to estimate how "
            "robust the effect is to allocation reshuffling."
            "</div>",
            unsafe_allow_html=True,
        )

    disclaimer()


if __name__ == "__main__":
    main()
