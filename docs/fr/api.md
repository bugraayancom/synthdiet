# Référence de l'API

Cette page liste l'API publique de `synthdiet` avec des descriptions
en français. La documentation complète générée par Sphinx est en
anglais ; ce résumé sert d'aperçu rapide.

## Modèle patient

| Symbole | Description |
|---------|-------------|
| `synthdiet.Patient` | Objet principal regroupant démographie, anthropométrie, biomarqueurs, mode de vie, diagnostics et médicaments. |
| `synthdiet.Demographics` | Âge, sexe, pays, etc. |
| `synthdiet.Anthropometrics` | Taille, poids, tour de taille. |
| `synthdiet.Biomarkers` | Valeurs biologiques (HbA1c, LDL, pression artérielle…). |
| `synthdiet.Lifestyle` | Activité physique, tabac, alcool. |

## Maladies

| Symbole | Description |
|---------|-------------|
| `synthdiet.Disease` | Classe de base. |
| `synthdiet.NutritionalConstraints` | Contraintes nutritionnelles spécifiques à la maladie. |
| `synthdiet.available_diseases()` | Liste toutes les maladies enregistrées. |
| `synthdiet.get_disease(name)` | Renvoie la classe à partir du nom. |

## Plans diététiques

| Symbole | Description |
|---------|-------------|
| `synthdiet.DietPlan` | Représentation structurée d'un régime. |
| `synthdiet.mediterranean_diet()` | Régime méditerranéen. |
| `synthdiet.dash_diet()` | Régime DASH. |
| `synthdiet.keto_diet()` | Régime cétogène. |
| `synthdiet.low_fodmap_diet()` | Régime pauvre en FODMAP. |
| `synthdiet.low_sodium_renal_diet()` | Régime rénal pauvre en sodium. |
| `synthdiet.diabetic_diet()` | Régime diabétique. |
| `synthdiet.vegan_diet()` | Régime vegan. |
| `synthdiet.standard_diet()` | Régime standard (témoin). |

## Générateurs

| Symbole | Description |
|---------|-------------|
| `synthdiet.RandomPatientGenerator` | Génération aléatoire. |
| `synthdiet.DistributionPatientGenerator` | À partir de distributions. |
| `synthdiet.CopulaPatientGenerator` | Par copule (variables corrélées). |
| `synthdiet.CohortGenerator` | Génère une liste à partir d'une spécification. |
| `synthdiet.CohortSpec` | Configuration de cohorte. |
| `synthdiet.DiseaseSpec` | Distribution d'une maladie dans la cohorte. |
| `synthdiet.MarkovProgressionGenerator` | Progression markovienne. |

## Simulation

| Symbole | Description |
|---------|-------------|
| `synthdiet.DietSimulator` | Simulateur principal (moteur simple + Hall 2011). |
| `synthdiet.SimulationResult` | Résultat avec trajectoire des biomarqueurs. |
| `synthdiet.HallSimulation` | Implémentation du modèle de Hall 2011. |
| `synthdiet.HallSimulationParameters` | Paramètres réglables. |

## Essais cliniques

| Symbole | Description |
|---------|-------------|
| `synthdiet.trials.ParallelTrial` | ECR à bras parallèles. |
| `synthdiet.trials.CrossoverTrial` | Essai croisé. |
| `synthdiet.trials.FactorialTrial` | Plan factoriel 2×2. |
| `synthdiet.trials.intention_to_treat` | Analyse en ITT. |
| `synthdiet.trials.per_protocol` | Analyse en per-protocol. |

## Indices de qualité alimentaire

| Symbole | Description |
|---------|-------------|
| `synthdiet.indices.HEI2020` | Healthy Eating Index 2020. |
| `synthdiet.indices.AHEI2010` | Alternate HEI 2010. |
| `synthdiet.indices.MEDAS` | Adhésion au régime méditerranéen. |
| `synthdiet.indices.DASHScore` | Adhésion à DASH. |
| `synthdiet.indices.PHDI` | Planetary Health Diet Index. |
| `synthdiet.indices.DII` | Dietary Inflammatory Index. |

## Inférence causale

| Symbole | Description |
|---------|-------------|
| `synthdiet.causal.counterfactual_run` | Simulation contrefactuelle d'un même patient sous deux régimes. |
| `synthdiet.causal.ATEEstimator` | Effet moyen du traitement (ATE). |
| `synthdiet.causal.cate_by_subgroup` | CATE par sous-groupes. |
| `synthdiet.causal.ConfoundingExperiment` | Confusion + ajustement IPTW et g-formule. |
| `synthdiet.causal.DietDAG` | Utilitaire DAG léger. |

## Éducation

| Symbole | Description |
|---------|-------------|
| `synthdiet.education.CaseStudy` | Un cas clinique. |
| `synthdiet.education.OSCEStation` | Station de notation type ECOS. |
| `synthdiet.education.built_in_cases()` | Les 15 cas intégrés. |

## Statistiques et bruit

| Symbole | Description |
|---------|-------------|
| `synthdiet.stats.sample_size_continuous` | Taille d'échantillon, résultat continu. |
| `synthdiet.stats.sample_size_binary` | Taille d'échantillon, résultat binaire. |
| `synthdiet.stats.bootstrap_ci` | IC bootstrap. |
| `synthdiet.stats.permutation_test` | Test de permutation. |
| `synthdiet.stats.fdr_bh` | FDR Benjamini-Hochberg. |
| `synthdiet.stats.ancova_baseline_adjusted` | ANCOVA ajustée sur valeur initiale. |
| `synthdiet.noise.add_lab_measurement_error` | Erreur de mesure sur valeurs biologiques. |
| `synthdiet.noise.inject_mcar_missing` | Données manquantes MCAR. |
| `synthdiet.noise.inject_mar_missing` | Données manquantes MAR. |
| `synthdiet.noise.inject_mnar_missing` | Données manquantes MNAR. |
