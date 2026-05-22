# 既発表 RCT に対する `synthdiet` のバリデーション

`synthdiet.validation` はシミュレータ全体を、既発表の試験結果の
パネルに対して実行します。期待される効果は査読付き論文に基づいて
おり、引用とともに文書化されています。

## 同梱ターゲット

| ターゲット | 引用 | アウトカム | 期待値 |
|------------|------|------------|--------|
| DASH-Sodium | Sacks NEJM 2001;344:3-10 | ΔSBP (mmHg) | -11.5 |
| PREDIMED | Estruch NEJM 2018;378:e34 | ΔLDL (mg/dL) | -6.0 |
| DiRECT | Lean Lancet 2018;391:541-51 | Δ体重 (kg) | -10.0 |
| Look AHEAD | Look AHEAD Diabetes Care 2007;30:1374-83 | Δ体重 (kg) | -7.9 |
| DPP | Knowler NEJM 2002;346:393-403 | Δ体重 (kg) | -5.5 |

## すべてのバリデーションを実行

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

## CI での利用

バリデーションスイートは pytest 上で ``slow`` マーカーが付いて
おり、通常テスト実行をブロックしません。実行例:

```bash
pytest -m slow tests/test_validation.py -v
```

## 失敗の解釈

FAIL は、シミュレータが文書化された許容差を超えて逸脱したことを
意味します。典型的な原因:

- 疾患レスポンスモデルのリグレッション
- デフォルト食事のマクロ栄養素変更によるバイオマーカーの逸脱
- アドヒアランス/ドロップアウトの不足/過剰補正

既発表効果が誤りだと結論する前に、当該疾患の `response_to_diet`
フックと Hall モデルのキャリブレーション定数を確認してください。
