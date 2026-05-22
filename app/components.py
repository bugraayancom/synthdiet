"""Reusable UI building blocks for the synthdiet Streamlit app.

All components are pure-Python helpers that emit HTML/CSS via
``st.markdown(..., unsafe_allow_html=True)``. Every HTML chunk is run
through :func:`textwrap.dedent` + ``strip`` first; without that the
common 4-space indentation in source-level f-strings would be parsed as
a Markdown code block by Streamlit's renderer.
"""
from __future__ import annotations

import html
import textwrap
from collections.abc import Iterable, Sequence
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parent
STYLE_PATH = APP_DIR / "style.css"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------
def _html(markup: str, *, sidebar: bool = False) -> None:
    """Render an arbitrary HTML chunk safely.

    Strips common leading whitespace before passing to Streamlit so the
    Markdown engine doesn't interpret indentation as a code block.
    """
    cleaned = textwrap.dedent(markup).strip()
    target = st.sidebar if sidebar else st
    target.markdown(cleaned, unsafe_allow_html=True)


def render_html(markup: str) -> None:
    """Public helper: dedent + strip a multi-line HTML block, then render.

    Use this from page modules instead of ``st.markdown(html, unsafe_allow_html=True)``
    when the HTML is built from a triple-quoted f-string with leading
    indentation — Streamlit's Markdown parser would otherwise treat the
    4-space indent as a fenced code block.
    """
    _html(markup)


def inject_global_styles() -> None:
    """Inject the project-wide CSS once per page run."""
    css = STYLE_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def page_setup(
    *,
    title: str,
    icon: str = "🩺",
    layout: str = "wide",
    sidebar_state: str = "expanded",
) -> None:
    """Set common Streamlit page config and inject styles."""
    st.set_page_config(
        page_title=f"{title} · synthdiet",
        page_icon=icon,
        layout=layout,
        initial_sidebar_state=sidebar_state,
    )
    inject_global_styles()
    _sidebar_brand()


def _sidebar_brand() -> None:
    """Render a small branded header in the sidebar."""
    _html(
        """
        <div style="padding: 14px 4px 18px 4px; border-bottom: 1px solid var(--sd-border); margin-bottom: 8px;">
          <div style="display:flex; align-items:center; gap:10px;">
            <div style="width:34px; height:34px; border-radius:10px; background: linear-gradient(135deg, #0EA5E9, #10B981); display:flex; align-items:center; justify-content:center; color:white; font-weight:800; font-size:14px;">sd</div>
            <div>
              <div style="font-weight:800; font-size:15px; letter-spacing:-0.01em;">synthdiet</div>
              <div style="font-size:11px; color: var(--sd-text-muted);">synthetic patients · diet simulation</div>
            </div>
          </div>
        </div>
        """,
        sidebar=True,
    )


# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
def hero(
    *,
    eyebrow: str,
    title_html: str,
    subtitle: str,
    stats: Sequence[tuple[str, str]] | None = None,
) -> None:
    """Render the home-page hero block.

    ``title_html`` may include a ``<span class="accent">...</span>`` to colour
    a portion of the title with the brand gradient.
    """
    stats_html = ""
    if stats:
        stat_items = "".join(
            f'<div class="sd-hero-stat"><div class="num">{html.escape(num)}</div>'
            f'<div class="label">{html.escape(label)}</div></div>'
            for num, label in stats
        )
        stats_html = f'<div class="sd-hero-stats">{stat_items}</div>'

    _html(
        f"""
        <div class="sd-hero">
        <span class="sd-hero-eyebrow"><span class="pulse"></span>{html.escape(eyebrow)}</span>
        <h1 class="sd-hero-title">{title_html}</h1>
        <p class="sd-hero-sub">{html.escape(subtitle)}</p>
        {stats_html}
        </div>
        """
    )


