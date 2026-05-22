# 在教学中使用临床案例

`synthdiet.education` 模块内置 **15 个临床案例**:代谢综合征、
慢阻肺老年患者、妊娠糖尿病、慢性肾脏病、乳糜泻、神经性厌食、
功能性消化不良、肿瘤恶病质等。

## 列出可用案例

```python
from synthdiet.education import list_cases
print(list_cases())
```

## 以 Markdown 显示一个案例

```python
from synthdiet.education import get_case

case = get_case("t2dm_ht_dyslipidemia")
print(case.as_markdown())
```

Markdown 输出包括:

- 主诉与病史,
- 患者画像(人口学、BMI、诊断、用药),
- 化验结果,
- 学习目标。

## 查看参考答案

```python
print(case.reference_solution.summary)
print(case.reference_solution.prescribed_diet.summary())
for outcome in case.reference_solution.expected_outcomes:
    print("预期:", outcome)
```

## OSCE 风格评分

```python
from synthdiet.education import OSCEStation
from synthdiet.diets import mediterranean_diet

station = OSCEStation(case=case)
student_diet = mediterranean_diet(daily_energy_kcal=1700)
score = station.grade(student_diet)
print(score.pretty())
```

默认评分量表对 5 项标准各给 4 分(共 20 分):能量充足性、无禁忌
食物、蛋白足量、钠在疾病特异性上限内、添加糖 ≤ 10%。

## 自定义量表

```python
from synthdiet.education import OSCERubric

extra = OSCERubric(
    code="R6",
    description="膳食纤维 >= 30 g/天",
    points=4.0,
    check=lambda plan, case: (plan.fiber_g_per_day or 0) >= 30,
)
station = OSCEStation(case=case, rubric=station._default_rubric() + [extra])
```

## 为整堂课批量生成习题册

```python
from synthdiet.education import built_in_cases

with open("worksheet.html", "w", encoding="utf-8") as fh:
    for c in built_in_cases():
        fh.write(c.as_html())
        fh.write("<hr/>")
```
