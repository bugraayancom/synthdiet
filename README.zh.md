# synthdiet

[![PyPI](https://img.shields.io/pypi/v/synthdiet.svg)](https://pypi.org/project/synthdiet/)
[![Python](https://img.shields.io/pypi/pyversions/synthdiet.svg)](https://pypi.org/project/synthdiet/)
[![许可证: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/bugraayancom/synthdiet/actions/workflows/ci.yml/badge.svg)](https://github.com/bugraayancom/synthdiet/actions/workflows/ci.yml)

> 其他语言: [English](README.md) · [Türkçe](README.tr.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português](README.pt.md) · [Italiano](README.it.md) · [日本語](README.ja.md)
`synthdiet` 是一个用于**生成具有真实临床特征的合成患者**并对其
**模拟饮食干预**的 Python 库。

它面向营养师、临床营养研究人员和教育工作者,可以在将膳食方案
应用于真实临床之前,先在数百到数千名合成患者上对方案进行原型
设计、虚拟试验以及压力测试。

> 免责声明:`synthdiet` 是一个研究与教学工具。其输出的数值
> **不是临床建议**,合成患者**也不是真实人物**。患者诊疗请始终
> 咨询合格的注册营养师/临床营养师。

![synthdiet hero](app/assets/screenshots/00_hero.png)

---

## 作者

**Buğra Ayan** —— 土耳其安卡拉
- 网站: <https://bugraayan.com>
- 邮箱: <bugraayan.com@gmail.com>
- Google Scholar: <https://scholar.google.com/citations?user=VHGqzNMAAAAJ&hl=tr>

---

## 功能特性

### 核心领域模型
- 一个带类型注解的 `Patient` 类,聚合了人口学、人体测量、
  生活方式、实验室生物标志物、诊断和当前用药信息。
- **25+ 种疾病注册表**,涵盖内分泌、心血管、肾脏、肝脏、
  胃肠道、代谢、肌骨、肿瘤、精神、过敏等类别。
- **19 项临床上重要的药物-营养素相互作用**(二甲双胍 → B12、
  他汀类 → 西柚、华法林 → 维生素 K、左甲状腺素服用时点、
  MAOI 与酪胺危机等)的注册表。
- 5 种合成患者生成器(随机、分布、Copula、队列、马尔可夫进展)。
- 包含 45 种食物(含宏量/微量营养素分解)的食物数据库,以及
  8 种预设饮食(地中海、DASH、生酮、低 FODMAP、低钠肾脏、
  糖尿病、纯素、标准)。

### 方法学深度(v0.1)
- 可选的 **Hall 2011 体成分模型**(`DietSimulator(engine="hall_2011")`),
  使用 Forbes 公式进行脂肪/瘦体质量分配并加入适应性产热。
- **依从性与脱落动力学**:恒定、衰减、Weibull 脱落、随机漏服、
  感知负担。
- **RCT 引擎**(`synthdiet.trials`):平行组、交叉、2×2 析因设计;
  分层 / 区组 / 最小化随机化;脱落建模;ITT/PP/AT 分析。
- **因果推断**(`synthdiet.causal`):反事实模拟、ATE/CATE
  估计器、IPTW 与 g-公式校正的混杂实验、轻量 DAG。
- **饮食质量指数**(`synthdiet.indices`):HEI-2020、AHEI-2010、
  MEDAS、DASH 评分、PHDI、DII。
- **统计辅助工具**(`synthdiet.stats`):连续/二分类结局的功效
  分析、Bootstrap CI、置换检验、Benjamini-Hochberg 与
  Holm-Bonferroni 校正、基线调整 ANCOVA。
- **测量误差与缺失数据注入**(`synthdiet.noise`):各检测的 CV%、
  自报偏倚、MCAR/MAR/MNAR 模式。
- **15 个临床案例 + OSCE 风格评分**(`synthdiet.education`)。
- 与 5 个里程碑式 RCT 的**校验套件**(`synthdiet.validation`):
  DASH-Sodium、PREDIMED、DiRECT、Look AHEAD、Diabetes Prevention
  Program。
- **可视化**(`synthdiet.viz`,可选):CONSORT 图、森林图、
  轨迹带、Table 1。

---

## 安装

```bash
pip install synthdiet
```

可选附加项:

```bash
pip install "synthdiet[viz]"     # matplotlib 可视化
pip install "synthdiet[causal]"  # networkx DAG 导出
pip install "synthdiet[docs]"    # Sphinx + furo + myst-parser
pip install "synthdiet[dev]"     # pytest + ruff + mypy + matplotlib
```

`synthdiet` 需要 Python 3.9+,依赖 `numpy`、`pandas`、`scipy`。

---

## 60 秒上手

```python
from synthdiet import (
    CohortGenerator, CohortSpec, DiseaseSpec,
    DietSimulator, mediterranean_diet,
    evaluate_simulation, format_evaluation_report,
)

spec = CohortSpec(
    size=100,
    diseases=[
        DiseaseSpec("type_2_diabetes", prevalence=0.40),
        DiseaseSpec("hypertension",     prevalence=0.45),
    ],
)
cohort = CohortGenerator(spec, seed=42).generate()

simulator = DietSimulator(adherence=0.8)
diet = mediterranean_diet(daily_energy_kcal=1800)

for patient in cohort[:3]:
    result = simulator.run(patient, diet, duration_weeks=12)
    evaluation = evaluate_simulation(result)
    print(format_evaluation_report(evaluation))
    print("-" * 60)
```

完整示例参见 [`examples/`](examples/);中文教程位于
[`docs/zh/`](docs/zh/)。

---

## 引用

```bibtex
@software{ayan_synthdiet_2026,
  author  = {Buğra Ayan},
  title   = {synthdiet: A Python library for simulating diets on synthetic patients},
  year    = {2026},
  version = {0.1.0},
  url     = {https://bugraayan.com}
}
```

## 许可证

MIT —— 详见 [`LICENSE`](LICENSE)。
