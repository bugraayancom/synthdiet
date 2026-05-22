# Validar `synthdiet` frente a ECAs publicados

`synthdiet.validation` ejecuta el simulador completo contra un panel
de resultados de ensayos publicados. Los efectos esperados provienen
de artículos revisados por pares y están documentados con su cita.

## Objetivos incluidos

| Objetivo | Cita | Resultado | Esperado |
|----------|------|-----------|----------|
| DASH-Sodium | Sacks NEJM 2001;344:3-10 | ΔPAS (mmHg) | -11,5 |
| PREDIMED | Estruch NEJM 2018;378:e34 | ΔLDL (mg/dL) | -6,0 |
| DiRECT | Lean Lancet 2018;391:541-51 | Δpeso (kg) | -10,0 |
| Look AHEAD | Look AHEAD Diabetes Care 2007;30:1374-83 | Δpeso (kg) | -7,9 |
| DPP | Knowler NEJM 2002;346:393-403 | Δpeso (kg) | -5,5 |

## Ejecutar todas las validaciones

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

## Uso en CI

La suite está marcada como ``slow`` en pytest para no ralentizar las
ejecuciones rápidas:

```bash
pytest -m slow tests/test_validation.py -v
```

## Interpretación de fallos

Un FAIL significa que el simulador se desvió más de la tolerancia
documentada. Causas típicas:

- Una regresión en el modelo de respuesta de la enfermedad.
- Cambios en los macronutrientes por defecto que sacan de rango las
  proyecciones de biomarcadores.
- Un cambio de adherencia/abandono que sub o sobre-corrige.

Antes de cuestionar el efecto publicado, revise el hook
`response_to_diet` de cada enfermedad y las constantes de calibración
del modelo de Hall.