# ---------------------------------------------------------------------------
# Section header
# ---------------------------------------------------------------------------
def section(title: str, meta: str | None = None) -> None:
    meta_html = f'<span class="meta">{html.escape(meta)}</span>' if meta else ""
    _html(
        f"""
        <div class="sd-section-header">
        <h2>{html.escape(title)}</h2>
        {meta_html}
        </div>
        """
    )


# ---------------------------------------------------------------------------
# Feature grid
# ---------------------------------------------------------------------------
def feature_grid(features: Iterable[tuple[str, str, str]]) -> None:
    """Render a responsive grid of feature cards.

    Each tuple is ``(icon, title, description)``.
    """
    cards = "".join(
        (
            f'<div class="sd-feature">'
            f'<div class="sd-feature-icon">{icon}</div>'
            f'<h3>{html.escape(title)}</h3>'
            f'<p>{html.escape(desc)}</p>'
            f'</div>'
        )
        for icon, title, desc in features
    )
    _html(f'<div class="sd-feature-grid">{cards}</div>')


# ---------------------------------------------------------------------------
# Metric grid
# ---------------------------------------------------------------------------
def metric_grid(items: Sequence[tuple[str, str, str | None, str]]) -> None:
    """Render a grid of metric cards.

    Each tuple is ``(label, value, trend_text_or_None, tone)`` where ``tone``
    is one of ``"primary" | "success" | "warning" | "danger" | ""``.
    """
    parts = []
    for label, value, trend, tone in items:
        tone_cls = f" tone-{tone}" if tone else ""
        trend_html = ""
        if trend:
            cls = "flat"
            if trend.startswith("+") or trend.lower().startswith("↑"):
                cls = "pos"
            elif trend.startswith("-") or trend.lower().startswith("↓"):
                cls = "neg"
            trend_html = f'<div class="trend {cls}">{html.escape(trend)}</div>'
        parts.append(
            f'<div class="sd-metric{tone_cls}">'
            f'<div class="label">{html.escape(label)}</div>'
            f'<div class="value">{html.escape(value)}</div>'
            f'{trend_html}'
            f'</div>'
        )
    _html(f'<div class="sd-metric-grid">{"".join(parts)}</div>')


# ---------------------------------------------------------------------------
# Patient card
# ---------------------------------------------------------------------------
def patient_card(
    *,
    initials: str,
    sex: str,
    name: str,
    sub: str,
    chips: Iterable[tuple[str, str]] = (),
) -> None:
    """Render a single patient row card."""
    sex_cls = "f" if sex.lower().startswith("f") else "m"
    chips_html = "".join(
        f'<span class="sd-chip {html.escape(kind)}">{html.escape(label)}</span>'
        for label, kind in chips
    )
    _html(
        f"""
        <div class="sd-patient-card">
        <div class="sd-avatar {sex_cls}">{html.escape(initials)}</div>
        <div class="sd-patient-meta">
        <div class="name">{html.escape(name)}</div>
        <div class="sub">{html.escape(sub)}</div>
        </div>
        <div>{chips_html}</div>
        </div>
        """
    )


# ---------------------------------------------------------------------------
# Callouts
# ---------------------------------------------------------------------------
def callout(text_html: str, tone: str = "info") -> None:
    cls = {"info": "", "warning": " warning", "success": " success"}.get(tone, "")
    _html(f'<div class="sd-callout{cls}">{text_html}</div>')


# ---------------------------------------------------------------------------
# Disclaimer
# ---------------------------------------------------------------------------
def disclaimer() -> None:
    _html(
        """
        <div class="sd-disclaimer">
        <strong>Disclaimer.</strong>
        <code>synthdiet</code> is a research and teaching tool.
        The patients generated in this interface are <strong>not real</strong>;
        the numbers shown <strong>cannot be used as clinical recommendations</strong>.
        For patient care always consult a qualified registered dietitian.
        </div>
        """
    )


