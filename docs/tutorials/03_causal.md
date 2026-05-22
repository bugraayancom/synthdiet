# Causal inference with synthetic patients

Because synthdiet generates fully synthetic patients, the *true* counterfactual
outcome for every patient under every diet is computable. This makes the
library uniquely suited to teaching causal inference.

## Counterfactual comparisons

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
print(f"Individual treatment effect on HbA1c: {ite:+.2f} pp")
```

## ATE on a cohort

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

## Heterogeneous effects (CATE)

```python
from synthdiet.causal import cate_by_subgroup

cate = cate_by_subgroup(
    cohort=cohort,
    treatment_diet=mediterranean_diet(),
    control_diet=standard_diet(),
    subgroup_fn=lambda p: "obese" if p.bmi >= 30 else "non_obese",
    outcome="hba1c_pct",
)
for group, ate in cate.items():
    print(group, ate.pretty())
```

## Confounding and adjustment

```python
from synthdiet.causal import ConfoundingExperiment

exp = ConfoundingExperiment(
    treatment_diet=mediterranean_diet(),
    control_diet=standard_diet(),
    # Sicker patients more likely to receive intervention (confounded assignment)
    propensity=lambda p: min(0.9, max(0.1, (p.bmi - 22) / 25.0)),
    duration_weeks=12,
)
report = exp.run(cohort, outcome="hba1c_pct", seed=42)
print(report)
```

The output includes the true ATE, the naive comparison (biased by
confounding), the IPTW-adjusted estimate, and the g-formula estimate.

## Visualising a DAG

```python
from synthdiet.causal.dag import default_diet_dag

dag = default_diet_dag()
print(dag.to_mermaid())
```

Paste the Mermaid output into a markdown viewer or GitHub README to render the
DAG graphically.
