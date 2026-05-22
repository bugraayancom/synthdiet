"""Case Studies page.

Browse the 15 built-in clinical case studies, inspect each in detail
and grade a student diet plan with the OSCE-style rubric.
"""
from __future__ import annotations

import sys
from pathlib import Path

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
    render_html,
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
from synthdiet.education import (  # noqa: E402
    OSCEStation,
    built_in_cases,
    get_case,
)

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

DIFFICULTY_TONE = {
    "introductory": "success",
    "intermediate": "warning",
    "advanced": "danger",
}


def _difficulty_chip(difficulty: str) -> str:
    tone = DIFFICULTY_TONE.get(difficulty.lower(), "")
    cls = {
        "success": "background:#D1FAE5;color:#065F46;",
        "warning": "background:#FEF3C7;color:#92400E;",
        "danger": "background:#FEE2E2;color:#991B1B;",
    }.get(tone, "background:#F1F5F9;color:#475569;")
    return (
        f'<span style="display:inline-block;padding:3px 10px;border-radius:999px;'
        f'font-size:11px;font-weight:600;{cls}">{difficulty}</span>'
    )


def main() -> None:
    page_setup(title="Case Studies", icon="📚")

    hero(
        eyebrow="step 4 · clinical teaching",
        title_html=(
            "15 ready-to-teach "
            "<span class='accent'>clinical scenarios</span> "
            "with OSCE grading."
        ),
        subtitle=(
            "Browse the built-in case library, share a Markdown handout "
            "with students and let an OSCE-style rubric automatically grade "
            "the diet plans they submit."
        ),
    )

    cases = built_in_cases()

    # ------------------------------------------------------------------
    # Overview metrics
    # ------------------------------------------------------------------
    section("Library overview")

    diff_counts: dict[str, int] = {}
    for c in cases:
        diff_counts[c.difficulty] = diff_counts.get(c.difficulty, 0) + 1

    avg_minutes = sum(c.estimated_minutes for c in cases) / max(1, len(cases))

    metric_grid(
        [
            ("Cases", str(len(cases)), "built-in", "primary"),
            (
                "Introductory",
                str(diff_counts.get("introductory", 0)),
                None,
                "success",
            ),
            (
                "Intermediate",
                str(diff_counts.get("intermediate", 0)),
                None,
                "warning",
            ),
            (
                "Advanced",
                str(diff_counts.get("advanced", 0)),
                None,
                "danger",
            ),
            ("Avg duration", f"{avg_minutes:.0f} min", "per case", ""),
            ("Tags", str(len({t for c in cases for t in c.tags})), "unique tags", ""),
        ]
    )

    # ------------------------------------------------------------------
    # Case picker
    # ------------------------------------------------------------------
    section("Pick a case")

    with st.sidebar:
        st.markdown("### Case filter")
        difficulty_filter = st.multiselect(
            "Difficulty",
            options=["introductory", "intermediate", "advanced"],
            default=["introductory", "intermediate", "advanced"],
        )
        all_tags = sorted({t for c in cases for t in c.tags})
        tag_filter = st.multiselect("Tags", options=all_tags, default=[])

    filtered: list = []
    for c in cases:
        if difficulty_filter and c.difficulty not in difficulty_filter:
            continue
        if tag_filter and not any(t in c.tags for t in tag_filter):
            continue
        filtered.append(c)

    if not filtered:
        callout(
            "No cases match the current filter — broaden the difficulty or "
            "tag selection in the sidebar.",
            tone="warning",
        )
        st.stop()

    # Render case cards in grid
    cols = st.columns(2)
    for i, c in enumerate(filtered):
        with cols[i % 2]:
            tags_html = "".join(
                f'<span class="sd-chip">{t}</span>' for t in sorted(c.tags)[:5]
            )
            render_html(
                f"""
                <div class="sd-feature" style="animation-delay:{i*0.04}s;">
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <div style="font-size:13px; font-weight:700; color:#0284C7; font-family:'JetBrains Mono', monospace;">
                      {c.case_id}
                    </div>
                    {_difficulty_chip(c.difficulty)}
                  </div>
                  <h3>{c.title}</h3>
                  <p>{c.chief_complaint}</p>
                  <div style="margin-top:12px;">{tags_html}</div>
                  <div style="font-size:12px; color:#94A3B8; margin-top:10px;">
                    ⏱ {c.estimated_minutes} min · {len(c.learning_objectives)} learning objectives
                  </div>
                </div>
                """
            )
            if st.button(
                f"Open {c.case_id} →",
                key=f"open_{c.case_id}",
                use_container_width=True,
            ):
                st.session_state.selected_case = c.case_id

    # ------------------------------------------------------------------
    # Detail
    # ------------------------------------------------------------------
    selected_id = st.session_state.get("selected_case")
    if not selected_id:
        callout(
            "Open a case from the cards above to see its full handout, "
            "reference solution and OSCE grading station.",
            tone="info",
        )
        disclaimer()
        return

    case = get_case(selected_id)

    section(f"Case detail · {case.case_id}", meta=case.title)

    detail_tabs = st.tabs(
        ["📋 Handout", "✅ Reference solution", "🎓 OSCE grader"]
    )

    with detail_tabs[0]:
        st.markdown(case.as_markdown())

    with detail_tabs[1]:
        ref = case.reference_solution
        st.markdown(f"### Summary\n\n{ref.summary}")
        st.markdown("### Rationale")
        st.markdown(ref.rationale)
        st.markdown("### Prescribed diet")
        st.code(ref.prescribed_diet.summary(), language="text")
        st.markdown(
            f"### Expected outcomes (over {ref.follow_up_weeks} weeks)"
        )
        for outcome in ref.expected_outcomes:
            st.markdown(f"- {outcome}")

    with detail_tabs[2]:
        st.markdown(
            "Submit a student diet plan and let the rubric grade it. "
            "Pick one of the preset diets to demo:"
        )
        presets = list_presets()
        col_d, col_k = st.columns([2, 1])
        with col_d:
            diet_name = st.selectbox(
                "Student diet",
                options=presets,
                format_func=lambda k: DIET_META.get(k, {}).get("name", k),
                key="osce_diet",
            )
        with col_k:
            kcal = st.number_input(
                "Daily energy (kcal)", 1200, 2800, 1700, step=50, key="osce_kcal"
            )

        if st.button("🎓 Grade plan", type="primary", use_container_width=True):
            student_diet = DIET_CONSTRUCTORS[diet_name](daily_energy_kcal=int(kcal))
            station = OSCEStation(case=case)
            score = station.grade(student_diet)

            total_pts = getattr(score, "total", None)
            max_pts = getattr(score, "max_points", None)
            if total_pts is None and hasattr(score, "scored"):
                total_pts = sum(s.points for s in score.scored)
            if max_pts is None and hasattr(score, "scored"):
                max_pts = sum(s.max_points for s in score.scored)

            pct = (total_pts / max_pts * 100) if (total_pts and max_pts) else 0
            tone = (
                "success" if pct >= 80
                else "warning" if pct >= 50
                else "danger"
            )
            metric_grid(
                [
                    ("Score", f"{total_pts:.1f} / {max_pts:.1f}", f"{pct:.0f}%", tone),
                ]
            )
            st.code(score.pretty(), language="text")

    if st.button("← Back to library"):
        st.session_state.selected_case = None
        st.rerun()

    disclaimer()


if __name__ == "__main__":
    main()
