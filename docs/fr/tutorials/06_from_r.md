# Utiliser `synthdiet` depuis R via `reticulate`

De nombreux chercheurs en nutrition travaillent principalement sous R.
`synthdiet` n'a pas de paquet R dédié, mais s'utilise sans difficulté
via `reticulate`.

## Configuration initiale

```r
install.packages("reticulate")
library(reticulate)

virtualenv_create("synthdiet-env")
virtualenv_install("synthdiet-env", packages = c("synthdiet"))
use_virtualenv("synthdiet-env", required = TRUE)
```

## Générer une cohorte

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

> Sous R, ajoutez le suffixe `L` aux entiers ; sinon ils arrivent en
> Python comme `float` et échouent là où un `int` est attendu.

## Lancer un ECR à bras parallèles

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
cat("ATE :", itt$diff,
    "(IC 95 %", itt$ci_95[1], ",", itt$ci_95[2], ")\n")
```

## Ramener le résultat dans R

```r
df <- py_to_r(result$outcomes)
head(df)

library(dplyr)
df %>%
  group_by(arm) %>%
  summarise(moyenne_delta = mean(delta_hba1c_pct))
```

## Graphiques sous R

```r
library(ggplot2)

ggplot(df, aes(x = arm, y = delta_hba1c_pct, colour = arm)) +
  geom_boxplot() +
  labs(
    x = "Bras",
    y = "Variation HbA1c (pp)",
    title = "Essai synthétique de 12 semaines"
  )
```

## Conseils

- Pour les grandes cohortes (>10 000 patients), agrégez en Python et
  ne ramenez que la table résumée dans R.
- Pour la reproductibilité, fixez la version :
  `virtualenv_install(..., packages = c("synthdiet==0.1.0"))`.
