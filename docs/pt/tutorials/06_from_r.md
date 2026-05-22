# Usar `synthdiet` a partir do R com `reticulate`

Muitos pesquisadores em nutrição trabalham principalmente em R.
`synthdiet` não tem pacote R dedicado, mas funciona perfeitamente
via `reticulate`.

## Configuração inicial

```r
install.packages("reticulate")
library(reticulate)

virtualenv_create("synthdiet-env")
virtualenv_install("synthdiet-env", packages = c("synthdiet"))
use_virtualenv("synthdiet-env", required = TRUE)
```

## Gerar uma coorte

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

> No R adicione `L` aos inteiros; caso contrário chegam ao Python
> como `float` e falham onde se espera `int`.

## Executar um ECR paralelo

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
    "(IC 95%", itt$ci_95[1], ",", itt$ci_95[2], ")\n")
```

## Trazer o resultado de volta ao R

```r
df <- py_to_r(result$outcomes)
head(df)

library(dplyr)
df %>%
  group_by(arm) %>%
  summarise(media_delta = mean(delta_hba1c_pct))
```

## Gráficos em R

```r
library(ggplot2)

ggplot(df, aes(x = arm, y = delta_hba1c_pct, colour = arm)) +
  geom_boxplot() +
  labs(
    x = "Braço",
    y = "Variação de HbA1c (pp)",
    title = "Ensaio sintético de 12 semanas"
  )
```

## Dicas

- Para coortes grandes (>10 000) agregue em Python e leve só o resumo
  para o R.
- Para reprodutibilidade fixe a versão:
  `virtualenv_install(..., packages = c("synthdiet==0.1.0"))`.
