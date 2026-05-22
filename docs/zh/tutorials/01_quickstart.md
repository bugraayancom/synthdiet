# 快速上手

本教程展示一个典型的 `synthdiet` 工作流:

1. 生成合成患者,
2. 添加疾病,
3. 应用饮食,
4. 模拟 12 周,
5. 评估结果。

## 安装

```bash
pip install synthdiet
```

## 创建患者

```python
from synthdiet import (
    Anthropometrics, Demographics, Lifestyle, Patient, Sex,
)
from synthdiet.diseases import Type2Diabetes
from synthdiet.patients.lifestyle import ActivityLevel

patient = Patient(
    demographics=Demographics(age=57, sex=Sex.MALE, country="CN"),
    anthropometrics=Anthropometrics(height_cm=176, weight_kg=98, waist_cm=108),
    lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT),
)
patient.add_disease(Type2Diabetes(severity="moderate"))
print(patient.summary())
```

## 选择预设饮食

```python
from synthdiet import mediterranean_diet

diet = mediterranean_diet(daily_energy_kcal=1800)
print(diet.summary())
```

## 运行模拟器

默认模拟器使用简单的能量平衡规则(7700 kcal/kg)。如需更真实的
长期预测,可启用 Hall 模型:

```python
from synthdiet import DietSimulator

sim = DietSimulator(adherence=0.85, engine="hall_2011")
result = sim.run(patient, diet, duration_weeks=24)
print(f"24 周体重变化: {result.weight_change_kg:+.2f} kg")
```

## 评估结果

```python
from synthdiet import evaluate_simulation, format_evaluation_report

evaluation = evaluate_simulation(result)
print(format_evaluation_report(evaluation))
```

## 检查饮食限制

```python
warnings = sim.check_diet_against_constraints(patient, diet)
for w in warnings:
    print("警告:", w)
```

## 下一步

- [02_rct](02_rct.md) —— 多臂 RCT。
- [03_causal](03_causal.md) —— 反事实分析与 ATE。
- [04_case_studies](04_case_studies.md) —— 内置临床案例。