# ---------------------------------------------------------------------------
# ECG / pulse waveform (decorative)
# ---------------------------------------------------------------------------
def ecg_waveform() -> None:
    _html(
        """
        <svg class="sd-ecg" viewBox="0 0 600 60" preserveAspectRatio="none">
        <path class="sd-ecg-path" d="M0,30 L80,30 L100,30 L110,10 L120,50 L130,30 L200,30 L220,30 L230,15 L240,45 L250,30 L320,30 L340,30 L350,5 L360,55 L370,30 L600,30"/>
        </svg>
        """
    )


# ---------------------------------------------------------------------------
# Diet preset descriptions
# ---------------------------------------------------------------------------
DIET_META: dict[str, dict[str, str]] = {
    "mediterranean": {
        "emoji": "🫒",
        "name": "Mediterranean",
        "desc": "Olive oil, fish, whole grains and vegetables; classic cardio-protective diet.",
    },
    "dash": {
        "emoji": "🥗",
        "name": "DASH",
        "desc": "Designed for hypertension; low sodium, high potassium.",
    },
    "keto": {
        "emoji": "🥑",
        "name": "Ketogenic",
        "desc": "Very low carbohydrate, high fat; targets metabolic adaptation.",
    },
    "low_fodmap": {
        "emoji": "🌾",
        "name": "Low FODMAP",
        "desc": "Restricts fermentable carbs for IBS symptom relief.",
    },
    "low_sodium_renal": {
        "emoji": "💧",
        "name": "Renal (low-sodium)",
        "desc": "For chronic kidney disease; sodium, potassium and phosphorus limited.",
    },
    "diabetic": {
        "emoji": "🩸",
        "name": "Diabetic",
        "desc": "Carbohydrate distribution and glycaemic load are the focus.",
    },
    "vegan": {
        "emoji": "🌱",
        "name": "Vegan",
        "desc": "Fully plant-based; B12 and iron supplementation may be needed.",
    },
    "standard": {
        "emoji": "🍽️",
        "name": "Standard",
        "desc": "Balanced reference diet, used as a control arm.",
    },
}


# ---------------------------------------------------------------------------
# Disease label normalisation
# ---------------------------------------------------------------------------
DISEASE_LABELS: dict[str, str] = {
    "type_2_diabetes": "Type 2 Diabetes",
    "type_1_diabetes": "Type 1 Diabetes",
    "hypertension": "Hypertension",
    "dyslipidemia": "Dyslipidemia",
    "obesity": "Obesity",
    "metabolic_syndrome": "Metabolic Syndrome",
    "chronic_kidney_disease": "Chronic Kidney Disease",
    "fatty_liver": "Fatty Liver",
    "celiac_disease": "Celiac Disease",
    "ibs": "Irritable Bowel Syndrome",
    "gerd": "GERD",
    "osteoporosis": "Osteoporosis",
    "anemia_iron_deficiency": "Iron-deficiency Anemia",
    "hypothyroidism": "Hypothyroidism",
    "hyperthyroidism": "Hyperthyroidism",
    "pcos": "PCOS",
    "gout": "Gout",
    "phenylketonuria": "Phenylketonuria",
    "cancer_cachexia": "Cancer Cachexia",
    "anorexia_nervosa": "Anorexia Nervosa",
    "bulimia_nervosa": "Bulimia Nervosa",
    "binge_eating_disorder": "Binge Eating Disorder",
    "crohns_disease": "Crohn's Disease",
    "ulcerative_colitis": "Ulcerative Colitis",
    "cirrhosis": "Cirrhosis",
}


def disease_label(name: str) -> str:
    return DISEASE_LABELS.get(name, name.replace("_", " ").title())


def disease_chip_kind(name: str) -> str:
    """Return a CSS chip kind for a disease, used to colour-code chips."""
    cardio = {"hypertension", "dyslipidemia", "metabolic_syndrome"}
    renal = {"chronic_kidney_disease"}
    endo = {
        "type_2_diabetes",
        "type_1_diabetes",
        "pcos",
        "hypothyroidism",
        "hyperthyroidism",
    }
    if name in cardio:
        return "dx-cardio"
    if name in renal:
        return "dx-renal"
    if name in endo:
        return "dx-endo"
    return "dx"
