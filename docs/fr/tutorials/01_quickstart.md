# Démarrage rapide

Ce tutoriel parcourt un flux de travail typique avec `synthdiet` :

1. générer un patient synthétique,
2. lui attacher une maladie,
3. lui appliquer un régime,
4. simuler 12 semaines,
5. évaluer le résultat.

## Installation

```bash
pip install synthdiet
```

## Créer un patient

```python
from synthdiet import (
    Anthropometrics, Demographics, Lifestyle, Patient, Sex,
)
from synthdiet.diseases import Type2Diabetes
from synthdiet.patients.lifestyle import ActivityLevel

patient = Patient(
    demographics=Demographics(age=57, sex=Sex.MALE, country="FR"),
    anthropometrics=Anthropometrics(height_cm=176, weight_kg=98, waist_cm=108),
    lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT),
)
patient.add_disease(Type2Diabetes(severity="moderate"))
print(patient.summary())
```

## Choisir un régime prédéfini

```python
from synthdiet import mediterranean_diet

diet = mediterranean_diet(daily_energy_kcal=1800)
print(diet.summary())
```

8 régimes prédéfinis : méditerranéen, DASH, cétogène, FODMAP pauvre,
rénal pauvre en sodium, diabétique, vegan, standard.

## Lancer le simulateur

Le simulateur par défaut applique une règle simple de balance
énergétique (7700 kcal/kg). Pour des projections plus réalistes à
long terme, activez le modèle de Hall :

```python
from synthdiet import DietSimulator

sim = DietSimulator(adherence=0.85, engine="hall_2011")
result = sim.run(patient, diet, duration_weeks=24)
print(f"Variation pondérale à 24 semaines : {result.weight_change_kg:+.2f} kg")
```

## Évaluer le résultat

```python
from synthdiet import evaluate_simulation, format_evaluation_report

evaluation = evaluate_simulation(result)
print(format_evaluation_report(evaluation))
```

## Vérifier les contraintes du régime

```python
warnings = sim.check_diet_against_constraints(patient, diet)
for w in warnings:
    print("Avertissement :", w)
```

## Pour aller plus loin

- [02_rct](02_rct.md) — exécuter un ECR multibras.
- [03_causal](03_causal.md) — analyses contrefactuelles et ATE.
- [04_case_studies](04_case_studies.md) — cas cliniques intégrés.
