# Cas cliniques pour l'enseignement

Le module `synthdiet.education` propose **15 cas cliniques** prêts
à être utilisés en cours : syndrome métabolique, sujet âgé BPCO,
diabète gestationnel, IRC, maladie cœliaque, anorexie, dyspepsie,
cachexie cancéreuse, etc.

## Lister les cas disponibles

```python
from synthdiet.education import list_cases
print(list_cases())
```

## Afficher un cas en Markdown

```python
from synthdiet.education import get_case

case = get_case("t2dm_ht_dyslipidemia")
print(case.as_markdown())
```

Le Markdown contient :

- motif de consultation et antécédents,
- profil du patient (démographie, IMC, diagnostics, traitements),
- valeurs biologiques,
- objectifs pédagogiques.

## Inspecter la solution de référence

```python
print(case.reference_solution.summary)
print(case.reference_solution.prescribed_diet.summary())
for outcome in case.reference_solution.expected_outcomes:
    print("attendu :", outcome)
```

## Notation type ECOS

```python
from synthdiet.education import OSCEStation
from synthdiet.diets import mediterranean_diet

station = OSCEStation(case=case)
student_diet = mediterranean_diet(daily_energy_kcal=1700)
score = station.grade(student_diet)
print(score.pretty())
```

La grille par défaut accorde 4 points à chacun des 5 critères
(20 au total) : adéquation énergétique, absence d'aliments interdits,
apport protéique suffisant, sodium dans la limite spécifique de la
maladie, sucres ajoutés ≤ 10 %.

## Personnaliser la grille

```python
from synthdiet.education import OSCERubric

extra = OSCERubric(
    code="R6",
    description="Fibres >= 30 g/jour",
    points=4.0,
    check=lambda plan, case: (plan.fiber_g_per_day or 0) >= 30,
)
station = OSCEStation(case=case, rubric=station._default_rubric() + [extra])
```

## Fiche de travail pour la classe

```python
from synthdiet.education import built_in_cases

with open("fiche_travail.html", "w", encoding="utf-8") as fh:
    for c in built_in_cases():
        fh.write(c.as_html())
        fh.write("<hr/>")
```
