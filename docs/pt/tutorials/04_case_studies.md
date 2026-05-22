# Casos clínicos para ensino

O módulo `synthdiet.education` traz **15 casos clínicos** prontos
para uso em sala: síndrome metabólica, idoso com DPOC, diabetes
gestacional, doença renal crônica, doença celíaca, anorexia,
dispepsia, caquexia oncológica, etc.

## Listar casos disponíveis

```python
from synthdiet.education import list_cases
print(list_cases())
```

## Mostrar um caso em Markdown

```python
from synthdiet.education import get_case

case = get_case("t2dm_ht_dyslipidemia")
print(case.as_markdown())
```

A saída inclui:

- queixa principal e história,
- perfil do paciente (demografia, IMC, diagnósticos, medicações),
- valores laboratoriais,
- objetivos de aprendizagem.

## Inspecionar a solução de referência

```python
print(case.reference_solution.summary)
print(case.reference_solution.prescribed_diet.summary())
for outcome in case.reference_solution.expected_outcomes:
    print("esperado:", outcome)
```

## Avaliação tipo OSCE

```python
from synthdiet.education import OSCEStation
from synthdiet.diets import mediterranean_diet

station = OSCEStation(case=case)
student_diet = mediterranean_diet(daily_energy_kcal=1700)
score = station.grade(student_diet)
print(score.pretty())
```

A rubrica padrão atribui 4 pontos a cada um de 5 critérios (20 no
total): adequação energética, ausência de alimentos proibidos,
suficiência proteica, sódio dentro do limite específico da doença,
açúcares adicionados ≤ 10%.

## Personalizar a rubrica

```python
from synthdiet.education import OSCERubric

extra = OSCERubric(
    code="R6",
    description="Fibras >= 30 g/dia",
    points=4.0,
    check=lambda plan, case: (plan.fiber_g_per_day or 0) >= 30,
)
station = OSCEStation(case=case, rubric=station._default_rubric() + [extra])
```

## Folha de exercícios para a turma

```python
from synthdiet.education import built_in_cases

with open("exercicios.html", "w", encoding="utf-8") as fh:
    for c in built_in_cases():
        fh.write(c.as_html())
        fh.write("<hr/>")
```
