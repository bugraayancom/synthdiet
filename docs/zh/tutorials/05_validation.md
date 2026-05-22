# 对照已发表 RCT 校验 `synthdiet`

`synthdiet.validation` 会将整套模拟器与一组已发表的临床试验
结果进行比对。预期效应来自同行评议论文,并标注引用出处。

## 内置目标

| 目标 | 引用 | 结局 | 预期 |
|------|------|------|------|
| DASH-Sodium | Sacks NEJM 2001;344:3-10 | ΔSBP (mmHg) | -11.5 |
| PREDIMED | Estruch NEJM 2018;378:e34 | ΔLDL (mg/dL) | -6.0 |
| DiRECT | Lean Lancet 2018;391:541-51 | Δ体重 (kg) | -10.0 |
| Look AHEAD | Look AHEAD Diabetes Care 2007;30:1374-83 | Δ体重 (kg) | -7.9 |
| DPP | Knowler NEJM 2002;346:393-403 | Δ体重 (kg) | -5.5 |

## 运行全部校验

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

## 在 CI 中使用

校验套件在 pytest 中标记为 ``slow``,以避免拖慢日常测试:

```bash
pytest -m slow tests/test_validation.py -v
```

## 解读失败

FAIL 表示模拟器超出文档容差。常见原因:

- 疾病响应模型回归;
- 默认饮食宏量改变,使生物标志物预测值越界;
- 依从/脱落变化导致欠校正或过度校正。

在质疑已发表效应之前,请先检查相关疾病的 `response_to_diet` 钩子
以及 Hall 模型的校准常数。
