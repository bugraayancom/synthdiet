# Valider `synthdiet` contre des ECR publiés

`synthdiet.validation` exécute le simulateur complet contre un panel
de résultats d'essais publiés. Les effets attendus proviennent
d'articles évalués par les pairs et sont documentés avec leur
référence.

## Cibles incluses

| Cible | Référence | Critère | Attendu |
|-------|-----------|---------|---------|
| DASH-Sodium | Sacks NEJM 2001;344:3-10 | ΔPAS (mmHg) | -11,5 |
| PREDIMED | Estruch NEJM 2018;378:e34 | ΔLDL (mg/dL) | -6,0 |
| DiRECT | Lean Lancet 2018;391:541-51 | Δpoids (kg) | -10,0 |
| Look AHEAD | Look AHEAD Diabetes Care 2007;30:1374-83 | Δpoids (kg) | -7,9 |
| DPP | Knowler NEJM 2002;346:393-403 | Δpoids (kg) | -5,5 |

## Lancer toutes les validations

```python
from synthdiet.validation import (
    validate_dash_sodium, validate_predimed, validate_direct,
    validate_look_ahead, validate_dpp,
)

for validator in (
    validate_dash_sodium, validate_predimed, validate_direct,
    validate_look_ahead, validate_dpp,
):
    report = validator(n_patients=120, seed=42)
    print(report.pretty())
```

## Utilisation en CI

La suite est marquée ``slow`` dans pytest pour ne pas ralentir les
tests rapides :

```bash
pytest -m slow tests/test_validation.py -v
```

## Interpréter les échecs

Un FAIL signifie que le simulateur s'est écarté au-delà de la
tolérance documentée. Causes typiques :

- régression dans le modèle de réponse de la maladie,
- changement des macronutriments par défaut sortant les biomarqueurs
  de la plage attendue,
- modification de l'adhésion/abandon sous- ou sur-corrigée.

Avant de remettre en cause l'effet publié, vérifiez le hook
`response_to_diet` de la maladie concernée et les constantes de
calibration du modèle de Hall.
