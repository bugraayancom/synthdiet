# API 参考

本页以中文简要列出 `synthdiet` 的公共 API。完整的 Sphinx
自动文档为英文,本表用于快速浏览。

## 患者模型

| 符号 | 描述 |
|------|------|
| `synthdiet.Patient` | 主对象,聚合人口学、人体测量、生物标志物、生活方式、诊断与用药。 |
| `synthdiet.Demographics` | 年龄、性别、国家等。 |
| `synthdiet.Anthropometrics` | 身高、体重、腰围。 |
| `synthdiet.Biomarkers` | 实验室指标(HbA1c、LDL、血压等)。 |
| `synthdiet.Lifestyle` | 体力活动、吸烟、饮酒等。 |

## 疾病

| 符号 | 描述 |
|------|------|
| `synthdiet.Disease` | 所有疾病的基类。 |
| `synthdiet.NutritionalConstraints` | 疾病特异性营养限制。 |
| `synthdiet.available_diseases()` | 列出已注册的所有疾病。 |
| `synthdiet.get_disease(name)` | 根据名称返回疾病类。 |

## 饮食方案

| 符号 | 描述 |
|------|------|
| `synthdiet.DietPlan` | 饮食方案的结构化表示。 |
| `synthdiet.mediterranean_diet()` | 地中海饮食。 |
| `synthdiet.dash_diet()` | DASH 饮食。 |
| `synthdiet.keto_diet()` | 生酮饮食。 |
| `synthdiet.low_fodmap_diet()` | 低 FODMAP 饮食。 |
| `synthdiet.low_sodium_renal_diet()` | 低钠肾脏饮食。 |
| `synthdiet.diabetic_diet()` | 糖尿病饮食。 |
| `synthdiet.vegan_diet()` | 纯素饮食。 |
| `synthdiet.standard_diet()` | 标准饮食(对照)。 |

## 生成器

| 符号 | 描述 |
|------|------|
| `synthdiet.RandomPatientGenerator` | 随机生成。 |
| `synthdiet.DistributionPatientGenerator` | 基于分布。 |
| `synthdiet.CopulaPatientGenerator` | 基于 Copula(变量相关)。 |
| `synthdiet.CohortGenerator` | 由配置生成患者列表。 |
| `synthdiet.CohortSpec` | 队列配置。 |
| `synthdiet.DiseaseSpec` | 疾病在队列中的分布。 |
| `synthdiet.MarkovProgressionGenerator` | 马尔可夫疾病进展。 |

## 模拟

| 符号 | 描述 |
|------|------|
| `synthdiet.DietSimulator` | 主模拟器(简单引擎 + Hall 2011)。 |
| `synthdiet.SimulationResult` | 包含生物标志物轨迹的结果。 |
| `synthdiet.HallSimulation` | Hall 2011 模型实现。 |
| `synthdiet.HallSimulationParameters` | 可调参数。 |

## 临床试验

| 符号 | 描述 |
|------|------|
| `synthdiet.trials.ParallelTrial` | 平行组 RCT。 |
| `synthdiet.trials.CrossoverTrial` | 交叉设计。 |
| `synthdiet.trials.FactorialTrial` | 2×2 析因。 |
| `synthdiet.trials.intention_to_treat` | ITT 分析。 |
| `synthdiet.trials.per_protocol` | 符合方案集分析。 |

## 饮食质量指数

| 符号 | 描述 |
|------|------|
| `synthdiet.indices.HEI2020` | Healthy Eating Index 2020。 |
| `synthdiet.indices.AHEI2010` | Alternate HEI 2010。 |
| `synthdiet.indices.MEDAS` | 地中海饮食依从性。 |
| `synthdiet.indices.DASHScore` | DASH 依从性。 |
| `synthdiet.indices.PHDI` | Planetary Health Diet Index。 |
| `synthdiet.indices.DII` | Dietary Inflammatory Index。 |

## 因果推断

| 符号 | 描述 |
|------|------|
| `synthdiet.causal.counterfactual_run` | 同一患者在两种饮食下的反事实模拟。 |
| `synthdiet.causal.ATEEstimator` | ATE 估计器。 |
| `synthdiet.causal.cate_by_subgroup` | 子组 CATE。 |
| `synthdiet.causal.ConfoundingExperiment` | 混杂 + IPTW + g-公式。 |
| `synthdiet.causal.DietDAG` | 轻量 DAG 工具。 |

## 教学

| 符号 | 描述 |
|------|------|
| `synthdiet.education.CaseStudy` | 单个临床案例。 |
| `synthdiet.education.OSCEStation` | OSCE 评分站。 |
| `synthdiet.education.built_in_cases()` | 内置 15 个案例。 |

## 统计与噪声

| 符号 | 描述 |
|------|------|
| `synthdiet.stats.sample_size_continuous` | 样本量(连续结局)。 |
| `synthdiet.stats.sample_size_binary` | 样本量(二分类结局)。 |
| `synthdiet.stats.bootstrap_ci` | Bootstrap 置信区间。 |
| `synthdiet.stats.permutation_test` | 置换检验。 |
| `synthdiet.stats.fdr_bh` | Benjamini-Hochberg FDR。 |
| `synthdiet.stats.ancova_baseline_adjusted` | 基线调整 ANCOVA。 |
| `synthdiet.noise.add_lab_measurement_error` | 给实验室指标加测量误差。 |
| `synthdiet.noise.inject_mcar_missing` | MCAR 缺失。 |
| `synthdiet.noise.inject_mar_missing` | MAR 缺失。 |
| `synthdiet.noise.inject_mnar_missing` | MNAR 缺失。 |
