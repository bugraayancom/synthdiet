"""Cohort Builder page.

Interactively configure a CohortSpec, regenerate the cohort and inspect
demographic / disease distributions with animated charts.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Make ``components`` importable when Streamlit runs this file from a
# subdirectory.
APP_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_DIR))

from components import (  # noqa: E402
    callout,
    disclaimer,
    disease_chip_kind,
    disease_label,
    hero,
    metric_grid,
    page_setup,
    patient_card,
    section,
)

from synthdiet import (  # noqa: E402
    CohortGenerator,
    CohortSpec,
    DiseaseSpec,
    available_diseases,
)

PRIMARY = "#0EA5E9"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"
GRID = "#E2E8F0"
TEXT_SOFT = "#475569"


# ---------------------------------------------------------------------------
# Cached cohort generator
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def _generate_cohort(
    size: int,
    diseases: tuple[tuple[str, float], ...],
    seed: int,
) -> pd.DataFrame:
    """Generate a cohort and return a tidy DataFrame for plotting.

    Patients themselves are not pickle-friendly across Streamlit cache
    boundaries, so we serialise the relevant columns instead. The full
    Patient objects are available via :func:`_generate_patients`.
    """
    spec = CohortSpec(
        size=size,
        diseases=[DiseaseSpec(name, prev) for name, prev in diseases],
    )
    cohort = CohortGenerator(spec, seed=seed).generate()
    rows = []
    for idx, p in enumerate(cohort):
        rows.append(
            {
                "id": idx,
                "uuid": p.uid[:8] if hasattr(p, "uid") else f"P{idx:04d}",
                "age": p.demographics.age,
                "sex": p.demographics.sex.value,
                "country": p.demographics.country or "—",
                "height_cm": p.anthropometrics.height_cm,
                "weight_kg": p.anthropometrics.weight_kg,
                "bmi": p.bmi,
                "diseases": [d.name for d in p.diseases],
                "disease_count": len(p.diseases),
            }
        )
    return pd.DataFrame(rows)


@st.cache_resource(show_spinner=False)
def _generate_patients(
    size: int,
    diseases: tuple[tuple[str, float], ...],
    seed: int,
):
    spec = CohortSpec(
        size=size,
        diseases=[DiseaseSpec(name, prev) for name, prev in diseases],
    )
    return CohortGenerator(spec, seed=seed).generate()


# ---------------------------------------------------------------------------
# Plot helpers
# ---------------------------------------------------------------------------
def _bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "underweight"
    if bmi < 25:
        return "normal"
    if bmi < 30:
        return "overweight"
    if bmi < 35:
        return "obese I"
    if bmi < 40:
        return "obese II"
    return "obese III"


def _polish(fig: go.Figure, *, height: int = 320) -> go.Figure:
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
        transition=dict(duration=400, easing="cubic-in-out"),
    )
    fig.update_xaxes(gridcolor=GRID, zeroline=False, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zeroline=False, linecolor=GRID)
    return fig


def _age_histogram(df: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        df,
        x="age",
        color="sex",
        nbins=20,
        barmode="overlay",
        opacity=0.75,
        color_discrete_map={"female": "#F472B6", "male": PRIMARY},
        labels={"age": "Age (years)", "count": "Patients"},
    )
    return _polish(fig, height=300)


def _bmi_histogram(df: pd.DataFrame) -> go.Figure:
    fig = px.histogram(
        df,
        x="bmi",
        nbins=24,
        color_discrete_sequence=[SUCCESS],
        labels={"bmi": "BMI", "count": "Patients"},
    )
    fig.update_traces(marker_line_color="white", marker_line_width=1)
    fig.add_vline(
        x=25,
        line_dash="dash",
        line_color=WARNING,
        annotation_text="overweight",
        annotation_position="top right",
        annotation_font_color=WARNING,
        annotation_font_size=11,
    )
    fig.add_vline(
        x=30,
        line_dash="dash",
        line_color=DANGER,
        annotation_text="obese",
        annotation_position="top right",
        annotation_font_color=DANGER,
        annotation_font_size=11,
    )
    return _polish(fig, height=300)


def _disease_bar(df: pd.DataFrame) -> go.Figure:
    counts: dict[str, int] = {}
    for diseases in df["diseases"]:
        for d in diseases:
            counts[d] = counts.get(d, 0) + 1
    if not counts:
        return _polish(go.Figure(), height=240)
    items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    labels = [disease_label(name) for name, _ in items]
    values = [c for _, c in items]
    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker=dict(
                color=values,
                colorscale=[[0, "#BAE6FD"], [1, PRIMARY]],
                line=dict(color="white", width=1),
            ),
            text=values,
            textposition="outside",
            textfont=dict(color="#0F172A", size=11),
            hovertemplate="<b>%{y}</b><br>%{x} patients<extra></extra>",
        )
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title="Patients",
        yaxis=dict(autorange="reversed"),
    )
    return _polish(fig, height=max(240, 36 * len(items) + 60))


def _bmi_donut(df: pd.DataFrame) -> go.Figure:
    cats = df["bmi"].apply(_bmi_category).value_counts()
    order = ["underweight", "normal", "overweight", "obese I", "obese II", "obese III"]
    palette = {
        "underweight": "#94A3B8",
        "normal": SUCCESS,
        "overweight": WARNING,
        "obese I": "#FB923C",
        "obese II": "#F87171",
        "obese III": DANGER,
    }
    labels = [c for c in order if c in cats.index]
    values = [int(cats[c]) for c in labels]
    colours = [palette[c] for c in labels]
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.6,
            marker=dict(colors=colours, line=dict(color="white", width=2)),
            textposition="outside",
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>%{value} patients · %{percent}<extra></extra>",
        )
    )
    fig.update_layout(showlegend=False)
    return _polish(fig, height=320)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    page_setup(title="Cohort Builder", icon="📋")

    hero(
        eyebrow="step 1 · synthetic cohort",
        title_html=(
            "Generate a "
            "<span class='accent'>realistic patient cohort</span> "
            "with one click."
        ),
        subtitle=(
            "Configure size, age band, sex ratio and disease prevalences. "
            "Distributions update on every change. The cohort can be reused "
            "in the Diet Simulator and RCT Engine pages."
        ),
    )

    # ------------------------------------------------------------------
    # Sidebar controls
    # ------------------------------------------------------------------
    with st.sidebar:
        st.markdown("### Cohort settings")
        size = st.slider("Cohort size", min_value=10, max_value=500, value=100, step=10)
        seed = st.number_input("Random seed", min_value=0, max_value=10_000, value=42, step=1)

        st.markdown("### Disease prevalences")
        all_diseases = available_diseases()
        # Sensible defaults: highlight the most common ones.
        defaults = ["type_2_diabetes", "hypertension", "dyslipidemia", "obesity"]
        selected = st.multiselect(
            "Conditions to include",
            options=all_diseases,
            default=[d for d in defaults if d in all_diseases],
            format_func=disease_label,
        )

        prevalences: list[tuple[str, float]] = []
        for name in selected:
            label = disease_label(name)
            prev = st.slider(
                f"  {label}",
                min_value=0.0,
                max_value=1.0,
                value=0.4,
                step=0.05,
                key=f"prev_{name}",
                help=f"Probability that a patient has {label}.",
            )
            prevalences.append((name, prev))

    # ------------------------------------------------------------------
    # Generate
    # ------------------------------------------------------------------
    if not prevalences:
        callout(
            "Pick at least one condition from the sidebar to generate a "
            "cohort. The patients will still receive realistic "
            "demographics and biomarkers, just without diagnoses.",
            tone="info",
        )
        prevalences = []

    df = _generate_cohort(size, tuple(prevalences), int(seed))
    patients = _generate_patients(size, tuple(prevalences), int(seed))

    # Persist for downstream pages
    st.session_state["cohort_spec"] = {
        "size": size,
        "seed": int(seed),
        "diseases": prevalences,
    }
    st.session_state["cohort_patients"] = patients
    st.session_state["cohort_df"] = df

    # ------------------------------------------------------------------
    # Top metrics
    # ------------------------------------------------------------------
    section("At a glance")

    pct_female = (df["sex"] == "female").mean() * 100
    pct_with_dx = (df["disease_count"] > 0).mean() * 100
    metric_grid(
        [
            ("Patients", f"{len(df):,}", None, "primary"),
            ("Mean age", f"{df['age'].mean():.1f} y", f"sd {df['age'].std():.1f}", ""),
            ("Mean BMI", f"{df['bmi'].mean():.1f}", f"sd {df['bmi'].std():.1f}", "success"),
            ("Female", f"{pct_female:.0f}%", None, ""),
            (
                "With ≥1 diagnosis",
                f"{pct_with_dx:.0f}%",
                f"{int((df['disease_count'] > 0).sum())} / {len(df)}",
                "warning",
            ),
            (
                "Multimorbidity",
                f"{(df['disease_count'] >= 2).mean() * 100:.0f}%",
                "≥ 2 conditions",
                "danger" if (df["disease_count"] >= 2).mean() > 0.3 else "",
            ),
        ]
    )

    # ------------------------------------------------------------------
    # Charts
    # ------------------------------------------------------------------
    section("Distributions")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Age × sex**")
        st.plotly_chart(_age_histogram(df), use_container_width=True)
    with c2:
        st.markdown("**BMI distribution**")
        st.plotly_chart(_bmi_histogram(df), use_container_width=True)

    c3, c4 = st.columns([1.4, 1])
    with c3:
        st.markdown("**Diagnoses**")
        st.plotly_chart(_disease_bar(df), use_container_width=True)
    with c4:
        st.markdown("**BMI categories**")
        st.plotly_chart(_bmi_donut(df), use_container_width=True)

    # ------------------------------------------------------------------
    # Patient browser
    # ------------------------------------------------------------------
    section("Browse patients", meta=f"showing first 10 of {len(df)}")

    for _, row in df.head(10).iterrows():
        chips = [
            (disease_label(name), disease_chip_kind(name)) for name in row["diseases"]
        ]
        if not chips:
            chips = [("no diagnosis", "")]
        sex = "F" if row["sex"] == "female" else "M"
        initials = f"{sex}{row['id']+1:02d}"
        country = row["country"] if row["country"] != "—" else "syn"
        patient_card(
            initials=initials,
            sex=row["sex"],
            name=f"Patient #{row['id']+1:03d}",
            sub=(
                f"{row['age']} y · {row['sex']} · {country} · "
                f"BMI {row['bmi']:.1f} · {_bmi_category(row['bmi'])}"
            ),
            chips=chips,
        )

    # ------------------------------------------------------------------
    # Export
    # ------------------------------------------------------------------
    section("Export")

    export_df = df.copy()
    export_df["diseases"] = export_df["diseases"].apply(lambda xs: ";".join(xs))
    csv_bytes = export_df.to_csv(index=False).encode("utf-8")

    col_a, col_b = st.columns([1, 3])
    with col_a:
        st.download_button(
            label="📥 Download cohort (CSV)",
            data=csv_bytes,
            file_name=f"synthdiet_cohort_n{size}_seed{seed}.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True,
        )
    with col_b:
        st.markdown(
            "<div style='padding-top:6px; color:#475569; font-size:14px;'>"
            "The cohort is also available to the next pages (Diet Simulator, "
            "RCT Engine) without re-generation as long as you keep this tab "
            "open.</div>",
            unsafe_allow_html=True,
        )

    callout(
        "Move on to <strong>Diet Simulator</strong> in the sidebar to apply "
        "a preset diet to a single patient and watch their biomarkers evolve.",
        tone="success",
    )

    disclaimer()


if __name__ == "__main__":
    main()
