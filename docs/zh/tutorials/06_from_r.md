# 通过 `reticulate` 在 R 中使用 `synthdiet`

许多营养研究人员主要使用 R。`synthdiet` 没有专门的 R 包,但通过
`reticulate` 可以无缝调用。

## 一次性配置

```r
install.packages("reticulate")
library(reticulate)

virtualenv_create("synthdiet-env")
virtualenv_install("synthdiet-env", packages = c("synthdiet"))
use_virtualenv("synthdiet-env", required = TRUE)
```

## 生成队列

```r
synthdiet <- import("synthdiet")

spec <- synthdiet$CohortSpec(
  size = 100L,
  diseases = list(
    synthdiet$DiseaseSpec("type_2_diabetes", prevalence = 0.4),
    synthdiet$DiseaseSpec("hypertension",     prevalence = 0.4)
  )
)
cohort <- synthdiet$CohortGenerator(spec, seed = 42L)$generate()
```

> 在 R 中请在整数后加 `L`,否则会被传成 `float`,在期望 `int` 的
> 位置会报错。

## 运行平行 RCT

```r
trial <- synthdiet$trials$ParallelTrial(
  cohort = cohort,
  arms = list(
    "control"      = synthdiet$standard_diet(),
    "intervention" = synthdiet$mediterranean_diet()
  ),
  duration_weeks  = 12L,
  primary_outcome = "hba1c_pct"
)
result <- trial$run(seed = 1L)
itt <- result$intention_to_treat()
cat("ATE:", itt$diff,
    "(95% CI", itt$ci_95[1], ",", itt$ci_95[2], ")\n")
```

## 把结果带回 R

```r
df <- py_to_r(result$outcomes)
head(df)

library(dplyr)
df %>%
  group_by(arm) %>%
  summarise(mean_delta = mean(delta_hba1c_pct))
```

## R 中绘图

```r
library(ggplot2)

ggplot(df, aes(x = arm, y = delta_hba1c_pct, colour = arm)) +
  geom_boxplot() +
  labs(
    x = "组别",
    y = "HbA1c 变化(pp)",
    title = "12 周合成临床试验"
  )
```

## 提示

- 大队列(>10 000)请在 Python 端先做汇总,再把摘要传回 R。
- 为了可重复性,请固定版本:
  `virtualenv_install(..., packages = c("synthdiet==0.1.0"))`。
