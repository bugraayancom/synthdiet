# Usar `synthdiet` desde R con `reticulate`

Muchos investigadores en nutrición trabajan principalmente en R.
`synthdiet` no tiene un paquete R dedicado, pero funciona sin
problema a través de `reticulate`.

## Configuración inicial

```r
install.packages("reticulate")
library(reticulate)

virtualenv_create("synthdiet-env")
virtualenv_install("synthdiet-env", packages = c("synthdiet"))
use_virtualenv("synthdiet-env", required = TRUE)
```

## Generar una cohorte

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

> En R añada el sufijo `L` a los enteros; en caso contrario llegan a
> Python como `float` y fallan donde se esperan `int`.

## Ejecutar un ECA paralelo

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

## Llevar el resultado de vuelta a R

```r
df <- py_to_r(result$outcomes)
head(df)

library(dplyr)
df %>%
  group_by(arm) %>%
  summarise(media_delta = mean(delta_hba1c_pct))
```

## Gráficos en R

```r
library(ggplot2)

ggplot(df, aes(x = arm, y = delta_hba1c_pct, colour = arm)) +
  geom_boxplot() +
  labs(
    x = "Brazo",
    y = "Cambio en HbA1c (pp)",
    title = "Ensayo sintético de 12 semanas"
  )
```

## Consejos

- Para cohortes grandes (>10 000) calcule el resumen en Python y
  pase solo la tabla agregada a R.
- Para reproducibilidad fije la versión:
  `virtualenv_install(..., packages = c("synthdiet==0.1.0"))`.
