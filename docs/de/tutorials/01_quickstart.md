# Schnellstart

Dieses Tutorial zeigt einen typischen `synthdiet`-Workflow:

1. eine\*n synthetische\*n Patient\*in erzeugen,
2. eine Krankheit hinzufügen,
3. eine Diät anwenden,
4. 12 Wochen simulieren,
5. das Ergebnis bewerten.

## Installation

```bash
pip install synthdiet
```

## Patient\*in anlegen

```python
from synthdiet import (
    Anthropometrics, Demographics, Lifestyle, Patient, Sex,
)
from synthdiet.diseases import Type2Diabetes
from synthdiet.patients.lifestyle import ActivityLevel

patient = Patient(
    demographics=Demographics(age=57, sex=Sex.MALE, country="DE"),
    anthropometrics=Anthropometrics(height_cm=176, weight_kg=98, waist_cm=108),
    lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT),
)
patient.add_disease(Type2Diabetes(severity="moderate"))
print(patient.summary())
```

## Vordefinierte Diät wählen

```python
from synthdiet import mediterranean_diet

diet = mediterranean_diet(daily_energy_kcal=1800)
print(diet.summary())
```

## Simulator ausführen

Standardmäßig nutzt der Simulator eine einfache Energiebilanzregel
(7700 kcal/kg). Für realistischere Langzeitprojektionen aktivieren
Sie das Hall-Modell:

```python
from synthdiet import DietSimulator

sim = DietSimulator(adherence=0.85, engine="hall_2011")
result = sim.run(patient, diet, duration_weeks=24)
print(f"Gewichtsänderung nach 24 Wochen: {result.weight_change_kg:+.2f} kg")
```

## Ergebnis bewerten

```python
from synthdiet import evaluate_simulation, format_evaluation_report

evaluation = evaluate_simulation(result)
print(format_evaluation_report(evaluation))
```

## Restriktionen prüfen

```python
warnings = sim.check_diet_against_constraints(patient, diet)
for w in warnings:
    print("Warnung:", w)
```

## Nächste Schritte

- [02_rct](02_rct.md) — RCT mit mehreren Armen durchführen.
- [03_causal](03_causal.md) — kontrafaktische Analysen, ATE.
- [04_case_studies](04_case_studies.md) — Lehrfälle.
