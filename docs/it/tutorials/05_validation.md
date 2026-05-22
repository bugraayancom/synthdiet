# Validare `synthdiet` rispetto a RCT pubblicati

`synthdiet.validation` esegue il simulatore completo contro un panel
di risultati di studi pubblicati. Gli effetti attesi provengono da
pubblicazioni peer-reviewed e sono documentati con la citazione.

## Target inclusi

| Target | Citazione | Esito | Atteso |
|--------|-----------|-------|--------|
| DASH-Sodium | Sacks NEJM 2001;344:3-10 | ΔSBP (mmHg) | -11,5 |
| PREDIMED | Estruch NEJM 2018;378:e34 | ΔLDL (mg/dL) | -6,0 |
| DiRECT | Lean Lancet 2018;391:541-51 | Δpeso (kg) | -10,0 |
| Look AHEAD | Look AHEAD Diabetes Care 2007;30:1374-83 | Δpeso (kg) | -7,9 |
| DPP | Knowler NEJM 2002;346:393-403 | Δpeso (kg) | -5,5 |

## Eseguire tutte le validazioni

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

## Uso in CI

La suite è marcata ``slow`` in pytest:

```bash
pytest -m slow tests/test_validation.py -v
```

## Interpretare i fallimenti

Un FAIL significa che il simulatore si è discostato oltre la
tolleranza documentata. Cause tipiche:

- regressione nel modello di risposta della patologia,
- modifiche dei macronutrienti predefiniti che spingono i
  biomarcatori fuori intervallo,
- variazione di aderenza/abbandono che sotto- o sovra-corregge.

Prima di mettere in dubbio l'effetto pubblicato, verificare l'hook
`response_to_diet` della patologia e le costanti di calibrazione
del modello di Hall.
