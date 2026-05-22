# `reticulate` を介して R から `synthdiet` を使う

栄養研究者の多くは主に R で作業します。`synthdiet` には専用の
R パッケージはありませんが、`reticulate` を介してスムーズに
利用できます。

## 一度きりのセットアップ

```r
install.packages("reticulate")
library(reticulate)

virtualenv_create("synthdiet-env")
virtualenv_install("synthdiet-env", packages = c("synthdiet"))
use_virtualenv("synthdiet-env", required = TRUE)
```

## コホートの生成

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

> R では整数の末尾に `L` を付けてください。さもないと Python 側に
> `float` として渡り、`int` を期待する箇所で失敗します。

## 並行 RCT の実行

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

## 結果を R に戻す

```r
df <- py_to_r(result$outcomes)
head(df)

library(dplyr)
df %>%
  group_by(arm) %>%
  summarise(mean_delta = mean(delta_hba1c_pct))
```

## R での描画

```r
library(ggplot2)

ggplot(df, aes(x = arm, y = delta_hba1c_pct, colour = arm)) +
  geom_boxplot() +
  labs(
    x = "群",
    y = "HbA1c 変化 (pp)",
    title = "12 週間の合成試験"
  )
```

## ヒント

- 大きなコホート(>10,000 例)では Python 側で集計して、要約
  テーブルだけを R に戻すと高速です。
- 再現性のためにバージョンを固定:
  `virtualenv_install(..., packages = c("synthdiet==0.1.0"))`。
