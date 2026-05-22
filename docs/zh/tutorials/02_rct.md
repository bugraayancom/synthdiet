# 设计并执行 RCT

本教程使用 `synthdiet.trials` 引擎模拟一个平行组随机对照试验。

## 生成队列

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

## 功效分析

```python
from synthdiet.stats import sample_size_continuous

n = sample_size_continuous(effect_size=2.0, sd=8.0, alpha=0.05, power=0.80)
print(f"每组需要 {n} 例(2 kg 差异,80% 功效)。")
```

## 定义并运行试验

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

## ITT 与 PP 分析

```python
itt = result.intention_to_treat(method="ancova")
pp = result.per_protocol(adherence_threshold=0.80)
print(itt.pretty())
print(pp.pretty())
```

- **ITT**:按分配组分析全部患者(包含脱落者),衡量
  **效果(effectiveness)**。
- **PP**:仅分析达到依从阈值的患者,衡量
  **效力(efficacy)**。

## CONSORT 图

```python
from synthdiet.viz import consort_diagram

ax = consort_diagram(result, title="合成 DASH 试验")
ax.figure.savefig("consort.png", dpi=150, bbox_inches="tight")
```

## 基线调整 ANCOVA

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

## 其他设计

`CrossoverTrial`(交叉)和 `FactorialTrial`(2×2 析因)与
`ParallelTrial` 共享相同接口。详见 API 参考。
