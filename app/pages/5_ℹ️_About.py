"""About page — credits, links and project metadata."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(APP_DIR))

from components import (  # noqa: E402
    callout,
    disclaimer,
    feature_grid,
    hero,
    page_setup,
    section,
)


def main() -> None:
    page_setup(title="About", icon="ℹ️")

    hero(
        eyebrow="about · synthdiet",
        title_html=(
            "An open-source library for "
            "<span class='accent'>clinical-nutrition research</span>."
        ),
        subtitle=(
            "synthdiet is a Python toolkit for generating synthetic patients "
            "with realistic clinical conditions and simulating dietary "
            "interventions on them. This Streamlit app showcases every "
            "module visually."
        ),
    )

    section("Author")

    st.markdown(
        """
        **Buğra Ayan** — Ankara / Türkiye

        - 🌐 [bugraayan.com](https://bugraayan.com)
        - ✉️ [bugraayan.com@gmail.com](mailto:bugraayan.com@gmail.com)
        - 🎓 [Google Scholar](https://scholar.google.com/citations?user=VHGqzNMAAAAJ&hl=tr)
        - 🐙 [GitHub](https://github.com/bugraayancom)
        """
    )

    section("What's inside the library")

    feature_grid(
        [
            ("👤", "Patient model", "Typed dataclass aggregating demographics, anthropometrics, biomarkers, lifestyle, diagnoses and current medications."),
            ("🩺", "25+ diseases", "Endocrine, cardiovascular, renal, hepatic, GI, metabolic, musculoskeletal, oncologic, psychiatric and allergy categories."),
            ("💊", "19 drug interactions", "Clinically important drug-nutrient pairs (metformin → B12, statins → grapefruit, warfarin → vitamin K, etc.)."),
            ("🧬", "5 cohort generators", "Random, distribution-based, copula-based, cohort-from-spec and Markov progression."),
            ("⚖️", "Hall 2011 model", "Optional body-composition engine with Forbes partition and adaptive thermogenesis."),
            ("🧪", "RCT engine", "Parallel-arm, crossover and 2×2 factorial designs with stratified / block / minimisation randomisation and ITT/PP/AT analyses."),
            ("🔗", "Causal inference", "Counterfactual simulation, ATE/CATE, propensity-confounding experiments with IPTW and g-formula."),
            ("📏", "Diet quality indices", "HEI-2020, AHEI-2010, MEDAS, DASH, PHDI, DII."),
            ("📈", "Statistics & noise", "Power analysis, bootstrap CI, permutation tests, FDR/Holm, ANCOVA, MCAR/MAR/MNAR injection."),
            ("📚", "15 case studies + OSCE", "Built-in clinical scenarios with automated rubric grading."),
            ("✅", "Validation suite", "Calibrated against DASH-Sodium, PREDIMED, DiRECT, Look AHEAD and DPP."),
            ("🌐", "9-language docs", "English, Türkçe, Español, Français, Deutsch, Português, Italiano, 中文 and 日本語."),
        ]
    )

    section("Citation")

    st.markdown(
        "If you use `synthdiet` in academic work, please cite it via "
        "[`CITATION.cff`](https://github.com/bugraayancom/synthdiet/blob/main/CITATION.cff) "
        "or with the BibTeX entry below:"
    )

    st.code(
        """@software{ayan_synthdiet_2026,
  author  = {Buğra Ayan},
  title   = {synthdiet: A Python library for simulating diets on synthetic patients},
  year    = {2026},
  version = {0.1.0},
  url     = {https://bugraayan.com}
}""",
        language="bibtex",
    )

    section("This Streamlit app")

    st.markdown(
        """
        - **Source**: [`app/`](https://github.com/bugraayancom/synthdiet/tree/main/app)
          inside the main repository.
        - **Stack**: Streamlit + Plotly + custom CSS, integrating directly with
          the synthdiet Python library.
        - **Run locally**:
          ```bash
          pip install "synthdiet[app]"
          streamlit run app/streamlit_app.py
          ```
        - **Deploy**: drop the repo into Streamlit Community Cloud and point
          it at `app/streamlit_app.py`.
        """
    )

    callout(
        "synthdiet is licensed under MIT. Issues and pull requests are "
        "welcome at "
        "<a href='https://github.com/bugraayancom/synthdiet'>github.com/bugraayancom/synthdiet</a>.",
        tone="info",
    )

    disclaimer()


if __name__ == "__main__":
    main()
