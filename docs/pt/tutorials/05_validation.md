# Validar `synthdiet` contra ECRs publicados

`synthdiet.validation` executa o simulador completo contra um painel
de resultados publicados. Os efeitos esperados vêm de artigos
revisados por pares e estão documentados com a citação.

## Alvos incluídos

| Alvo | Citação | Desfecho | Esperado |
|------|---------|----------|----------|
| DASH-Sodium | Sacks NEJM 2001;344:3-10 | ΔPAS (mmHg) | -11,5 |
| PREDIMED | Estruch NEJM 2018;378:e34 | ΔLDL (mg/dL) | -6,0 |
| DiRECT | Lean Lancet 2018;391:541-51 | Δpeso (kg) | -10,0 |
| Look AHEAD | Look AHEAD Diabetes Care 2007;30:1374-83 | Δpeso (kg) | -7,9 |
| DPP | Knowler NEJM 2002;346:393-403 | Δpeso (kg) | -5,5 |

## Executar todas as validações

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

## Uso em CI

A suíte está marcada como ``slow`` no pytest:

```bash
pytest -m slow tests/test_validation.py -v
```

## Interpretando falhas

Um FAIL significa que o simulador desviou além da tolerância
documentada. Causas típicas:

- regressão no modelo de resposta da doença,
- mudanças nos macronutrientes padrão que tiram os biomarcadores
  da faixa esperada,
- alteração de adesão/abandono que sub ou supercorrige.

Antes de questionar o efeito publicado, revise o hook
`response_to_diet` da doença e as constantes de calibração do
modelo de Hall.
