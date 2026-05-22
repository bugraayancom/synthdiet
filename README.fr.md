# synthdiet

[![PyPI](https://img.shields.io/pypi/v/synthdiet.svg)](https://pypi.org/project/synthdiet/)
[![Python](https://img.shields.io/pypi/pyversions/synthdiet.svg)](https://pypi.org/project/synthdiet/)
[![Licence : MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/bugraayancom/synthdiet/actions/workflows/ci.yml/badge.svg)](https://github.com/bugraayancom/synthdiet/actions/workflows/ci.yml)

> Autres langues : [English](README.md) · [Türkçe](README.tr.md) · [Español](README.es.md) · [Deutsch](README.de.md) · [Português](README.pt.md) · [Italiano](README.it.md) · [中文](README.zh.md) · [日本語](README.ja.md)
Une bibliothèque Python pour **générer des patients synthétiques**
présentant des tableaux cliniques réalistes et **simuler des
interventions diététiques** sur ces patients.

`synthdiet` s'adresse aux diététiciens, aux chercheurs en nutrition
clinique et aux enseignants qui souhaitent prototyper des régimes,
mener des essais virtuels et éprouver les recommandations
nutritionnelles sur des centaines ou des milliers de patients
synthétiques avant de les amener en clinique.

> Avertissement : `synthdiet` est un outil de recherche et
> d'enseignement. Les chiffres qu'il produit **ne sont pas des
> recommandations cliniques** et les patients synthétiques **ne sont
> pas de vraies personnes**. Pour la prise en charge des patients,
> référez-vous toujours à un diététicien-nutritionniste qualifié.

![synthdiet hero](app/assets/screenshots/00_hero.png)

---

## Auteur

**Buğra Ayan** — Ankara / Turquie
- Site web : <https://bugraayan.com>
- E-mail : <bugraayan.com@gmail.com>
- Google Scholar : <https://scholar.google.com/citations?user=VHGqzNMAAAAJ&hl=tr>

---

## Fonctionnalités

### Modèle de domaine
- Une classe `Patient` typée agrégeant la démographie,
  l'anthropométrie, le mode de vie, les biomarqueurs biologiques,
  les diagnostics et les médicaments en cours.
- Un registre de **plus de 25 maladies** couvrant l'endocrinologie,
  la cardiologie, la néphrologie, l'hépatologie, la gastro-entérologie,
  la métabolique, la rhumatologie, l'oncologie, la psychiatrie et
  les allergies.
- Un registre de **19 interactions médicament-nutriment** cliniquement
  importantes (metformine → B12, statines → pamplemousse, warfarine →
  vitamine K, prise de la lévothyroxine, crise tyraminique aux IMAO,
  etc.).
- 5 générateurs de patients synthétiques (aléatoire, par
  distribution, par copule, cohorte, progression markovienne).
- Une base de 45 aliments avec décomposition macro/micronutriments
  et 8 régimes prédéfinis (méditerranéen, DASH, cétogène, FODMAP
  pauvre, rénal pauvre en sodium, diabétique, vegan, standard).

### Profondeur méthodologique (extension v0.1)
- **Modèle de composition corporelle de Hall (2011)** optionnel
  (`DietSimulator(engine="hall_2011")`), avec partition masse
  grasse / masse maigre via l'équation de Forbes et thermogenèse
  adaptative.
- **Dynamiques d'adhésion et d'abandon** : constante, décroissante,
  abandon Weibull, saut stochastique, charge perçue.
- **Moteur d'ECR** (`synthdiet.trials`) : bras parallèles, croisement
  (crossover), plans factoriels 2×2 ; randomisation stratifiée /
  par blocs / par minimisation ; modélisation des abandons ; analyses
  ITT/PP/AT.
- **Inférence causale** (`synthdiet.causal`) : simulation
  contrefactuelle, estimateurs ATE/CATE, expériences de confusion
  avec IPTW et g-formule, DAGs légers.
- **Indices de qualité alimentaire** (`synthdiet.indices`) : HEI-2020,
  AHEI-2010, MEDAS, score DASH, PHDI, DII.
- **Aides statistiques** (`synthdiet.stats`) : taille d'échantillon
  (continu/binaire), IC bootstrap, tests de permutation, ajustements
  Benjamini-Hochberg + Holm-Bonferroni, ANCOVA ajustée sur valeur
  initiale.
- **Injection d'erreurs de mesure et de données manquantes**
  (`synthdiet.noise`) : CV% par dosage, biais d'auto-déclaration,
  schémas MCAR/MAR/MNAR.
- **15 cas cliniques + notation type ECOS**
  (`synthdiet.education`).
- **Suite de validation** contre 5 ECR de référence
  (`synthdiet.validation`) : DASH-Sodium, PREDIMED, DiRECT,
  Look AHEAD, Diabetes Prevention Program.
- **Visualisation** (`synthdiet.viz`, optionnelle) : diagramme
  CONSORT, forest plot, ruban de trajectoires, Tableau 1.

---

## Installation

```bash
pip install synthdiet
```

Extras optionnels :

```bash
pip install "synthdiet[viz]"     # visualisations matplotlib
pip install "synthdiet[causal]"  # export DAG networkx
pip install "synthdiet[docs]"    # Sphinx + furo + myst-parser
pip install "synthdiet[dev]"     # pytest + ruff + mypy + matplotlib
```

`synthdiet` requiert Python 3.9+ et dépend de `numpy`, `pandas`, `scipy`.

---

## Tour en 60 secondes

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

Exemples complets dans [`examples/`](examples/) ; tutoriels en
français dans [`docs/fr/`](docs/fr/).

---

## Citation

```bibtex
@software{ayan_synthdiet_2026,
  author  = {Buğra Ayan},
  title   = {synthdiet: A Python library for simulating diets on synthetic patients},
  year    = {2026},
  version = {0.1.0},
  url     = {https://bugraayan.com}
}
```

## Licence

MIT — voir [`LICENSE`](LICENSE).
