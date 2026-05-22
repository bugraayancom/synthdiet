# synthdiet

[![PyPI](https://img.shields.io/pypi/v/synthdiet.svg)](https://pypi.org/project/synthdiet/)
[![Python](https://img.shields.io/pypi/pyversions/synthdiet.svg)](https://pypi.org/project/synthdiet/)
[![Licenza: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/bugraayancom/synthdiet/actions/workflows/ci.yml/badge.svg)](https://github.com/bugraayancom/synthdiet/actions/workflows/ci.yml)

> Altre lingue: [English](README.md) · [Türkçe](README.tr.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português](README.pt.md) · [中文](README.zh.md) · [日本語](README.ja.md)
Una libreria Python per **generare pazienti sintetici** con quadri
clinici realistici e **simulare interventi dietetici** su di essi.

`synthdiet` è pensato per dietisti, ricercatori in nutrizione clinica
e docenti che vogliano prototipare diete, condurre studi virtuali e
mettere alla prova le raccomandazioni nutrizionali su centinaia o
migliaia di pazienti sintetici prima di portarle in clinica.

> Avvertenza: `synthdiet` è uno strumento di ricerca e didattica.
> I numeri prodotti **non sono raccomandazioni cliniche** e i pazienti
> sintetici **non sono persone reali**. Per la cura del paziente
> consultare sempre un dietista qualificato.

---

## Autore

**Buğra Ayan** — Ankara / Turchia
- Sito web: <https://bugraayan.com>
- Email: <bugraayan.com@gmail.com>
- Google Scholar: <https://scholar.google.com/citations?user=VHGqzNMAAAAJ&hl=tr>

---

## Funzionalità

### Modello di dominio
- Una classe `Patient` tipata che aggrega demografia, antropometria,
  stile di vita, biomarcatori di laboratorio, diagnosi e farmaci.
- Un registro di **oltre 25 patologie** che copre endocrinologia,
  cardiologia, nefrologia, epatologia, gastroenterologia, metabolica,
  apparato muscolo-scheletrico, oncologia, psichiatria e allergie.
- Un registro di **19 interazioni farmaco-nutriente** clinicamente
  rilevanti (metformina → B12, statine → pompelmo, warfarin →
  vitamina K, tempistica della levotiroxina, crisi tiraminica con
  IMAO, ecc.).
- 5 generatori di pazienti sintetici (random, per distribuzione, per
  copula, coorte, progressione di Markov).
- Una banca di 45 alimenti con scomposizione macro/micronutriente
  e 8 diete predefinite (mediterranea, DASH, chetogenica, low-FODMAP,
  renale iposodica, diabetica, vegana, standard).

### Profondità metodologica (v0.1)
- **Modello di composizione corporea di Hall (2011)** opzionale
  (`DietSimulator(engine="hall_2011")`), con partizione massa
  grassa/magra via equazione di Forbes e termogenesi adattativa.
- **Dinamiche di aderenza e abbandono**: costante, decrescente,
  abbandono Weibull, salto stocastico, carico percepito.
- **Motore RCT** (`synthdiet.trials`): bracci paralleli, crossover,
  fattoriale 2×2; randomizzazione stratificata / a blocchi / per
  minimizzazione; modellazione dell'abbandono; analisi ITT/PP/AT.
- **Inferenza causale** (`synthdiet.causal`): simulazione
  controfattuale, stimatori ATE/CATE, esperimenti di confondimento
  con IPTW e g-formula, DAG leggeri.
- **Indici di qualità della dieta** (`synthdiet.indices`): HEI-2020,
  AHEI-2010, MEDAS, punteggio DASH, PHDI, DII.
- **Strumenti statistici** (`synthdiet.stats`): calcolo della potenza
  per esiti continui e binari, IC bootstrap, test di permutazione,
  correzioni Benjamini-Hochberg + Holm-Bonferroni, ANCOVA aggiustata
  per il valore basale.
- **Iniezione di errori di misura e dati mancanti**
  (`synthdiet.noise`): CV% per saggio, bias di auto-segnalazione,
  schemi MCAR/MAR/MNAR.
- **15 casi clinici + valutazione tipo OSCE**
  (`synthdiet.education`).
- **Suite di validazione** contro 5 RCT cardine
  (`synthdiet.validation`): DASH-Sodium, PREDIMED, DiRECT,
  Look AHEAD, Diabetes Prevention Program.
- **Visualizzazione** (`synthdiet.viz`, opzionale): diagramma
  CONSORT, forest plot, banda di traiettorie, Tabella 1.

---

## Installazione

```bash
pip install synthdiet
```

Extra opzionali:

```bash
pip install "synthdiet[viz]"     # visualizzazioni matplotlib
pip install "synthdiet[causal]"  # esportazione DAG con networkx
pip install "synthdiet[docs]"    # Sphinx + furo + myst-parser
pip install "synthdiet[dev]"     # pytest + ruff + mypy + matplotlib
```

`synthdiet` richiede Python 3.9+ e dipende da `numpy`, `pandas`, `scipy`.

---

## Tour in 60 secondi

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

Esempi completi in [`examples/`](examples/); tutorial in italiano in
[`docs/it/`](docs/it/).

---

## Citazione

```bibtex
@software{ayan_synthdiet_2026,
  author  = {Buğra Ayan},
  title   = {synthdiet: A Python library for simulating diets on synthetic patients},
  year    = {2026},
  version = {0.1.0},
  url     = {https://bugraayan.com}
}
```

## Licenza

MIT — vedere [`LICENSE`](LICENSE).
