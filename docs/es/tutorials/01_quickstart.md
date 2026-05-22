# Inicio rápido

Este tutorial recorre un flujo de trabajo típico de `synthdiet`:

1. generar un paciente sintético,
2. añadirle una enfermedad,
3. aplicar una dieta,
4. simular 12 semanas, y
5. evaluar el resultado.

## Instalación

```bash
pip install synthdiet
```

## Crear un paciente

```python
from synthdiet import (
    Anthropometrics, Demographics, Lifestyle, Patient, Sex,
)
from synthdiet.diseases import Type2Diabetes
from synthdiet.patients.lifestyle import ActivityLevel

patient = Patient(
    demographics=Demographics(age=57, sex=Sex.MALE, country="ES"),
    anthropometrics=Anthropometrics(height_cm=176, weight_kg=98, waist_cm=108),
    lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT),
)
patient.add_disease(Type2Diabetes(severity="moderate"))
print(patient.summary())
```

## Elegir una dieta predefinida

```python
from synthdiet import mediterranean_diet

diet = mediterranean_diet(daily_energy_kcal=1800)
print(diet.summary())
```

Hay 8 dietas predefinidas: mediterránea, DASH, cetogénica, baja en
FODMAP, renal baja en sodio, diabética, vegana y estándar.

## Ejecutar el simulador

El simulador por defecto usa una regla simple de balance energético
(7700 kcal/kg). Para proyecciones de largo plazo más realistas,
active el modelo de Hall:

```python
from synthdiet import DietSimulator

sim = DietSimulator(adherence=0.85, engine="hall_2011")
result = sim.run(patient, diet, duration_weeks=24)
print(f"Cambio de peso a 24 semanas: {result.weight_change_kg:+.2f} kg")
```

## Evaluar el resultado

```python
from synthdiet import evaluate_simulation, format_evaluation_report

evaluation = evaluate_simulation(result)
print(format_evaluation_report(evaluation))
```

## Comprobar restricciones de la dieta

```python
warnings = sim.check_diet_against_constraints(patient, diet)
for w in warnings:
    print("Aviso:", w)
```

## Próximos pasos

- [02_rct](02_rct.md) — ejecutar un ECA con varios brazos.
- [03_causal](03_causal.md) — análisis contrafactual y ATE.
- [04_case_studies](04_case_studies.md) — casos clínicos integrados.
