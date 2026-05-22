# Usare `synthdiet` da R con `reticulate`

Molti ricercatori in nutrizione lavorano principalmente in R.
`synthdiet` non ha un pacchetto R dedicato, ma funziona senza
problemi tramite `reticulate`.

## Configurazione iniziale

```r
install.packages("reticulate")
library(reticulate)

virtualenv_create("synthdiet-env")
virtualenv_install("synthdiet-env", packages = c("synthdiet"))
use_virtualenv("synthdiet-env", required = TRUE)
```

## Generare una coorte

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

> In R aggiungere `L` agli interi; altrimenti arrivano in Python come
> `float` e falliscono dove ci si aspetta `int`.

## Eseguire un RCT parallelo

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

## Riportare il risultato in R

```r
df <- py_to_r(result$outcomes)
head(df)

library(dplyr)
df %>%
  group_by(arm) %>%
  summarise(media_delta = mean(delta_hba1c_pct))
```

## Grafici in R

```r
library(ggplot2)

ggplot(df, aes(x = arm, y = delta_hba1c_pct, colour = arm)) +
  geom_boxplot() +
  labs(
    x = "Braccio",
    y = "Variazione HbA1c (pp)",
    title = "Studio sintetico di 12 settimane"
  )
```

## Suggerimenti

- Per coorti grandi (>10 000) aggregate in Python e portate solo il
  riepilogo in R.
- Per riproducibilità fissate la versione:
  `virtualenv_install(..., packages = c("synthdiet==0.1.0"))`.
