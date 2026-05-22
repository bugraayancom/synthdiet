# `synthdiet` gegen publizierte RCTs validieren

`synthdiet.validation` führt den vollen Simulator gegen ein Panel
publizierter Studienergebnisse aus. Die erwarteten Effekte stammen
aus peer-reviewed Publikationen und sind mit Zitation dokumentiert.

## Mitgelieferte Ziele

| Ziel | Zitation | Endpunkt | Erwartet |
|------|----------|----------|----------|
| DASH-Sodium | Sacks NEJM 2001;344:3-10 | ΔSBP (mmHg) | -11,5 |
| PREDIMED | Estruch NEJM 2018;378:e34 | ΔLDL (mg/dL) | -6,0 |
| DiRECT | Lean Lancet 2018;391:541-51 | ΔGewicht (kg) | -10,0 |
| Look AHEAD | Look AHEAD Diabetes Care 2007;30:1374-83 | ΔGewicht (kg) | -7,9 |
| DPP | Knowler NEJM 2002;346:393-403 | ΔGewicht (kg) | -5,5 |

## Alle Validierungen ausführen

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

## Einsatz in CI

Die Suite ist in pytest als ``slow`` markiert, damit schnelle Läufe
nicht ausgebremst werden:

```bash
pytest -m slow tests/test_validation.py -v
```

## Fehler interpretieren

Ein FAIL bedeutet, dass der Simulator außerhalb der dokumentierten
Toleranz liegt. Typische Ursachen:

- Regression im Krankheits-Antwortmodell,
- Änderungen der voreingestellten Makronährstoffe, die Biomarker
  außerhalb des Bereichs bringen,
- Adhärenz-/Drop-out-Änderung, die unter- oder überkorrigiert.

Bevor Sie den publizierten Effekt anzweifeln, prüfen Sie den
`response_to_diet`-Hook der jeweiligen Krankheit und die
Kalibrationskonstanten des Hall-Modells.
