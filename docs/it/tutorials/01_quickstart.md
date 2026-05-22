# Avvio rapido

Questo tutorial percorre un flusso di lavoro tipico di `synthdiet`:

1. generare un paziente sintetico,
2. assegnargli una patologia,
3. applicare una dieta,
4. simulare 12 settimane,
5. valutare il risultato.

## Installazione

```bash
pip install synthdiet
```

## Creare un paziente

```python
from synthdiet import (
    Anthropometrics, Demographics, Lifestyle, Patient, Sex,
)
from synthdiet.diseases import Type2Diabetes
from synthdiet.patients.lifestyle import ActivityLevel

patient = Patient(
    demographics=Demographics(age=57, sex=Sex.MALE, country="IT"),
    anthropometrics=Anthropometrics(height_cm=176, weight_kg=98, waist_cm=108),
    lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT),
)
patient.add_disease(Type2Diabetes(severity="moderate"))
print(patient.summary())
```

## Scegliere una dieta predefinita

```python
from synthdiet import mediterranean_diet

diet = mediterranean_diet(daily_energy_kcal=1800)
print(diet.summary())
```

## Eseguire il simulatore

Il simulatore di default usa la regola del bilancio energetico
(7700 kcal/kg). Per proiezioni a lungo termine più realistiche,
attivare il modello di Hall:

```python
from synthdiet import DietSimulator

sim = DietSimulator(adherence=0.85, engine="hall_2011")
result = sim.run(patient, diet, duration_weeks=24)
print(f"Variazione di peso a 24 settimane: {result.weight_change_kg:+.2f} kg")
```

## Valutare il risultato

```python
from synthdiet import evaluate_simulation, format_evaluation_report

evaluation = evaluate_simulation(result)
print(format_evaluation_report(evaluation))
```

## Verificare i vincoli

```python
warnings = sim.check_diet_against_constraints(patient, diet)
for w in warnings:
    print("Avviso:", w)
```

## Prossimi passi

- [02_rct](02_rct.md) — RCT multi-braccio.
- [03_causal](03_causal.md) — analisi controfattuali, ATE.
- [04_case_studies](04_case_studies.md) — casi clinici inclusi.
