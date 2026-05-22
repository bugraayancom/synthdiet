"""Diet Simulator page.

Pick a synthetic patient, apply a preset diet and simulate the
trajectory of their biomarkers with animated Plotly charts.
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
    disease_chip_kind,
    disease_label,
    hero,
    metric_grid,
    page_setup,
    section,
)

from synthdiet import (  # noqa: E402
    DietSimulator,
    evaluate_simulation,
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

PRIMARY = "#0EA5E9"
PRIMARY_STRONG = "#0284C7"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"
GRID = "#E2E8F0"

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
        transition=dict(duration=400, easing="cubic-in-out"),
    )
    fig.update_xaxes(gridcolor=GRID, zeroline=False, linecolor=GRID)
    fig.update_yaxes(gridcolor=GRID, zeroline=False, linecolor=GRID)
    return fig


# ---------------------------------------------------------------------------
# Animated trajectory chart
# ---------------------------------------------------------------------------
PRIMARY_OUTCOMES = {
    "weight_kg": ("Weight", "kg", PRIMARY_STRONG),
    "bm_hba1c_pct": ("HbA1c", "%", DANGER),
    "bm_systolic_bp_mmhg": ("Systolic BP", "mmHg", "#7C3AED"),
    "bm_ldl_mg_dl": ("LDL cholesterol", "mg/dL", WARNING),
    "bm_fasting_glucose_mg_dl": ("Fasting glucose", "mg/dL", "#F472B6"),
    "bm_triglycerides_mg_dl": ("Triglycerides", "mg/dL", "#22D3EE"),
}


def _animated_trajectory(
    df: pd.DataFrame,
    metric: str,
    label: str,
    unit: str,
    colour: str,
) -> go.Figure:
    """Build a frame-animated trace that draws the line week by week."""
    weeks = df["week"].tolist()
    values = df[metric].tolist()

    if not weeks or len(weeks) < 2:
        fig = go.Figure()
        fig.add_annotation(text="No data to plot", showarrow=False)
        return _polish(fig, height=320)

    # Frames: progressively reveal more points.
    frames = []
    for i in range(1, len(weeks) + 1):
        sub_w = weeks[:i]
        sub_v = values[:i]
        frames.append(
            go.Frame(
                name=str(weeks[i - 1]),
                data=[
                    go.Scatter(
                        x=sub_w,
                        y=sub_v,
                        mode="lines+markers",
                        line=dict(color=colour, width=3, shape="spline", smoothing=0.9),
                        marker=dict(size=7, color=colour, line=dict(color="white", width=2)),
                        fill="tozeroy",
                        fillcolor=f"rgba({_rgb(colour)}, 0.10)",
                        hovertemplate=(
                            f"<b>Week %{{x}}</b><br>{label}: %{{y:.2f}} {unit}<extra></extra>"
                        ),
                        showlegend=False,
                    ),
                ],
            )
        )

    fig = go.Figure(
        data=[
            go.Scatter(
                x=[weeks[0]],
                y=[values[0]],
                mode="lines+markers",
                line=dict(color=colour, width=3, shape="spline", smoothing=0.9),
                marker=dict(size=7, color=colour, line=dict(color="white", width=2)),
                fill="tozeroy",
                fillcolor=f"rgba({_rgb(colour)}, 0.10)",
                showlegend=False,
            )
        ],
        frames=frames,
    )

    # Reference baseline line
    fig.add_hline(
        y=values[0],
        line_color="#CBD5E1",
        line_dash="dot",
        line_width=1,
        annotation_text="baseline",
        annotation_position="bottom right",
        annotation_font_color="#64748B",
        annotation_font_size=11,
    )

    # Y-axis padding
    y_min = min(values) * 0.96
    y_max = max(values) * 1.04
    fig.update_yaxes(range=[y_min, y_max], title=f"{label} ({unit})")
    fig.update_xaxes(range=[0, max(weeks) + 1], title="Week")

    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                x=0.0,
                y=1.18,
                xanchor="left",
                yanchor="top",
                pad=dict(r=4, t=0),
                buttons=[
                    dict(
                        label="▶  Play",
                        method="animate",
                        args=[
                            None,
                            dict(
                                frame=dict(duration=120, redraw=True),
                                fromcurrent=True,
                                transition=dict(duration=80, easing="cubic-in-out"),
                                mode="immediate",
                            ),
                        ],
                    ),
                    dict(
                        label="⏸  Pause",
                        method="animate",
                        args=[
                            [None],
                            dict(
                                frame=dict(duration=0, redraw=False),
                                mode="immediate",
                                transition=dict(duration=0),
                            ),
                        ],
                    ),
                ],
            )
        ],
    )
    return _polish(fig, height=380)


def _rgb(hex_colour: str) -> str:
    h = hex_colour.lstrip("#")
    return f"{int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}"


def _multi_metric_chart(df: pd.DataFrame, metrics: list[str]) -> go.Figure:
    """Compact multi-metric chart with normalised values (0-100% of baseline)."""
    fig = go.Figure()
    palette = [PRIMARY_STRONG, DANGER, "#7C3AED", WARNING, "#F472B6", "#22D3EE"]
    for i, metric in enumerate(metrics):
        if metric not in df.columns or df[metric].iloc[0] == 0:
            continue
        baseline = df[metric].iloc[0]
        rel = (df[metric] / baseline) * 100.0
        label = PRIMARY_OUTCOMES.get(metric, (metric, "", PRIMARY))[0]
        fig.add_trace(
            go.Scatter(
                x=df["week"],
                y=rel,
                mode="lines+markers",
                name=label,
                line=dict(color=palette[i % len(palette)], width=2.5, shape="spline"),
                marker=dict(size=5),
                hovertemplate=f"<b>{label}</b><br>Week %{{x}}: %{{y:.1f}} %<extra></extra>",
            )
        )
    fig.add_hline(
        y=100,
        line_color="#94A3B8",
        line_dash="dash",
        line_width=1,
    )
    fig.update_xaxes(title="Week")
    fig.update_yaxes(title="% of baseline")
    return _polish(fig, height=340)


# ---------------------------------------------------------------------------
# Diet preset gallery
# ---------------------------------------------------------------------------
def _diet_gallery(selected: str) -> str:
    """Render diet preset cards. Returns the (possibly new) selection."""
    presets = list_presets()
    cols = st.columns(4)
    for i, name in enumerate(presets):
        meta = DIET_META.get(name, {"emoji": "🥘", "name": name, "desc": ""})
        is_selected = name == selected
        with cols[i % 4]:
            cls = "selected" if is_selected else ""
            st.markdown(
                f"""
                <div class="sd-diet-card {cls}">
                  <span class="emoji">{meta['emoji']}</span>
                  <div class="name">{meta['name']}</div>
                  <div class="desc">{meta['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                "Selected ✓" if is_selected else "Select",
                key=f"diet_{name}",
                use_container_width=True,
                type="primary" if is_selected else "secondary",
            ):
                return name
    return selected


# ---------------------------------------------------------------------------
# Cached simulation
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def _run_simulation(
    cohort_signature: tuple[Any, ...],
    patient_idx: int,
    diet_name: str,
    daily_kcal: int,
    duration_weeks: int,
    adherence: float,
    engine: str,
    sampling_weeks: int,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Run a simulation. ``cohort_signature`` is used only for cache invalidation."""
    patients = st.session_state.get("cohort_patients")
    if not patients:
        return pd.DataFrame(), {}
    patient = patients[patient_idx]
    diet = DIET_CONSTRUCTORS[diet_name](daily_energy_kcal=daily_kcal)
    sim = DietSimulator(
        adherence=adherence,
        sampling_weeks=sampling_weeks,
        engine=engine,
    )
    result = sim.run(patient, diet, duration_weeks=duration_weeks)
    df = result.as_dataframe()
    evaluation = evaluate_simulation(result)
    summary = {
        "weight_change_kg": result.weight_change_kg,
        "duration_weeks": duration_weeks,
        "evaluation": str(evaluation),
    }
    return df, summary


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    page_setup(title="Diet Simulator", icon="🍽️")

    hero(
        eyebrow="step 2 · simulate one patient",
        title_html=(
            "Watch the diet "
            "<span class='accent'>reshape biomarkers</span> "
            "week by week."
        ),
        subtitle=(
            "Pick a patient from your cohort, choose a preset diet and let "
            "the Hall 2011 body-composition model project weight, glucose, "
            "blood pressure and lipids for up to 24 weeks."
        ),
    )

    # ------------------------------------------------------------------
    # Guardrail: must have a cohort first
    # ------------------------------------------------------------------
    patients = st.session_state.get("cohort_patients")
    df_cohort = st.session_state.get("cohort_df")
    if not patients or df_cohort is None or df_cohort.empty:
        callout(
            "You need to generate a cohort first. Open "
            "<strong>Cohort Builder</strong> from the sidebar, configure "
            "your synthetic population, then return here.",
            tone="warning",
        )
        st.stop()

    # ------------------------------------------------------------------
    # Sidebar controls
    # ------------------------------------------------------------------
    with st.sidebar:
        st.markdown("### Simulation settings")

        labels = []
        for _, row in df_cohort.iterrows():
            dx = ", ".join(disease_label(d) for d in row["diseases"]) or "no dx"
            labels.append(
                f"#{int(row['id'])+1:03d} · {row['age']}y {row['sex'][0].upper()} · "
                f"BMI {row['bmi']:.1f} · {dx}"
            )
        patient_idx = st.selectbox(
            "Patient",
            options=list(range(len(df_cohort))),
            format_func=lambda i: labels[i],
            index=0,
        )

        duration_weeks = st.slider("Duration (weeks)", 4, 52, 24, step=4)
        daily_kcal = st.slider("Daily energy (kcal)", 1200, 2800, 1800, step=100)
        adherence = st.slider("Adherence", 0.4, 1.0, 0.85, step=0.05)
        engine = st.radio(
            "Engine",
            options=["hall_2011", "simple"],
            format_func=lambda x: {
                "hall_2011": "Hall 2011 (recommended)",
                "simple": "Simple energy balance",
            }[x],
        )
        sampling = st.select_slider(
            "Sampling cadence", options=[1, 2, 4], value=2,
            format_func=lambda v: f"every {v}w",
        )

    # ------------------------------------------------------------------
    # Diet selection
    # ------------------------------------------------------------------
    section("Choose a diet")

    if "selected_diet" not in st.session_state:
        st.session_state.selected_diet = "mediterranean"
    new_selection = _diet_gallery(st.session_state.selected_diet)
    if new_selection != st.session_state.selected_diet:
        st.session_state.selected_diet = new_selection
        st.rerun()
    diet_name = st.session_state.selected_diet
    diet_meta = DIET_META.get(diet_name, {"emoji": "🥘", "name": diet_name})

    # ------------------------------------------------------------------
    # Patient summary
    # ------------------------------------------------------------------
    patient_row = df_cohort.iloc[int(patient_idx)]
    chips_html = "".join(
        f'<span class="sd-chip {disease_chip_kind(d)}">{disease_label(d)}</span>'
        for d in patient_row["diseases"]
    )
    if not chips_html:
        chips_html = '<span class="sd-chip">no diagnosis</span>'
    sex_cls = "f" if patient_row["sex"] == "female" else "m"

    section("Patient & plan", meta=f"diet: {diet_meta['name']}")
    col_a, col_b = st.columns([1.2, 1])
    with col_a:
        st.markdown(
            f"""
            <div class="sd-patient-card" style="margin-bottom:14px;">
              <div class="sd-avatar {sex_cls}">P{int(patient_row['id'])+1:02d}</div>
              <div class="sd-patient-meta">
                <div class="name">Patient #{int(patient_row['id'])+1:03d}</div>
                <div class="sub">
                  {int(patient_row['age'])} y · {patient_row['sex']} ·
                  height {patient_row['height_cm']:.0f} cm ·
                  weight {patient_row['weight_kg']:.1f} kg ·
                  BMI {patient_row['bmi']:.1f}
                </div>
              </div>
              <div>{chips_html}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_b:
        st.markdown(
            f"""
            <div class="sd-feature" style="animation:none;">
              <div class="sd-feature-icon">{diet_meta['emoji']}</div>
              <h3>{diet_meta['name']}</h3>
              <p style="margin-bottom:10px;">{diet_meta.get('desc', '')}</p>
              <div style="font-size:12px; color:#475569;">
                {daily_kcal} kcal/day · {duration_weeks} weeks ·
                adherence {adherence:.0%} · engine: {engine}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ------------------------------------------------------------------
    # Run simulation
    # ------------------------------------------------------------------
    with st.spinner("Simulating…"):
        df, summary = _run_simulation(
            cohort_signature=(
                st.session_state.get("cohort_spec", {}).get("seed"),
                len(df_cohort),
                tuple(st.session_state.get("cohort_spec", {}).get("diseases", [])),
                int(patient_idx),
                diet_name,
                int(daily_kcal),
                int(duration_weeks),
                float(adherence),
                engine,
                int(sampling),
            ),
            patient_idx=int(patient_idx),
            diet_name=diet_name,
            daily_kcal=int(daily_kcal),
            duration_weeks=int(duration_weeks),
            adherence=float(adherence),
            engine=engine,
            sampling_weeks=int(sampling),
        )

    if df.empty:
        callout("Simulation produced no data points.", tone="warning")
        st.stop()

    # ------------------------------------------------------------------
    # Summary metrics
    # ------------------------------------------------------------------
    section("Results", meta=f"{duration_weeks} weeks elapsed")

    # Compute key deltas
    def _delta(col: str) -> tuple[float, float]:
        if col not in df.columns:
            return 0.0, 0.0
        first = df[col].iloc[0]
        last = df[col].iloc[-1]
        if first == 0:
            return last - first, 0.0
        return last - first, (last - first) / first * 100

    dw, _ = _delta("weight_kg")
    dh, dh_pct = _delta("bm_hba1c_pct")
    dl, dl_pct = _delta("bm_ldl_mg_dl")
    ds, _ = _delta("bm_systolic_bp_mmhg")
    df_glu, df_glu_pct = _delta("bm_fasting_glucose_mg_dl")

    metric_grid(
        [
            (
                "Δ Weight",
                f"{dw:+.1f} kg",
                f"final {df['weight_kg'].iloc[-1]:.1f} kg",
                "primary" if dw < 0 else "warning",
            ),
            (
                "Δ HbA1c",
                f"{dh:+.2f} %",
                f"{dh_pct:+.1f}%",
                "success" if dh < 0 else "danger",
            ),
            (
                "Δ LDL",
                f"{dl:+.0f} mg/dL",
                f"{dl_pct:+.1f}%",
                "success" if dl < 0 else "danger",
            ),
            (
                "Δ Systolic BP",
                f"{ds:+.1f} mmHg",
                None,
                "success" if ds < 0 else "danger",
            ),
            (
                "Δ Fasting glucose",
                f"{df_glu:+.0f} mg/dL",
                f"{df_glu_pct:+.1f}%",
                "success" if df_glu < 0 else "danger",
            ),
            (
                "Adherence",
                f"{df['adherence'].mean():.0%}",
                f"avg over {duration_weeks} w",
                "",
            ),
        ]
    )

    # ------------------------------------------------------------------
    # Animated trajectories
    # ------------------------------------------------------------------
    section("Animated trajectories", meta="press ▶ Play in any chart")

    metric_choice = st.radio(
        "Outcome",
        options=list(PRIMARY_OUTCOMES.keys()),
        horizontal=True,
        format_func=lambda k: PRIMARY_OUTCOMES[k][0],
        key="trajectory_metric",
    )
    label, unit, colour = PRIMARY_OUTCOMES[metric_choice]
    if metric_choice in df.columns:
        st.plotly_chart(
            _animated_trajectory(df, metric_choice, label, unit, colour),
            use_container_width=True,
        )
    else:
        callout(f"<strong>{label}</strong> not present in this simulation.", tone="warning")

    # ------------------------------------------------------------------
    # Multi-metric overview
    # ------------------------------------------------------------------
    section("All key outcomes (% of baseline)")

    available = [m for m in PRIMARY_OUTCOMES.keys() if m in df.columns]
    st.plotly_chart(_multi_metric_chart(df, available), use_container_width=True)

    # ------------------------------------------------------------------
    # Raw data
    # ------------------------------------------------------------------
    with st.expander("Raw simulation dataframe"):
        st.dataframe(df, use_container_width=True, height=320)

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    col_dl, col_text = st.columns([1, 3])
    with col_dl:
        st.download_button(
            "📥 Download trajectory (CSV)",
            data=csv_bytes,
            file_name=(
                f"synthdiet_sim_p{int(patient_idx)+1:03d}_{diet_name}_"
                f"{duration_weeks}w.csv"
            ),
            mime="text/csv",
            type="primary",
            use_container_width=True,
        )
    with col_text:
        st.markdown(
            "<div style='padding-top:6px; color:#475569; font-size:14px;'>"
            "Move on to <strong>RCT Engine</strong> to compare two diets "
            "across the entire cohort with a randomised controlled design."
            "</div>",
            unsafe_allow_html=True,
        )

    disclaimer()


if __name__ == "__main__":
    main()
