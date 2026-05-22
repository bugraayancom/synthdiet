# Início rápido

Este tutorial percorre um fluxo típico do `synthdiet`:

1. gerar um paciente sintético,
2. atribuir uma doença,
3. aplicar uma dieta,
4. simular 12 semanas,
5. avaliar o resultado.

## Instalação

```bash
pip install synthdiet
```

## Criar um paciente

```python
from synthdiet import (
    Anthropometrics, Demographics, Lifestyle, Patient, Sex,
)
from synthdiet.diseases import Type2Diabetes
from synthdiet.patients.lifestyle import ActivityLevel

patient = Patient(
    demographics=Demographics(age=57, sex=Sex.MALE, country="BR"),
    anthropometrics=Anthropometrics(height_cm=176, weight_kg=98, waist_cm=108),
    lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT),
)
patient.add_disease(Type2Diabetes(severity="moderate"))
print(patient.summary())
```

## Escolher uma dieta

```python
from synthdiet import mediterranean_diet

diet = mediterranean_diet(daily_energy_kcal=1800)
print(diet.summary())
```

## Executar o simulador

O simulador padrão usa a regra simples de balanço energético
(7700 kcal/kg). Para projeções de longo prazo mais realistas, ative
o modelo de Hall:

```python
from synthdiet import DietSimulator

sim = DietSimulator(adherence=0.85, engine="hall_2011")
result = sim.run(patient, diet, duration_weeks=24)
print(f"Variação de peso em 24 semanas: {result.weight_change_kg:+.2f} kg")
```

## Avaliar o resultado

```python
from synthdiet import evaluate_simulation, format_evaluation_report

evaluation = evaluate_simulation(result)
print(format_evaluation_report(evaluation))
```

## Verificar restrições

```python
warnings = sim.check_diet_against_constraints(patient, diet)
for w in warnings:
    print("Aviso:", w)
```

## Próximos passos

- [02_rct](02_rct.md) — ECR multi-braços.
- [03_causal](03_causal.md) — análises contrafactuais.
- [04_case_studies](04_case_studies.md) — casos clínicos integrados.
