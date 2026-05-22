# Inferência causal com pacientes sintéticos

Como `synthdiet` gera pacientes totalmente sintéticos, o **resultado
contrafactual real** de cada paciente sob qualquer dieta pode ser
calculado. Isso torna a biblioteca ideal para o ensino de inferência
causal.

## Comparações contrafactuais

```python
from synthdiet import (
    Anthropometrics, Demographics, Lifestyle, Patient, Sex,
    mediterranean_diet, standard_diet,
)
from synthdiet.diseases import Type2Diabetes
from synthdiet.causal import counterfactual_run

patient = Patient(
    demographics=Demographics(age=58, sex=Sex.MALE),
    anthropometrics=Anthropometrics(height_cm=176, weight_kg=98),
    lifestyle=Lifestyle(),
)
patient.add_disease(Type2Diabetes(severity="moderate"))

pair = counterfactual_run(patient, mediterranean_diet(), standard_diet(),
                          duration_weeks=12)
ite = pair.individual_effect("hba1c_pct")
print(f"Efeito individual sobre HbA1c: {ite:+.2f} pp")
```

## ATE em uma coorte

```python
from synthdiet import CohortGenerator, CohortSpec, DiseaseSpec
from synthdiet.causal import ATEEstimator

cohort = CohortGenerator(
    CohortSpec(size=80, diseases=[DiseaseSpec("type_2_diabetes", 1.0)]),
    seed=1,
).generate()

est = ATEEstimator(
    treatment_diet=mediterranean_diet(),
    control_diet=standard_diet(),
    duration_weeks=12,
)
result = est.estimate(cohort, outcome="hba1c_pct")
print(result.pretty())
```

## Efeitos heterogêneos (CATE)

```python
from synthdiet.causal import cate_by_subgroup

cate = cate_by_subgroup(
    cohort=cohort,
    treatment_diet=mediterranean_diet(),
    control_diet=standard_diet(),
    subgroup_fn=lambda p: "obeso" if p.bmi >= 30 else "nao_obeso",
    outcome="hba1c_pct",
)
for group, ate in cate.items():
    print(group, ate.pretty())
```

## Confundimento e ajuste

```python
from synthdiet.causal import ConfoundingExperiment

exp = ConfoundingExperiment(
    treatment_diet=mediterranean_diet(),
    control_diet=standard_diet(),
    # Pacientes mais doentes tendem a receber a intervenção
    propensity=lambda p: min(0.9, max(0.1, (p.bmi - 22) / 25.0)),
    duration_weeks=12,
)
report = exp.run(cohort, outcome="hba1c_pct", seed=42)
print(report)
```

A saída inclui o ATE verdadeiro, a comparação ingênua (viesada), a
estimativa por IPTW e a estimativa pela g-fórmula.

## Visualizar um DAG

```python
from synthdiet.causal.dag import default_diet_dag

dag = default_diet_dag()
print(dag.to_mermaid())
```
