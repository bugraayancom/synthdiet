# `synthdiet` aus R via `reticulate` nutzen

Viele Ernährungsforschende arbeiten primär in R. `synthdiet` hat
kein dediziertes R-Paket, lässt sich aber problemlos über
`reticulate` ansprechen.

## Einmalige Einrichtung

```r
install.packages("reticulate")
library(reticulate)

virtualenv_create("synthdiet-env")
virtualenv_install("synthdiet-env", packages = c("synthdiet"))
use_virtualenv("synthdiet-env", required = TRUE)
```

## Kohorte erzeugen

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

> Hängen Sie in R `L` an Ganzzahlen an; sonst kommen sie als `float`
> in Python an und schlagen dort fehl, wo `int` erwartet wird.

## Parallel-RCT durchführen

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
    "(95% KI", itt$ci_95[1], ",", itt$ci_95[2], ")\n")
```

## Ergebnis nach R zurückholen

```r
df <- py_to_r(result$outcomes)
head(df)

library(dplyr)
df %>%
  group_by(arm) %>%
  summarise(mittel_delta = mean(delta_hba1c_pct))
```

## Plotten in R

```r
library(ggplot2)

ggplot(df, aes(x = arm, y = delta_hba1c_pct, colour = arm)) +
  geom_boxplot() +
  labs(
    x = "Arm",
    y = "HbA1c-Änderung (pp)",
    title = "Synthetische 12-Wochen-Studie"
  )
```

## Tipps

- Bei großen Kohorten (>10 000) aggregieren Sie in Python und
  übergeben nur die Zusammenfassung an R.
- Für Reproduzierbarkeit Version fixieren:
  `virtualenv_install(..., packages = c("synthdiet==0.1.0"))`.
