# Quickstart

This tutorial walks through a typical synthdiet workflow:

1. generate a synthetic patient,
2. attach a disease,
3. apply a diet,
4. simulate 12 weeks, and
5. evaluate the outcome.

## Install

```bash
pip install synthdiet
```

## Create a single patient

```python
from synthdiet import (
    Anthropometrics, Demographics, Lifestyle, Patient, Sex,
    Type2Diabetes := None,  # placeholder; real import below
)
from synthdiet.diseases import Type2Diabetes
from synthdiet.patients.lifestyle import ActivityLevel

patient = Patient(
    demographics=Demographics(age=57, sex=Sex.MALE, country="TR"),
    anthropometrics=Anthropometrics(height_cm=176, weight_kg=98, waist_cm=108),
    lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT),
)
patient.add_disease(Type2Diabetes(severity="moderate"))
print(patient.summary())
```

## Choose a diet preset

```python
from synthdiet import mediterranean_diet

diet = mediterranean_diet(daily_energy_kcal=1800)
print(diet.summary())
```

## Run the simulator

The default simulator uses a simple "7700 kcal/kg" energy-balance rule. For
more realistic long-term projections pass `engine="hall_2011"` to enable
the Hall body-composition model.

```python
from synthdiet import DietSimulator

sim = DietSimulator(adherence=0.85, engine="hall_2011")
result = sim.run(patient, diet, duration_weeks=24)
print(f"Weight change after 24 weeks: {result.weight_change_kg:+.2f} kg")
```

## Evaluate the outcome

```python
from synthdiet import evaluate_simulation, format_evaluation_report

evaluation = evaluate_simulation(result)
print(format_evaluation_report(evaluation))
```

## Next steps

- `02_rct` — run a multi-arm randomised trial on a cohort.
- `03_causal` — counterfactual analyses and ATE estimation.
- `04_case_studies` — use built-in clinical cases for teaching.
