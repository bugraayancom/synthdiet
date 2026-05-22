# Riferimento API

Questa pagina elenca l'API pubblica di `synthdiet` con descrizioni in
italiano. La documentazione completa generata da Sphinx è in inglese;
questo riepilogo serve per una consultazione rapida.

## Modello del paziente

| Simbolo | Descrizione |
|---------|-------------|
| `synthdiet.Patient` | Oggetto principale con demografia, antropometria, biomarcatori, stile di vita, diagnosi e farmaci. |
| `synthdiet.Demographics` | Età, sesso, paese ecc. |
| `synthdiet.Anthropometrics` | Statura, peso, circonferenza vita. |
| `synthdiet.Biomarkers` | Valori di laboratorio (HbA1c, LDL, PA…). |
| `synthdiet.Lifestyle` | Attività fisica, fumo, alcol. |

## Patologie

| Simbolo | Descrizione |
|---------|-------------|
| `synthdiet.Disease` | Classe base. |
| `synthdiet.NutritionalConstraints` | Vincoli nutrizionali specifici della patologia. |
| `synthdiet.available_diseases()` | Tutte le patologie registrate. |
| `synthdiet.get_disease(name)` | Restituisce la classe dato il nome. |

## Piani dietetici

| Simbolo | Descrizione |
|---------|-------------|
| `synthdiet.DietPlan` | Rappresentazione strutturata. |
| `synthdiet.mediterranean_diet()` | Dieta mediterranea. |
| `synthdiet.dash_diet()` | DASH. |
| `synthdiet.keto_diet()` | Chetogenica. |
| `synthdiet.low_fodmap_diet()` | Low-FODMAP. |
| `synthdiet.low_sodium_renal_diet()` | Renale iposodica. |
| `synthdiet.diabetic_diet()` | Diabetica. |
| `synthdiet.vegan_diet()` | Vegana. |
| `synthdiet.standard_diet()` | Standard (controllo). |

## Generatori

| Simbolo | Descrizione |
|---------|-------------|
| `synthdiet.RandomPatientGenerator` | Generazione casuale. |
| `synthdiet.DistributionPatientGenerator` | Da distribuzioni. |
| `synthdiet.CopulaPatientGenerator` | Tramite copule (variabili correlate). |
| `synthdiet.CohortGenerator` | Genera una lista da una specifica. |
| `synthdiet.CohortSpec` | Configurazione della coorte. |
| `synthdiet.DiseaseSpec` | Distribuzione di una patologia nella coorte. |
| `synthdiet.MarkovProgressionGenerator` | Progressione di Markov. |

## Simulazione

| Simbolo | Descrizione |
|---------|-------------|
| `synthdiet.DietSimulator` | Simulatore principale (semplice + Hall 2011). |
| `synthdiet.SimulationResult` | Risultato con la traiettoria dei biomarcatori. |
| `synthdiet.HallSimulation` | Implementazione del modello di Hall 2011. |
| `synthdiet.HallSimulationParameters` | Parametri regolabili. |

## Studi clinici

| Simbolo | Descrizione |
|---------|-------------|
| `synthdiet.trials.ParallelTrial` | RCT a bracci paralleli. |
| `synthdiet.trials.CrossoverTrial` | Crossover. |
| `synthdiet.trials.FactorialTrial` | Fattoriale 2×2. |
| `synthdiet.trials.intention_to_treat` | Analisi ITT. |
| `synthdiet.trials.per_protocol` | Per-protocol. |

## Indici di qualità della dieta

| Simbolo | Descrizione |
|---------|-------------|
| `synthdiet.indices.HEI2020` | Healthy Eating Index 2020. |
| `synthdiet.indices.AHEI2010` | Alternate HEI 2010. |
| `synthdiet.indices.MEDAS` | Aderenza alla dieta mediterranea. |
| `synthdiet.indices.DASHScore` | Aderenza a DASH. |
| `synthdiet.indices.PHDI` | Planetary Health Diet Index. |
| `synthdiet.indices.DII` | Dietary Inflammatory Index. |

## Inferenza causale

| Simbolo | Descrizione |
|---------|-------------|
| `synthdiet.causal.counterfactual_run` | Simulazione controfattuale dello stesso paziente sotto due diete. |
| `synthdiet.causal.ATEEstimator` | Stimatore dell'ATE. |
| `synthdiet.causal.cate_by_subgroup` | CATE per sottogruppi. |
| `synthdiet.causal.ConfoundingExperiment` | Confondimento + IPTW + g-formula. |
| `synthdiet.causal.DietDAG` | Utility leggera per DAG. |

## Didattica

| Simbolo | Descrizione |
|---------|-------------|
| `synthdiet.education.CaseStudy` | Caso clinico. |
| `synthdiet.education.OSCEStation` | Stazione OSCE. |
| `synthdiet.education.built_in_cases()` | I 15 casi inclusi. |

## Statistica e rumore

| Simbolo | Descrizione |
|---------|-------------|
| `synthdiet.stats.sample_size_continuous` | Numerosità campionaria, esito continuo. |
| `synthdiet.stats.sample_size_binary` | Numerosità campionaria, esito binario. |
| `synthdiet.stats.bootstrap_ci` | IC bootstrap. |
| `synthdiet.stats.permutation_test` | Test di permutazione. |
| `synthdiet.stats.fdr_bh` | FDR Benjamini-Hochberg. |
| `synthdiet.stats.ancova_baseline_adjusted` | ANCOVA aggiustata per valore basale. |
| `synthdiet.noise.add_lab_measurement_error` | Errore di misura sui valori di laboratorio. |
| `synthdiet.noise.inject_mcar_missing` | Mancanti MCAR. |
| `synthdiet.noise.inject_mar_missing` | Mancanti MAR. |
| `synthdiet.noise.inject_mnar_missing` | Mancanti MNAR. |
