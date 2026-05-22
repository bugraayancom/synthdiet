# Kausale Inferenz mit synthetischen Patient\*innen

Da `synthdiet` vollständig synthetische Patient\*innen erzeugt, ist
das **echte kontrafaktische Ergebnis** jeder Person unter jeder Diät
berechenbar. Das macht die Bibliothek zu einem hervorragenden
Werkzeug für die Lehre kausaler Inferenz.

## Kontrafaktische Vergleiche

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
print(f"Individueller Effekt auf HbA1c: {ite:+.2f} pp")
```

## ATE auf einer Kohorte

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

## Heterogene Effekte (CATE)

```python
from synthdiet.causal import cate_by_subgroup

cate = cate_by_subgroup(
    cohort=cohort,
    treatment_diet=mediterranean_diet(),
    control_diet=standard_diet(),
    subgroup_fn=lambda p: "adipoes" if p.bmi >= 30 else "nicht_adipoes",
    outcome="hba1c_pct",
)
for group, ate in cate.items():
    print(group, ate.pretty())
```

## Konfundierung und Adjustierung

```python
from synthdiet.causal import ConfoundingExperiment

exp = ConfoundingExperiment(
    treatment_diet=mediterranean_diet(),
    control_diet=standard_diet(),
    # Krankere Patient*innen erhalten häufiger die Intervention
    propensity=lambda p: min(0.9, max(0.1, (p.bmi - 22) / 25.0)),
    duration_weeks=12,
)
report = exp.run(cohort, outcome="hba1c_pct", seed=42)
print(report)
```

Die Ausgabe enthält den wahren ATE, den naiven (verzerrten) Vergleich,
die IPTW-adjustierte Schätzung und die g-Formel-Schätzung.

## Einen DAG visualisieren

```python
from synthdiet.causal.dag import default_diet_dag

dag = default_diet_dag()
print(dag.to_mermaid())
```

Fügen Sie die Mermaid-Ausgabe in einen Markdown-Viewer oder ein
GitHub-README ein, um den DAG grafisch zu sehen.
