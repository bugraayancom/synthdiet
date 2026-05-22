# Casos clínicos para enseñanza

El módulo `synthdiet.education` incluye **15 casos clínicos** listos
para usar en clase: síndrome metabólico, paciente mayor con EPOC,
diabetes gestacional, enfermedad renal crónica, celiaquía, anorexia,
dispepsia, caquexia oncológica, etc.

## Listar los casos disponibles

```python
from synthdiet.education import list_cases
print(list_cases())
```

## Mostrar un caso en Markdown

```python
from synthdiet.education import get_case

case = get_case("t2dm_ht_dyslipidemia")
print(case.as_markdown())
```

El Markdown contiene:

- Motivo de consulta y antecedentes,
- Perfil del paciente (demografía, IMC, diagnósticos, medicación),
- Valores de laboratorio,
- Objetivos de aprendizaje.

## Inspeccionar la solución de referencia

```python
print(case.reference_solution.summary)
print(case.reference_solution.prescribed_diet.summary())
for outcome in case.reference_solution.expected_outcomes:
    print("esperado:", outcome)
```

## Calificación tipo OSCE

```python
from synthdiet.education import OSCEStation
from synthdiet.diets import mediterranean_diet

station = OSCEStation(case=case)
student_diet = mediterranean_diet(daily_energy_kcal=1700)
score = station.grade(student_diet)
print(score.pretty())
```

La rúbrica por defecto otorga 4 puntos a cada uno de 5 criterios
(20 en total): adecuación energética, ausencia de alimentos
prohibidos, suficiencia proteica, sodio dentro del límite específico
de la enfermedad, y azúcares añadidos ≤ 10%.

## Personalizar la rúbrica

```python
from synthdiet.education import OSCERubric

extra = OSCERubric(
    code="R6",
    description="Fibra >= 30 g/día",
    points=4.0,
    check=lambda plan, case: (plan.fiber_g_per_day or 0) >= 30,
)
station = OSCEStation(case=case, rubric=station._default_rubric() + [extra])
```

## Hoja de trabajo masiva para una clase

```python
from synthdiet.education import built_in_cases

with open("hoja_trabajo.html", "w", encoding="utf-8") as fh:
    for c in built_in_cases():
        fh.write(c.as_html())
        fh.write("<hr/>")
```
