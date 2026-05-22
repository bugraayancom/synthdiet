# Using clinical case studies in teaching

The `synthdiet.education` module ships 15 ready-to-teach clinical scenarios.

## List available cases

```python
from synthdiet.education import list_cases
print(list_cases())
```

## Display a case as Markdown

```python
from synthdiet.education import get_case

case = get_case("t2dm_ht_dyslipidemia")
print(case.as_markdown())
```

The output includes:

- Chief complaint and history
- Patient profile (demographics, BMI, diagnoses, medications)
- Lab values
- Learning objectives

## Inspect the reference solution

```python
print(case.reference_solution.summary)
print(case.reference_solution.prescribed_diet.summary())
for outcome in case.reference_solution.expected_outcomes:
    print("expected:", outcome)
```

## OSCE-style grading

Give students a diet plan to design, then grade their submission:

```python
from synthdiet.education import OSCEStation
from synthdiet.diets import mediterranean_diet

station = OSCEStation(case=case)
student_diet = mediterranean_diet(daily_energy_kcal=1700)
score = station.grade(student_diet)
print(score.pretty())
```

The default rubric awards 4 points each for 5 criteria (20 total):
energy appropriateness, no forbidden foods, protein adequacy,
sodium within the disease-specific cap, and added sugar ≤ 10%.

## Customise the rubric

```python
from synthdiet.education import OSCERubric

extra = OSCERubric(
    code="R6",
    description="Fibre >= 30 g/day",
    points=4.0,
    check=lambda plan, case: (plan.fiber_g_per_day or 0) >= 30,
)
station = OSCEStation(case=case, rubric=station._default_rubric() + [extra])
```

## Bulk-print a worksheet for a class

```python
from synthdiet.education import built_in_cases

with open("worksheet.html", "w") as fh:
    for c in built_in_cases():
        fh.write(c.as_html())
        fh.write("<hr/>")
```
