# Using synthdiet from R via reticulate

Many nutrition researchers work primarily in R. synthdiet has no dedicated R
binding, but it works smoothly through `reticulate`.

## One-time setup

```r
install.packages("reticulate")
library(reticulate)

# Create a local Python virtual environment with synthdiet installed.
virtualenv_create("synthdiet-env")
virtualenv_install("synthdiet-env", packages = c("synthdiet"))
use_virtualenv("synthdiet-env", required = TRUE)
```

## Generate a cohort

```r
synthdiet <- import("synthdiet")

spec <- synthdiet$CohortSpec(
  size = 100L,
  diseases = list(
    synthdiet$DiseaseSpec("type_2_diabetes", prevalence = 0.4),
    synthdiet$DiseaseSpec("hypertension", prevalence = 0.4)
  )
)
cohort <- synthdiet$CohortGenerator(spec, seed = 42L)$generate()
```

## Run a parallel trial

```r
trial <- synthdiet$trials$ParallelTrial(
  cohort = cohort,
  arms = list(
    "control" = synthdiet$standard_diet(),
    "intervention" = synthdiet$mediterranean_diet()
  ),
  duration_weeks = 12L,
  primary_outcome = "hba1c_pct"
)
result <- trial$run(seed = 1L)
itt <- result$intention_to_treat()
cat("ATE:", itt$diff, "(95% CI", itt$ci_95[1], ",", itt$ci_95[2], ")\n")
```

## Bring the result back to R

```r
df <- py_to_r(result$outcomes)
head(df)

# Now you can use base R, dplyr, lme4, etc.
library(dplyr)
df %>% group_by(arm) %>% summarise(mean_delta = mean(delta_hba1c_pct))
```

## Plotting in R

```r
library(ggplot2)
ggplot(df, aes(x = arm, y = delta_hba1c_pct, colour = arm)) +
  geom_boxplot() +
  labs(y = "Change in HbA1c (pp)", title = "Synthetic 12-week trial")
```
