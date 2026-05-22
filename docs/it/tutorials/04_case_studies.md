# Casi clinici per la didattica

Il modulo `synthdiet.education` include **15 casi clinici** pronti
per l'uso in aula: sindrome metabolica, anziano con BPCO, diabete
gestazionale, insufficienza renale cronica, celiachia, anoressia,
dispepsia, cachessia oncologica, ecc.

## Elencare i casi disponibili

```python
from synthdiet.education import list_cases
print(list_cases())
```

## Mostrare un caso in Markdown

```python
from synthdiet.education import get_case

case = get_case("t2dm_ht_dyslipidemia")
print(case.as_markdown())
```

L'output Markdown contiene:

- motivo della visita e anamnesi,
- profilo del paziente (demografia, BMI, diagnosi, farmaci),
- valori di laboratorio,
- obiettivi formativi.

## Soluzione di riferimento

```python
print(case.reference_solution.summary)
print(case.reference_solution.prescribed_diet.summary())
for outcome in case.reference_solution.expected_outcomes:
    print("atteso:", outcome)
```

## Valutazione tipo OSCE

```python
from synthdiet.education import OSCEStation
from synthdiet.diets import mediterranean_diet

station = OSCEStation(case=case)
student_diet = mediterranean_diet(daily_energy_kcal=1700)
score = station.grade(student_diet)
print(score.pretty())
```

La rubrica predefinita assegna 4 punti a ciascuno di 5 criteri (20
totali): adeguatezza energetica, assenza di alimenti vietati,
adeguatezza proteica, sodio entro il limite specifico della patologia
e zuccheri aggiunti ≤ 10%.

## Personalizzare la rubrica

```python
from synthdiet.education import OSCERubric

extra = OSCERubric(
    code="R6",
    description="Fibre >= 30 g/die",
    points=4.0,
    check=lambda plan, case: (plan.fiber_g_per_day or 0) >= 30,
)
station = OSCEStation(case=case, rubric=station._default_rubric() + [extra])
```

## Foglio di lavoro per la classe

```python
from synthdiet.education import built_in_cases

with open("foglio_lavoro.html", "w", encoding="utf-8") as fh:
    for c in built_in_cases():
        fh.write(c.as_html())
        fh.write("<hr/>")
```
