# synthdiet

A Python library for generating synthetic patients with realistic clinical
conditions and simulating dietary interventions on them.

`synthdiet` is built for dietitians, clinical-nutrition researchers, and
educators who want to prototype diets, run virtual trials, and stress-test
nutritional recommendations against hundreds or thousands of synthetic
patients before bringing them to a clinic.

> Disclaimer: `synthdiet` is a research and teaching tool. The numbers it
> produces are *not* clinical recommendations and the synthetic patients are
> *not* real people. Always defer to a qualified registered dietitian for
> patient care.

---

## Author

**Buğra Ayan** — Ankara / Türkiye
- Website: <https://bugraayan.com>
- Email: <bugraayan.com@gmail.com>
- Google Scholar: <https://scholar.google.com/citations?user=VHGqzNMAAAAJ&hl=tr>

---

## Features

### Core domain model
- A typed `Patient` aggregating demographics, anthropometrics, lifestyle,
  lab biomarkers, diagnoses, and current medications.
- A registry of **25+ diseases** spanning endocrine, cardiovascular, renal,
  hepatic, gastrointestinal, metabolic, musculoskeletal, oncologic,
  psychiatric, and allergy categories.
- A registry of **19 clinically important drug-nutrient interactions**
  (metformin → B12, statins → grapefruit, warfarin → vitamin K,
  levothyroxine timing, MAOI tyramine crisis, etc.).
- 5 synthetic patient generators (random, distribution, copula, cohort,
  Markov progression).
- A 45-item food database with macro/micro nutrient breakdown and 8
  preset diets (Mediterranean, DASH, keto, low-FODMAP, low-sodium renal,
  diabetic, vegan, standard).

### Methodological depth (v0.1 expansion)
- **Hall 2011 body composition model** as an opt-in
  (`DietSimulator(engine="hall_2011")`) with fat-mass / lean-mass
  partitioning via the Forbes equation and adaptive thermogenesis.
- **Adherence and dropout dynamics**: constant, decaying, Weibull dropout,
  stochastic skip, perceived-burden.
- **RCT engine** (`synthdiet.trials`) supporting parallel-arm, crossover,
  and 2×2 factorial designs, with stratified / block / minimisation
  randomisation, dropout modelling, and ITT/PP/AT analyses.
- **Causal inference** (`synthdiet.causal`): counterfactual simulation,
  ATE/CATE estimators, propensity-confounding experiments with IPTW and
  g-formula adjustment, lightweight DAGs.
- **Diet quality indices** (`synthdiet.indices`): HEI-2020, AHEI-2010,
  MEDAS, DASH score, PHDI, DII.
- **Statistical helpers** (`synthdiet.stats`): power analysis for
  continuous and binary outcomes, bootstrap CI, permutation tests,
  Benjamini-Hochberg + Holm-Bonferroni adjustments, baseline-adjusted
  ANCOVA.
- **Measurement-error and missing-data injection** (`synthdiet.noise`):
  per-assay CV%, self-report bias, MCAR/MAR/MNAR patterns.
- **15 clinical case studies + OSCE-style grading**
  (`synthdiet.education`).
- **Validation suite** against 5 landmark RCTs
  (`synthdiet.validation`): DASH-Sodium, PREDIMED, DiRECT, Look AHEAD,
  Diabetes Prevention Program.
- **Visualisation** (`synthdiet.viz`, optional): CONSORT diagram, forest
  plot, trajectory ribbon, Table 1.

---

## Installation

```bash
pip install -e ".[dev,viz]"
```

`synthdiet` requires Python 3.9+ and depends on `numpy`, `pandas`, and `scipy`.

---

## 60-second tour

```python
from synthdiet import (
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

simulator = DietSimulator(adherence=0.8)
diet = mediterranean_diet(daily_energy_kcal=1800)

for patient in cohort[:3]:
    result = simulator.run(patient, diet, duration_weeks=12)
    evaluation = evaluate_simulation(result)
    print(format_evaluation_report(evaluation))
    print("-" * 60)
```

More end-to-end scripts live in [`examples/`](examples/).

---

## Project layout

```
src/synthdiet/
├── patients/          # Demographics, anthropometrics, biomarkers, lifestyle
├── diseases/          # 25+ disease classes + registry
├── interactions/      # Medication catalogue + drug-nutrient registry
├── nutrition/         # Foods, nutrients, DRIs
├── diets/             # DietPlan + 8 preset diets
├── generators/        # 5 synthetic patient generators
├── simulation/        # Diet simulator (simple + Hall 2011 body composition)
├── behavior/          # Adherence + Weibull dropout models
├── trials/            # RCT engine (parallel/crossover/factorial + ITT/PP)
├── causal/            # Counterfactual + ATE/CATE + IPTW + DAG
├── indices/           # HEI-2020, AHEI-2010, MEDAS, DASH, PHDI, DII
├── stats/             # Power analysis, bootstrap, ANCOVA, FDR/Holm
├── noise/             # Lab CV% + MCAR/MAR/MNAR missing-data injection
├── validation/        # DASH-Sodium / PREDIMED / DiRECT / Look AHEAD / DPP
├── education/         # 15 case studies + OSCE rubric + Markdown/HTML
├── viz/               # CONSORT, trajectories, forest, Table 1 (matplotlib)
├── evaluation/        # Outcome metrics + reports
└── utils/             # Constants, validators, random-state helpers
```

Tutorials live in [`docs/tutorials/`](docs/tutorials/) and a draft JOSS
paper lives in [`paper/`](paper/).

---

## Extending `synthdiet`

Add a new disease by subclassing `Disease` and registering it:

```python
from synthdiet.diseases.base import Disease, NutritionalConstraints
from synthdiet.diseases.registry import register


@register
class FattyLiverGradeII(Disease):
    name = "fatty_liver_grade_ii"
    icd10 = "K76.0"
    category = "hepatic"

    def nutritional_constraints(self, patient):
        return NutritionalConstraints(
            carbohydrate_pct_range=(0.35, 0.45),
            added_sugar_pct_max=0.05,
            fiber_g_min=30,
        )
```

After import, the class is automatically discoverable through
`get_disease("fatty_liver_grade_ii")` and selectable in `DiseaseSpec`.

---

## Citation

If you use `synthdiet` in academic work, please cite it via
[`CITATION.cff`](CITATION.cff) or the BibTeX entry below:

```bibtex
@software{ayan_synthdiet_2026,
  author  = {Buğra Ayan},
  title   = {synthdiet: A Python library for simulating diets on synthetic patients},
  year    = {2026},
  version = {0.1.0},
  url     = {https://bugraayan.com}
}
```

---

## License

MIT — see [`LICENSE`](LICENSE).
