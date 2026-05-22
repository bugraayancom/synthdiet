# API reference

## Patient model

```{eval-rst}
.. autosummary::
   :toctree: _autosummary

   synthdiet.Patient
   synthdiet.Demographics
   synthdiet.Anthropometrics
   synthdiet.Biomarkers
   synthdiet.Lifestyle
```

## Diseases

```{eval-rst}
.. autosummary::
   :toctree: _autosummary

   synthdiet.Disease
   synthdiet.NutritionalConstraints
   synthdiet.available_diseases
   synthdiet.get_disease
```

## Diet plans

```{eval-rst}
.. autosummary::
   :toctree: _autosummary

   synthdiet.DietPlan
   synthdiet.mediterranean_diet
   synthdiet.dash_diet
   synthdiet.keto_diet
   synthdiet.low_fodmap_diet
   synthdiet.low_sodium_renal_diet
   synthdiet.diabetic_diet
   synthdiet.vegan_diet
   synthdiet.standard_diet
```

## Generators

```{eval-rst}
.. autosummary::
   :toctree: _autosummary

   synthdiet.RandomPatientGenerator
   synthdiet.DistributionPatientGenerator
   synthdiet.CopulaPatientGenerator
   synthdiet.CohortGenerator
   synthdiet.CohortSpec
   synthdiet.DiseaseSpec
   synthdiet.MarkovProgressionGenerator
```

## Simulation

```{eval-rst}
.. autosummary::
   :toctree: _autosummary

   synthdiet.DietSimulator
   synthdiet.SimulationResult
   synthdiet.HallSimulation
   synthdiet.HallSimulationParameters
```

## Trials

```{eval-rst}
.. autosummary::
   :toctree: _autosummary

   synthdiet.trials.ParallelTrial
   synthdiet.trials.CrossoverTrial
   synthdiet.trials.FactorialTrial
   synthdiet.trials.intention_to_treat
   synthdiet.trials.per_protocol
```

## Diet quality indices

```{eval-rst}
.. autosummary::
   :toctree: _autosummary

   synthdiet.indices.HEI2020
   synthdiet.indices.AHEI2010
   synthdiet.indices.MEDAS
   synthdiet.indices.DASHScore
   synthdiet.indices.PHDI
   synthdiet.indices.DII
```

## Causal inference

```{eval-rst}
.. autosummary::
   :toctree: _autosummary

   synthdiet.causal.counterfactual_run
   synthdiet.causal.ATEEstimator
   synthdiet.causal.cate_by_subgroup
   synthdiet.causal.ConfoundingExperiment
   synthdiet.causal.DietDAG
```

## Education

```{eval-rst}
.. autosummary::
   :toctree: _autosummary

   synthdiet.education.CaseStudy
   synthdiet.education.OSCEStation
   synthdiet.education.built_in_cases
```

## Statistics & noise

```{eval-rst}
.. autosummary::
   :toctree: _autosummary

   synthdiet.stats.sample_size_continuous
   synthdiet.stats.sample_size_binary
   synthdiet.stats.bootstrap_ci
   synthdiet.stats.permutation_test
   synthdiet.stats.fdr_bh
   synthdiet.stats.ancova_baseline_adjusted
   synthdiet.noise.add_lab_measurement_error
   synthdiet.noise.inject_mcar_missing
   synthdiet.noise.inject_mar_missing
   synthdiet.noise.inject_mnar_missing
```
