# Referencia de la API

Esta página enumera la superficie pública de `synthdiet` con
descripciones en español. La documentación completa generada por
Sphinx está en inglés; este resumen está pensado para ojear con
rapidez.

## Modelo de paciente

| Símbolo | Descripción |
|---------|-------------|
| `synthdiet.Patient` | Objeto principal que agrega demografía, antropometría, biomarcadores, estilo de vida, diagnósticos y medicación. |
| `synthdiet.Demographics` | Edad, sexo, país y demás campos demográficos. |
| `synthdiet.Anthropometrics` | Talla, peso, perímetro de cintura. |
| `synthdiet.Biomarkers` | Valores de laboratorio (HbA1c, LDL, presión arterial, etc.). |
| `synthdiet.Lifestyle` | Actividad física, tabaco, alcohol, etc. |

## Enfermedades

| Símbolo | Descripción |
|---------|-------------|
| `synthdiet.Disease` | Clase base de todas las enfermedades. |
| `synthdiet.NutritionalConstraints` | Restricciones nutricionales específicas de la enfermedad. |
| `synthdiet.available_diseases()` | Lista todas las enfermedades registradas. |
| `synthdiet.get_disease(name)` | Devuelve la clase a partir del nombre. |

## Planes de dieta

| Símbolo | Descripción |
|---------|-------------|
| `synthdiet.DietPlan` | Representación estructurada de una dieta. |
| `synthdiet.mediterranean_diet()` | Dieta mediterránea predefinida. |
| `synthdiet.dash_diet()` | Dieta DASH. |
| `synthdiet.keto_diet()` | Dieta cetogénica. |
| `synthdiet.low_fodmap_diet()` | Dieta baja en FODMAP. |
| `synthdiet.low_sodium_renal_diet()` | Dieta renal baja en sodio. |
| `synthdiet.diabetic_diet()` | Dieta diabética. |
| `synthdiet.vegan_diet()` | Dieta vegana. |
| `synthdiet.standard_diet()` | Dieta estándar (control). |

## Generadores

| Símbolo | Descripción |
|---------|-------------|
| `synthdiet.RandomPatientGenerator` | Generador aleatorio. |
| `synthdiet.DistributionPatientGenerator` | A partir de distribuciones. |
| `synthdiet.CopulaPatientGenerator` | Basado en cópulas (rasgos correlacionados). |
| `synthdiet.CohortGenerator` | Genera una lista de pacientes desde una especificación. |
| `synthdiet.CohortSpec` | Configuración de cohorte. |
| `synthdiet.DiseaseSpec` | Distribución de una enfermedad en la cohorte. |
| `synthdiet.MarkovProgressionGenerator` | Progresión por cadenas de Markov. |

## Simulación

| Símbolo | Descripción |
|---------|-------------|
| `synthdiet.DietSimulator` | Simulador principal (motor simple + Hall 2011). |
| `synthdiet.SimulationResult` | Resultado con la trayectoria de los biomarcadores. |
| `synthdiet.HallSimulation` | Implementación del modelo de Hall 2011. |
| `synthdiet.HallSimulationParameters` | Parámetros ajustables. |

## Ensayos clínicos

| Símbolo | Descripción |
|---------|-------------|
| `synthdiet.trials.ParallelTrial` | ECA de brazos paralelos. |
| `synthdiet.trials.CrossoverTrial` | Diseño cruzado. |
| `synthdiet.trials.FactorialTrial` | Diseño factorial 2×2. |
| `synthdiet.trials.intention_to_treat` | Análisis ITT. |
| `synthdiet.trials.per_protocol` | Análisis por protocolo. |

## Índices de calidad de la dieta

| Símbolo | Descripción |
|---------|-------------|
| `synthdiet.indices.HEI2020` | Healthy Eating Index 2020. |
| `synthdiet.indices.AHEI2010` | Alternate HEI 2010. |
| `synthdiet.indices.MEDAS` | Adherencia a la dieta mediterránea. |
| `synthdiet.indices.DASHScore` | Adherencia a DASH. |
| `synthdiet.indices.PHDI` | Planetary Health Diet Index. |
| `synthdiet.indices.DII` | Dietary Inflammatory Index. |

## Inferencia causal

| Símbolo | Descripción |
|---------|-------------|
| `synthdiet.causal.counterfactual_run` | Simulación contrafactual del mismo paciente bajo dos dietas. |
| `synthdiet.causal.ATEEstimator` | Estimador del efecto medio del tratamiento. |
| `synthdiet.causal.cate_by_subgroup` | ATE condicionada (CATE) por subgrupos. |
| `synthdiet.causal.ConfoundingExperiment` | Confusión + ajuste por IPTW y g-fórmula. |
| `synthdiet.causal.DietDAG` | Utilidad ligera de DAG. |

## Educación

| Símbolo | Descripción |
|---------|-------------|
| `synthdiet.education.CaseStudy` | Caso clínico individual. |
| `synthdiet.education.OSCEStation` | Estación de evaluación tipo OSCE. |
| `synthdiet.education.built_in_cases()` | Los 15 casos integrados. |

## Estadística y ruido

| Símbolo | Descripción |
|---------|-------------|
| `synthdiet.stats.sample_size_continuous` | Tamaño muestral, resultado continuo. |
| `synthdiet.stats.sample_size_binary` | Tamaño muestral, resultado binario. |
| `synthdiet.stats.bootstrap_ci` | Intervalo de confianza bootstrap. |
| `synthdiet.stats.permutation_test` | Test de permutación. |
| `synthdiet.stats.fdr_bh` | FDR de Benjamini-Hochberg. |
| `synthdiet.stats.ancova_baseline_adjusted` | ANCOVA ajustada por línea base. |
| `synthdiet.noise.add_lab_measurement_error` | Error de medida en valores de laboratorio. |
| `synthdiet.noise.inject_mcar_missing` | Datos faltantes MCAR. |
| `synthdiet.noise.inject_mar_missing` | Datos faltantes MAR. |
| `synthdiet.noise.inject_mnar_missing` | Datos faltantes MNAR. |
