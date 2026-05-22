# 使用合成患者进行因果推断

由于 `synthdiet` 生成的是完全合成的患者,任何饮食下每位患者的
**真实反事实结果**都是可计算的。这使得本库特别适合用于因果推断
教学。

## 反事实比较

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
print(f"HbA1c 个体处理效应: {ite:+.2f} pp")
```

## 队列上的 ATE

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

## 异质性效应(CATE)

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

## 混杂与校正

```python
from synthdiet.causal import ConfoundingExperiment

exp = ConfoundingExperiment(
    treatment_diet=mediterranean_diet(),
    control_diet=standard_diet(),
    # 病情更重者更容易接受干预(混杂分配)
    propensity=lambda p: min(0.9, max(0.1, (p.bmi - 22) / 25.0)),
    duration_weeks=12,
)
report = exp.run(cohort, outcome="hba1c_pct", seed=42)
print(report)
```

输出包含真实 ATE、朴素估计(有偏)、IPTW 校正估计与 g-公式估计。

## DAG 可视化

```python
from synthdiet.causal.dag import default_diet_dag

dag = default_diet_dag()
print(dag.to_mermaid())
```

把 Mermaid 输出粘贴到 Markdown 查看器或 GitHub README 即可看到
图形化的 DAG。
