# Diseñar y ejecutar un ECA

Este tutorial usa el motor `synthdiet.trials` para simular un ensayo
clínico aleatorizado de brazos paralelos.

## Generar la cohorte

```python
from synthdiet import CohortGenerator, CohortSpec, DiseaseSpec

spec = CohortSpec(
    size=200,
    diseases=[
        DiseaseSpec("hypertension", prevalence=0.40,
                    severity_weights={"mild": 4, "moderate": 4, "severe": 2}),
        DiseaseSpec("type_2_diabetes", prevalence=0.30),
    ],
)
cohort = CohortGenerator(spec, seed=2026).generate()
```

## Cálculo de potencia

```python
from synthdiet.stats import sample_size_continuous

n = sample_size_continuous(effect_size=2.0, sd=8.0, alpha=0.05, power=0.80)
print(f"Se necesitan {n} pacientes por brazo (diferencia de 2 kg, potencia 80%).")
```

## Definir y lanzar el ensayo

```python
from synthdiet.diets import dash_diet, standard_diet
from synthdiet.trials import ParallelTrial, WeibullDropout
from synthdiet.behavior import DecayingAdherence

trial = ParallelTrial(
    cohort=cohort,
    arms={"control": standard_diet(), "dash": dash_diet()},
    duration_weeks=24,
    primary_outcome="systolic_bp_mmhg",
    secondary_outcomes=["weight_kg", "ldl_mg_dl"],
    randomization="stratified",
    strata=[lambda p: p.demographics.sex.value,
            lambda p: p.has_disease("type_2_diabetes")],
    adherence=DecayingAdherence(initial=0.90, floor=0.45, rate=0.02),
    dropout=WeibullDropout(shape=1.5, scale_weeks=40, seed=7),
    engine="hall_2011",
)
result = trial.run(seed=42)
```

## Análisis ITT y por protocolo

```python
itt = result.intention_to_treat(method="ancova")
pp = result.per_protocol(adherence_threshold=0.80)
print(itt.pretty())
print(pp.pretty())
```

- **ITT**: analiza a cada paciente en su brazo asignado, incluyendo
  abandonos. Mide la **efectividad**.
- **Por protocolo**: solo los que cumplieron el umbral de adherencia.
  Mide la **eficacia**.

## Diagrama CONSORT

```python
from synthdiet.viz import consort_diagram

ax = consort_diagram(result, title="Ensayo DASH sintético")
ax.figure.savefig("consort.png", dpi=150, bbox_inches="tight")
```

## ANCOVA ajustada por línea base

```python
from synthdiet.stats import ancova_baseline_adjusted

ancova = ancova_baseline_adjusted(
    result.outcomes,
    outcome="delta_systolic_bp_mmhg",
    baseline="baseline_systolic_bp_mmhg",
    treatment="arm",
)
print(ancova.pretty())
```

## Otros diseños

`CrossoverTrial` (diseño cruzado) y `FactorialTrial` (factorial 2×2)
comparten la misma interfaz que `ParallelTrial`. Detalles en la
referencia de la API.
