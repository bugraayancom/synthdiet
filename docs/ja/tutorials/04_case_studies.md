# 教育における臨床ケースの活用

`synthdiet.education` には授業ですぐ使える **15 の臨床ケース**
が含まれています:メタボリックシンドローム、COPD の高齢患者、
妊娠糖尿病、慢性腎臓病、セリアック病、神経性やせ症、機能性
ディスペプシア、がん悪液質 など。

## 利用可能なケース一覧

```python
from synthdiet.education import list_cases
print(list_cases())
```

## ケースを Markdown で表示

```python
from synthdiet.education import get_case

case = get_case("t2dm_ht_dyslipidemia")
print(case.as_markdown())
```

Markdown 出力には次が含まれます:

- 主訴と病歴
- 患者プロフィール(人口統計、BMI、診断、薬剤)
- 検査値
- 学習目標

## 参照解答の確認

```python
print(case.reference_solution.summary)
print(case.reference_solution.prescribed_diet.summary())
for outcome in case.reference_solution.expected_outcomes:
    print("期待値:", outcome)
```

## OSCE 形式の採点

```python
from synthdiet.education import OSCEStation
from synthdiet.diets import mediterranean_diet

station = OSCEStation(case=case)
student_diet = mediterranean_diet(daily_energy_kcal=1700)
score = station.grade(student_diet)
print(score.pretty())
```

デフォルトのルーブリックは 5 項目に各 4 点(計 20 点)を割り当て
ます:エネルギー適正、禁忌食品なし、たんぱく質充足、疾患特異的
ナトリウム上限内、添加糖 ≤ 10%。

## ルーブリックのカスタマイズ

```python
from synthdiet.education import OSCERubric

extra = OSCERubric(
    code="R6",
    description="食物繊維 >= 30 g/日",
    points=4.0,
    check=lambda plan, case: (plan.fiber_g_per_day or 0) >= 30,
)
station = OSCEStation(case=case, rubric=station._default_rubric() + [extra])
```

## クラス用ワークシートの一括生成

```python
from synthdiet.education import built_in_cases

with open("worksheet.html", "w", encoding="utf-8") as fh:
    for c in built_in_cases():
        fh.write(c.as_html())
        fh.write("<hr/>")
```
