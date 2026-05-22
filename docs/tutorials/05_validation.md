# Validating synthdiet against published RCTs

`synthdiet.validation` runs the full simulator against a panel of published
trial results. The expected effects come from peer-reviewed papers and are
documented with their citation.

## Bundled targets

| Target | Citation | Outcome | Expected |
|--------|----------|---------|----------|
| DASH-Sodium | Sacks NEJM 2001;344:3-10 | ΔSBP (mmHg) | -11.5 |
| PREDIMED | Estruch NEJM 2018;378:e34 | ΔLDL (mg/dL) | -6.0 |
| DiRECT | Lean Lancet 2018;391:541-51 | Δweight (kg) | -10.0 |
| Look AHEAD | Look AHEAD Diabetes Care 2007;30:1374-83 | Δweight (kg) | -7.9 |
| DPP | Knowler NEJM 2002;346:393-403 | Δweight (kg) | -5.5 |

## Run all validations

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

## Use in CI

The validation suite is marked ``slow`` in pytest so it does not block fast
test runs. To execute it:

```bash
pytest -m slow tests/test_validation.py -v
```

## Interpreting failures

A validation FAIL means the simulator deviated more than the documented
tolerance from the published RCT. Causes are usually:

- A regression in the disease response model.
- A change to default diet macros that pushes biomarker projections out
  of range.
- An adherence/dropout change that under- or over-corrects.

When this happens, investigate the per-disease ``response_to_diet`` hook and
the Hall model's calibration constants before considering the published
effect to be wrong.
