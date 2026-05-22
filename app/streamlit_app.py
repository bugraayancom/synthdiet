"""synthdiet · interactive Streamlit app — landing page.

Run locally with::

    streamlit run app/streamlit_app.py

Deploy on Streamlit Community Cloud by pointing it at this file. The
multi-page experience lives under ``app/pages/``; Streamlit will pick
the pages up automatically.
"""
from __future__ import annotations

import streamlit as st
from components import (
    callout,
    disclaimer,
    feature_grid,
    hero,
    page_setup,
    section,
)


def main() -> None:
    page_setup(title="Home", icon="🩺")

    hero(
        eyebrow="v0.1 · synthetic data for clinical nutrition",
        title_html=(
            "Stress-test "
            "<span class='accent'>diet interventions</span> "
            "on synthetic patients before they reach the clinic."
        ),
        subtitle=(
            "synthdiet ships a typed patient model, a registry of 25+ "
            "diseases, 8 ready-to-use diet presets and a full "
            "RCT / causal inference pipeline. This interface lets you "
            "explore every part of the library visually — without writing "
            "a single line of code."
        ),
        stats=[
            ("25+", "Disease registry"),
            ("19", "Drug–nutrient interactions"),
            ("8", "Preset diets"),
            ("5", "Validated RCTs"),
        ],
    )

    section("What can you do here?", meta="pick a page from the sidebar")

    feature_grid(
        [
            (
                "📋",
                "Build a cohort",
                "Adjust disease prevalences, see stratified distributions "
                "update in real time, and generate 10–500 patients with one click.",
            ),
            (
                "🍽️",
                "Apply a diet & simulate",
                "Pick one of 8 preset diets and follow biomarker trajectories "
                "for up to 24 weeks under the Hall 2011 body-composition model.",
            ),
            (
                "🧪",
                "Run a virtual RCT",
                "Set up a parallel-arm, stratified, Weibull-dropout trial end "
                "to end and analyse it with both ITT and per-protocol methods.",
            ),
            (
                "📚",
                "Practice on clinical cases",
                "Browse 15 ready-to-teach case studies and let an OSCE-style "
                "rubric grade student diet plans automatically.",
            ),
            (
                "📈",
                "Animated trajectories",
                "Watch HbA1c, blood pressure, LDL and weight evolve week by "
                "week with smooth Plotly animations.",
            ),
            (
                "🌐",
                "9-language documentation",
                "The same content is available in English, Türkçe, Español, "
                "Français, Deutsch, Português, Italiano, 中文 and 日本語.",
            ),
        ]
    )

    section("Start with a single Python call")

    st.markdown(
        "Even if no one is at the keyboard, this app showcases the full "
        "workflow. On the code side, a typical starter template looks like:"
    )

    st.code(
        '''from synthdiet import (
    CohortGenerator, CohortSpec, DiseaseSpec,
    DietSimulator, mediterranean_diet,
    evaluate_simulation, format_evaluation_report,
)

spec = CohortSpec(
    size=100,
    diseases=[
        DiseaseSpec("type_2_diabetes", prevalence=0.40),
        DiseaseSpec("hypertension",     prevalence=0.45),
    ],
)
cohort = CohortGenerator(spec, seed=42).generate()

sim = DietSimulator(adherence=0.85, engine="hall_2011")
diet = mediterranean_diet(daily_energy_kcal=1800)

result = sim.run(cohort[0], diet, duration_weeks=24)
print(format_evaluation_report(evaluate_simulation(result)))
''',
        language="python",
    )

    section("Quick links")

    cols = st.columns(3)
    cols[0].markdown(
        """
        **📦 Package**
        - [PyPI](https://pypi.org/project/synthdiet/)
        - [GitHub repository](https://github.com/bugraayancom/synthdiet)
        - [Releases](https://github.com/bugraayancom/synthdiet/releases)
        """
    )
    cols[1].markdown(
        """
        **📖 Docs**
        - [English](https://github.com/bugraayancom/synthdiet/tree/main/docs)
        - [Türkçe](https://github.com/bugraayancom/synthdiet/tree/main/docs/tr)
        - [All languages](https://github.com/bugraayancom/synthdiet/tree/main/docs)
        """
    )
    cols[2].markdown(
        """
        **👤 Author**
        - [bugraayan.com](https://bugraayan.com)
        - [Email](mailto:bugraayan.com@gmail.com)
        - [Google Scholar](https://scholar.google.com/citations?user=VHGqzNMAAAAJ&hl=tr)
        """
    )

    callout(
        "Start with <strong>Cohort Builder</strong> from the sidebar, then "
        "move to <strong>Diet Simulator</strong> and "
        "<strong>RCT Engine</strong> to run a full virtual study.",
        tone="info",
    )

    disclaimer()


if __name__ == "__main__":
    main()
