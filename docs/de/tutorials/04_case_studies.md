# Klinische Fallstudien in der Lehre

Das Modul `synthdiet.education` enthält **15 fertige klinische
Szenarien**: metabolisches Syndrom, betagte\*r Patient\*in mit COPD,
Gestationsdiabetes, chronische Niereninsuffizienz, Zöliakie, Anorexie,
Dyspepsie, Tumor-Kachexie usw.

## Verfügbare Fälle auflisten

```python
from synthdiet.education import list_cases
print(list_cases())
```

## Fall als Markdown anzeigen

```python
from synthdiet.education import get_case

case = get_case("t2dm_ht_dyslipidemia")
print(case.as_markdown())
```

Markdown-Ausgabe enthält:

- Beratungsanlass und Anamnese,
- Patient\*innenprofil (Demografie, BMI, Diagnosen, Medikation),
- Laborwerte,
- Lernziele.

## Referenzlösung einsehen

```python
print(case.reference_solution.summary)
print(case.reference_solution.prescribed_diet.summary())
for outcome in case.reference_solution.expected_outcomes:
    print("erwartet:", outcome)
```

## OSCE-artige Bewertung

```python
from synthdiet.education import OSCEStation
from synthdiet.diets import mediterranean_diet

station = OSCEStation(case=case)
student_diet = mediterranean_diet(daily_energy_kcal=1700)
score = station.grade(student_diet)
print(score.pretty())
```

Die Standardrubrik vergibt je 4 Punkte für 5 Kriterien (insgesamt
20): Energieadäquanz, keine verbotenen Lebensmittel,
Proteinausreichung, Natrium innerhalb des krankheitsspezifischen
Limits, zugesetzter Zucker ≤ 10 %.

## Rubrik anpassen

```python
from synthdiet.education import OSCERubric

extra = OSCERubric(
    code="R6",
    description="Ballaststoffe >= 30 g/Tag",
    points=4.0,
    check=lambda plan, case: (plan.fiber_g_per_day or 0) >= 30,
)
station = OSCEStation(case=case, rubric=station._default_rubric() + [extra])
```

## Arbeitsblatt für eine Klasse erzeugen

```python
from synthdiet.education import built_in_cases

with open("arbeitsblatt.html", "w", encoding="utf-8") as fh:
    for c in built_in_cases():
        fh.write(c.as_html())
        fh.write("<hr/>")
```
