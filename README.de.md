# synthdiet

[![PyPI](https://img.shields.io/pypi/v/synthdiet.svg)](https://pypi.org/project/synthdiet/)
[![Python](https://img.shields.io/pypi/pyversions/synthdiet.svg)](https://pypi.org/project/synthdiet/)
[![Lizenz: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/bugraayancom/synthdiet/actions/workflows/ci.yml/badge.svg)](https://github.com/bugraayancom/synthdiet/actions/workflows/ci.yml)

> Andere Sprachen: [English](README.md) · [Türkçe](README.tr.md) · [Español](README.es.md) · [Français](README.fr.md) · [Português](README.pt.md) · [Italiano](README.it.md) · [中文](README.zh.md) · [日本語](README.ja.md)
Eine Python-Bibliothek zum **Erzeugen synthetischer Patientinnen und
Patienten** mit realistischen klinischen Tableaus und zur
**Simulation diätetischer Interventionen** an ihnen.

`synthdiet` richtet sich an Diätassistent\*innen, klinische
Ernährungsforscher\*innen und Lehrende, die Diäten prototypisch
entwickeln, virtuelle Studien durchführen und Ernährungsempfehlungen
an Hunderten oder Tausenden synthetischer Patient\*innen
stresstesten möchten, bevor sie in die Klinik gelangen.

> Hinweis: `synthdiet` ist ein Forschungs- und Lehrwerkzeug. Die
> erzeugten Zahlen sind **keine klinischen Empfehlungen** und die
> synthetischen Patient\*innen sind **keine realen Personen**. Für die
> Patientenversorgung wenden Sie sich stets an eine\*n qualifizierte\*n
> registrierte\*n Diätassistent\*in.

![synthdiet hero](app/assets/screenshots/00_hero.png)

---

## Autor

**Buğra Ayan** — Ankara / Türkei
- Webseite: <https://bugraayan.com>
- E-Mail: <bugraayan.com@gmail.com>
- Google Scholar: <https://scholar.google.com/citations?user=VHGqzNMAAAAJ&hl=tr>

---

## Funktionsumfang

### Kerndomänenmodell
- Eine typisierte `Patient`-Klasse, die Demografie, Anthropometrie,
  Lebensstil, Laborbiomarker, Diagnosen und aktuelle Medikation
  zusammenführt.
- Ein Register mit **mehr als 25 Krankheiten** aus den Bereichen
  Endokrinologie, Kardiologie, Nephrologie, Hepatologie,
  Gastroenterologie, Stoffwechsel, Bewegungsapparat, Onkologie,
  Psychiatrie und Allergologie.
- Ein Register mit **19 klinisch relevanten Arzneimittel-Nährstoff-
  Wechselwirkungen** (Metformin → B12, Statine → Grapefruit,
  Warfarin → Vitamin K, L-Thyroxin-Einnahmezeitpunkt, Tyramin-Krise
  unter MAO-Hemmern usw.).
- 5 Generatoren synthetischer Patient\*innen (zufällig, verteilungs-
  basiert, Copula, Kohorte, Markow-Progression).
- Eine 45 Lebensmittel umfassende Datenbank mit Makro-/Mikronährstoff-
  Aufschlüsselung und 8 voreingestellten Diäten (Mediterran, DASH,
  Keto, Low-FODMAP, natriumarm bei Niereninsuffizienz, Diabetiker,
  vegan, Standard).

### Methodische Tiefe (v0.1)
- **Hall-Körperzusammensetzungsmodell (2011)** als optionale Engine
  (`DietSimulator(engine="hall_2011")`) mit Fett-/Magermassen-
  Aufteilung über die Forbes-Gleichung und adaptiver Thermogenese.
- **Adhärenz- und Drop-out-Dynamik**: konstant, abklingend, Weibull,
  stochastische Aussetzer, wahrgenommene Belastung.
- **RCT-Engine** (`synthdiet.trials`): Parallelarm-, Crossover- und
  2×2-faktorielle Designs; geschichtete / Block- /
  Minimierungs-Randomisierung; Drop-out-Modellierung; ITT/PP/AT-
  Analysen.
- **Kausale Inferenz** (`synthdiet.causal`): kontrafaktische
  Simulation, ATE/CATE-Schätzer, Konfundierungs-Experimente mit
  IPTW und g-Formel, leichtgewichtige DAGs.
- **Indizes der Ernährungsqualität** (`synthdiet.indices`): HEI-2020,
  AHEI-2010, MEDAS, DASH-Score, PHDI, DII.
- **Statistische Helfer** (`synthdiet.stats`): Power-Analysen für
  stetige und binäre Endpunkte, Bootstrap-KI, Permutationstests,
  Benjamini-Hochberg- und Holm-Bonferroni-Korrekturen,
  baseline-adjustierte ANCOVA.
- **Mess- und Fehlende-Daten-Injektion** (`synthdiet.noise`):
  Assay-CV%, Selbstauskunfts-Bias, MCAR/MAR/MNAR-Muster.
- **15 Fallstudien + OSCE-artige Bewertung**
  (`synthdiet.education`).
- **Validierungssuite** gegen 5 Meilenstein-RCTs
  (`synthdiet.validation`): DASH-Sodium, PREDIMED, DiRECT,
  Look AHEAD, Diabetes Prevention Program.
- **Visualisierung** (`synthdiet.viz`, optional): CONSORT-Diagramm,
  Forest-Plot, Trajektorien-Band, Tabelle 1.

---

## Installation

```bash
pip install synthdiet
```

Optionale Extras:

```bash
pip install "synthdiet[viz]"     # matplotlib-Visualisierungen
pip install "synthdiet[causal]"  # networkx-DAG-Export
pip install "synthdiet[docs]"    # Sphinx + furo + myst-parser
pip install "synthdiet[dev]"     # pytest + ruff + mypy + matplotlib
```

`synthdiet` benötigt Python 3.9+ und stützt sich auf `numpy`, `pandas`,
`scipy`.

---

## 60-Sekunden-Tour

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

Vollständige Beispiele in [`examples/`](examples/); deutsche
Tutorials in [`docs/de/`](docs/de/).

---

## Zitation

```bibtex
@software{ayan_synthdiet_2026,
  author  = {Buğra Ayan},
  title   = {synthdiet: A Python library for simulating diets on synthetic patients},
  year    = {2026},
  version = {0.1.0},
  url     = {https://bugraayan.com}
}
```

## Lizenz

MIT — siehe [`LICENSE`](LICENSE).
