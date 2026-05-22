# synthdiet · Streamlit app

An interactive multi-page web interface for the
[`synthdiet`](https://github.com/bugraayancom/synthdiet) Python library.

It exposes the full workflow visually:

| Page | What it does |
|------|--------------|
| 🩺 Home | Project overview, hero, feature grid, quick links. |
| 📋 Cohort Builder | Interactive prevalence sliders → live age × sex × BMI × diagnosis distributions, CSV export. |
| 🍽️ Diet Simulator | Apply any of 8 preset diets to a single patient and watch HbA1c, BP, LDL and weight trajectories animate week-by-week. |
| 🧪 RCT Engine | Set up a parallel-arm trial, run with Weibull dropout + adherence, view CONSORT flow, forest plot, ITT / per-protocol / as-treated. |
| 📚 Case Studies | Browse the 15 built-in clinical cases, filter by difficulty / tag, and grade student diet plans with the OSCE rubric. |
| ℹ️ About | Author, citation, license, deployment instructions. |

The visual style is "clinical clean": white background, medical
blue / green accents, glassmorphism cards, smooth fade-up animations
and animated Plotly charts.

---

## Run locally

From the repository root:

```bash
# 1. Install the library + Streamlit extras
pip install -e ".[app]"

# 2. Launch the app
streamlit run app/streamlit_app.py
```

The app opens at <http://localhost:8501>. Streamlit will pick up the
multi-page structure under `app/pages/` automatically.

### Custom theme & styling

- Theme primaries are defined in `app/.streamlit/config.toml`
  (clinical-clean, light, sky-blue + emerald accents).
- All custom CSS lives in `app/style.css` and is injected once per page
  by `components.page_setup()`.
- Reusable building blocks (hero, metric grid, patient cards, callouts,
  etc.) are in `app/components.py`.

---

## Deploy to Streamlit Community Cloud

1. Sign in at <https://share.streamlit.io> with your GitHub account.
2. Click **New app**, point it to:
   - **Repository**: `bugraayancom/synthdiet`
   - **Branch**: `main`
   - **Main file path**: `app/streamlit_app.py`
3. Under **Advanced settings → Python version**, pick `3.11` or `3.12`.
4. The deploy step will read `app/requirements.txt` (which already
   pins `synthdiet`, `streamlit`, `plotly`, `pandas`, `numpy`, `scipy`).
5. Hit **Deploy**. The first build takes ~2 minutes.

Once deployed, you'll get a public URL of the form
`https://synthdiet.streamlit.app`.

### Updating

Streamlit Cloud redeploys automatically on every push to `main`. If
you change `app/requirements.txt`, the build environment is rebuilt
on the next deploy.

---

## Folder structure

```
app/
├── .streamlit/
│   └── config.toml           # theme + server config
├── pages/                    # Streamlit auto-discovers these
│   ├── 1_📋_Cohort_Builder.py
│   ├── 2_🍽️_Diet_Simulator.py
│   ├── 3_🧪_RCT_Engine.py
│   ├── 4_📚_Case_Studies.py
│   └── 5_ℹ️_About.py
├── streamlit_app.py          # Home / landing
├── components.py             # Reusable HTML/CSS components
├── style.css                 # Project-wide custom CSS
├── requirements.txt          # For Streamlit Community Cloud
└── README.md                 # This file
```

## Notes

- Patient generation and simulations are cached with
  `@st.cache_data` / `@st.cache_resource` keyed on the active cohort
  signature, so navigating between pages doesn't re-run heavy work.
- Cohorts persist across pages via `st.session_state`; if you
  hard-reload the tab you'll need to regenerate one in the
  **Cohort Builder**.
- The app relies only on the public `synthdiet` API; no private
  internals are touched.

## License

MIT — see the repository root [`LICENSE`](../LICENSE).
