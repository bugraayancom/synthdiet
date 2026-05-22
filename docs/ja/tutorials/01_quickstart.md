# クイックスタート

このチュートリアルでは典型的な `synthdiet` のワークフローを示します。

1. 合成患者を生成し、
2. 疾患を付与し、
3. 食事を適用し、
4. 12 週間シミュレーションし、
5. 結果を評価します。

## インストール

```bash
pip install synthdiet
```

## 患者の作成

```python
from synthdiet import (
    Anthropometrics, Demographics, Lifestyle, Patient, Sex,
)
from synthdiet.diseases import Type2Diabetes
from synthdiet.patients.lifestyle import ActivityLevel

patient = Patient(
    demographics=Demographics(age=57, sex=Sex.MALE, country="JP"),
    anthropometrics=Anthropometrics(height_cm=176, weight_kg=98, waist_cm=108),
    lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT),
)
patient.add_disease(Type2Diabetes(severity="moderate"))
print(patient.summary())
```

## プリセット食を選ぶ

```python
from synthdiet import mediterranean_diet

diet = mediterranean_diet(daily_energy_kcal=1800)
print(diet.summary())
```

## シミュレータの実行

デフォルトのシミュレータは単純なエネルギー収支則
(7700 kcal/kg)を用います。長期予測でより現実的な結果が必要な
場合は Hall モデルを有効にします。

```python
from synthdiet import DietSimulator

sim = DietSimulator(adherence=0.85, engine="hall_2011")
result = sim.run(patient, diet, duration_weeks=24)
print(f"24 週後の体重変化: {result.weight_change_kg:+.2f} kg")
```

## 結果の評価

```python
from synthdiet import evaluate_simulation, format_evaluation_report

evaluation = evaluate_simulation(result)
print(format_evaluation_report(evaluation))
```

## 制約のチェック

```python
warnings = sim.check_diet_against_constraints(patient, diet)
for w in warnings:
    print("警告:", w)
```

## 次のステップ

- [02_rct](02_rct.md) —— 多群 RCT。
- [03_causal](03_causal.md) —— 反事実解析と ATE。
- [04_case_studies](04_case_studies.md) —— 内蔵臨床ケース。
