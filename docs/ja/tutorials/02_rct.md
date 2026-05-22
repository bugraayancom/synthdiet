# RCT の設計と実行

このチュートリアルでは `synthdiet.trials` エンジンを用いて並行群
ランダム化比較試験(RCT)をシミュレーションします。

## コホートの生成

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

## 検出力分析

```python
from synthdiet.stats import sample_size_continuous

n = sample_size_continuous(effect_size=2.0, sd=8.0, alpha=0.05, power=0.80)
print(f"群あたり {n} 例必要(2 kg 差、検出力 80%)。")
```

## 試験の定義と実行

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

## ITT・PP 解析

```python
itt = result.intention_to_treat(method="ancova")
pp = result.per_protocol(adherence_threshold=0.80)
print(itt.pretty())
print(pp.pretty())
```

- **ITT**: 割り付け群で患者全員を解析(脱落者を含む)。
  **effectiveness** を測ります。
- **PP**: アドヒアランス閾値以上の患者のみ。**efficacy** を測ります。

## CONSORT 図

```python
from synthdiet.viz import consort_diagram

ax = consort_diagram(result, title="合成 DASH 試験")
ax.figure.savefig("consort.png", dpi=150, bbox_inches="tight")
```

## ベースライン調整 ANCOVA

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

## その他の設計

`CrossoverTrial`(クロスオーバー)と `FactorialTrial`(2×2 要因)
も同じインターフェースを共有します。詳細は API リファレンスを
参照してください。
