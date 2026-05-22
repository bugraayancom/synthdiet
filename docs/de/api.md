# API-Referenz

Diese Seite listet die öffentliche API von `synthdiet` mit deutschen
Kurzbeschreibungen. Die vollständige, von Sphinx generierte
Dokumentation ist auf Englisch; diese Tabellen dienen dem schnellen
Überblick.

## Patientenmodell

| Symbol | Beschreibung |
|--------|--------------|
| `synthdiet.Patient` | Hauptobjekt mit Demografie, Anthropometrie, Biomarkern, Lebensstil, Diagnosen und Medikation. |
| `synthdiet.Demographics` | Alter, Geschlecht, Land usw. |
| `synthdiet.Anthropometrics` | Größe, Gewicht, Taillenumfang. |
| `synthdiet.Biomarkers` | Laborwerte (HbA1c, LDL, Blutdruck …). |
| `synthdiet.Lifestyle` | Bewegung, Rauchen, Alkohol. |

## Krankheiten

| Symbol | Beschreibung |
|--------|--------------|
| `synthdiet.Disease` | Basisklasse für alle Krankheiten. |
| `synthdiet.NutritionalConstraints` | Krankheitsspezifische Ernährungsrestriktionen. |
| `synthdiet.available_diseases()` | Listet alle registrierten Krankheiten. |
| `synthdiet.get_disease(name)` | Liefert die Klasse anhand des Namens. |

## Diätpläne

| Symbol | Beschreibung |
|--------|--------------|
| `synthdiet.DietPlan` | Strukturierte Repräsentation eines Diätplans. |
| `synthdiet.mediterranean_diet()` | Mediterrane Diät. |
| `synthdiet.dash_diet()` | DASH-Diät. |
| `synthdiet.keto_diet()` | Ketogene Diät. |
| `synthdiet.low_fodmap_diet()` | Low-FODMAP-Diät. |
| `synthdiet.low_sodium_renal_diet()` | Natriumarme renale Diät. |
| `synthdiet.diabetic_diet()` | Diabetiker-Diät. |
| `synthdiet.vegan_diet()` | Vegane Diät. |
| `synthdiet.standard_diet()` | Standard-Referenzdiät. |

## Generatoren

| Symbol | Beschreibung |
|--------|--------------|
| `synthdiet.RandomPatientGenerator` | Zufallsgenerator. |
| `synthdiet.DistributionPatientGenerator` | Verteilungsbasiert. |
| `synthdiet.CopulaPatientGenerator` | Copula-basiert (korrelierte Merkmale). |
| `synthdiet.CohortGenerator` | Erzeugt eine Liste aus einer Spezifikation. |
| `synthdiet.CohortSpec` | Kohortenkonfiguration. |
| `synthdiet.DiseaseSpec` | Verteilung einer Krankheit in der Kohorte. |
| `synthdiet.MarkovProgressionGenerator` | Markow-basierte Krankheitsprogression. |

## Simulation

| Symbol | Beschreibung |
|--------|--------------|
| `synthdiet.DietSimulator` | Hauptsimulator (einfach + Hall 2011). |
| `synthdiet.SimulationResult` | Ergebnis mit Biomarker-Trajektorie. |
| `synthdiet.HallSimulation` | Implementierung des Hall-2011-Modells. |
| `synthdiet.HallSimulationParameters` | Einstellbare Parameter. |

## Studien

| Symbol | Beschreibung |
|--------|--------------|
| `synthdiet.trials.ParallelTrial` | Parallel-RCT. |
| `synthdiet.trials.CrossoverTrial` | Crossover-Design. |
| `synthdiet.trials.FactorialTrial` | 2×2-faktoriell. |
| `synthdiet.trials.intention_to_treat` | ITT-Analyse. |
| `synthdiet.trials.per_protocol` | Per-Protocol-Analyse. |

## Diätqualitäts-Indizes

| Symbol | Beschreibung |
|--------|--------------|
| `synthdiet.indices.HEI2020` | Healthy Eating Index 2020. |
| `synthdiet.indices.AHEI2010` | Alternate HEI 2010. |
| `synthdiet.indices.MEDAS` | Mediterrane-Adhärenz-Skala. |
| `synthdiet.indices.DASHScore` | DASH-Adhärenz. |
| `synthdiet.indices.PHDI` | Planetary Health Diet Index. |
| `synthdiet.indices.DII` | Dietary Inflammatory Index. |

## Kausale Inferenz

| Symbol | Beschreibung |
|--------|--------------|
| `synthdiet.causal.counterfactual_run` | Kontrafaktische Simulation einer Person unter zwei Diäten. |
| `synthdiet.causal.ATEEstimator` | ATE-Schätzer. |
| `synthdiet.causal.cate_by_subgroup` | Subgruppen-CATE. |
| `synthdiet.causal.ConfoundingExperiment` | Konfundierung + IPTW + g-Formel. |
| `synthdiet.causal.DietDAG` | Leichtgewichtige DAG-Hilfsklasse. |

## Lehre

| Symbol | Beschreibung |
|--------|--------------|
| `synthdiet.education.CaseStudy` | Eine klinische Fallstudie. |
| `synthdiet.education.OSCEStation` | OSCE-Bewertungsstation. |
| `synthdiet.education.built_in_cases()` | Die 15 eingebauten Fälle. |

## Statistik & Rauschen

| Symbol | Beschreibung |
|--------|--------------|
| `synthdiet.stats.sample_size_continuous` | Stichprobengröße, stetiger Endpunkt. |
| `synthdiet.stats.sample_size_binary` | Stichprobengröße, binärer Endpunkt. |
| `synthdiet.stats.bootstrap_ci` | Bootstrap-Konfidenzintervall. |
| `synthdiet.stats.permutation_test` | Permutationstest. |
| `synthdiet.stats.fdr_bh` | Benjamini-Hochberg-FDR. |
| `synthdiet.stats.ancova_baseline_adjusted` | Baseline-adjustierte ANCOVA. |
| `synthdiet.noise.add_lab_measurement_error` | Messfehler auf Laborwerten. |
| `synthdiet.noise.inject_mcar_missing` | MCAR-Fehlwerte. |
| `synthdiet.noise.inject_mar_missing` | MAR-Fehlwerte. |
| `synthdiet.noise.inject_mnar_missing` | MNAR-Fehlwerte. |
