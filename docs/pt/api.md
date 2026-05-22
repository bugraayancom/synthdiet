# Referência da API

Esta página lista a API pública de `synthdiet` com descrições em
português. A documentação completa gerada pelo Sphinx está em inglês;
este resumo serve para consulta rápida.

## Modelo de paciente

| Símbolo | Descrição |
|---------|-----------|
| `synthdiet.Patient` | Objeto principal com demografia, antropometria, biomarcadores, estilo de vida, diagnósticos e medicações. |
| `synthdiet.Demographics` | Idade, sexo, país, etc. |
| `synthdiet.Anthropometrics` | Estatura, peso, circunferência da cintura. |
| `synthdiet.Biomarkers` | Valores laboratoriais (HbA1c, LDL, PA…). |
| `synthdiet.Lifestyle` | Atividade física, tabagismo, álcool. |

## Doenças

| Símbolo | Descrição |
|---------|-----------|
| `synthdiet.Disease` | Classe base. |
| `synthdiet.NutritionalConstraints` | Restrições específicas da doença. |
| `synthdiet.available_diseases()` | Lista todas as doenças registradas. |
| `synthdiet.get_disease(name)` | Retorna a classe pelo nome. |

## Planos de dieta

| Símbolo | Descrição |
|---------|-----------|
| `synthdiet.DietPlan` | Representação estruturada. |
| `synthdiet.mediterranean_diet()` | Dieta mediterrânea. |
| `synthdiet.dash_diet()` | DASH. |
| `synthdiet.keto_diet()` | Cetogênica. |
| `synthdiet.low_fodmap_diet()` | Baixa em FODMAP. |
| `synthdiet.low_sodium_renal_diet()` | Renal hipossódica. |
| `synthdiet.diabetic_diet()` | Diabética. |
| `synthdiet.vegan_diet()` | Vegana. |
| `synthdiet.standard_diet()` | Padrão (controle). |

## Geradores

| Símbolo | Descrição |
|---------|-----------|
| `synthdiet.RandomPatientGenerator` | Geração aleatória. |
| `synthdiet.DistributionPatientGenerator` | A partir de distribuições. |
| `synthdiet.CopulaPatientGenerator` | Por cópulas (variáveis correlacionadas). |
| `synthdiet.CohortGenerator` | Gera lista a partir de uma especificação. |
| `synthdiet.CohortSpec` | Configuração de coorte. |
| `synthdiet.DiseaseSpec` | Distribuição de uma doença na coorte. |
| `synthdiet.MarkovProgressionGenerator` | Progressão por Markov. |

## Simulação

| Símbolo | Descrição |
|---------|-----------|
| `synthdiet.DietSimulator` | Simulador principal (simples + Hall 2011). |
| `synthdiet.SimulationResult` | Resultado com trajetória dos biomarcadores. |
| `synthdiet.HallSimulation` | Implementação do modelo de Hall 2011. |
| `synthdiet.HallSimulationParameters` | Parâmetros ajustáveis. |

## Ensaios clínicos

| Símbolo | Descrição |
|---------|-----------|
| `synthdiet.trials.ParallelTrial` | ECR de braços paralelos. |
| `synthdiet.trials.CrossoverTrial` | Cruzado. |
| `synthdiet.trials.FactorialTrial` | Fatorial 2×2. |
| `synthdiet.trials.intention_to_treat` | Análise ITT. |
| `synthdiet.trials.per_protocol` | Por protocolo. |

## Índices de qualidade

| Símbolo | Descrição |
|---------|-----------|
| `synthdiet.indices.HEI2020` | Healthy Eating Index 2020. |
| `synthdiet.indices.AHEI2010` | Alternate HEI 2010. |
| `synthdiet.indices.MEDAS` | Adesão à dieta mediterrânea. |
| `synthdiet.indices.DASHScore` | Adesão à DASH. |
| `synthdiet.indices.PHDI` | Planetary Health Diet Index. |
| `synthdiet.indices.DII` | Dietary Inflammatory Index. |

## Inferência causal

| Símbolo | Descrição |
|---------|-----------|
| `synthdiet.causal.counterfactual_run` | Simulação contrafactual do mesmo paciente em duas dietas. |
| `synthdiet.causal.ATEEstimator` | Estimador do ATE. |
| `synthdiet.causal.cate_by_subgroup` | CATE por subgrupos. |
| `synthdiet.causal.ConfoundingExperiment` | Confundimento + IPTW + g-fórmula. |
| `synthdiet.causal.DietDAG` | Utilitário leve de DAG. |

## Educação

| Símbolo | Descrição |
|---------|-----------|
| `synthdiet.education.CaseStudy` | Caso clínico. |
| `synthdiet.education.OSCEStation` | Estação OSCE. |
| `synthdiet.education.built_in_cases()` | Os 15 casos integrados. |

## Estatística e ruído

| Símbolo | Descrição |
|---------|-----------|
| `synthdiet.stats.sample_size_continuous` | Tamanho de amostra, desfecho contínuo. |
| `synthdiet.stats.sample_size_binary` | Tamanho de amostra, desfecho binário. |
| `synthdiet.stats.bootstrap_ci` | IC bootstrap. |
| `synthdiet.stats.permutation_test` | Teste de permutação. |
| `synthdiet.stats.fdr_bh` | FDR Benjamini-Hochberg. |
| `synthdiet.stats.ancova_baseline_adjusted` | ANCOVA ajustada à linha de base. |
| `synthdiet.noise.add_lab_measurement_error` | Erro de medida em laboratoriais. |
| `synthdiet.noise.inject_mcar_missing` | Faltantes MCAR. |
| `synthdiet.noise.inject_mar_missing` | Faltantes MAR. |
| `synthdiet.noise.inject_mnar_missing` | Faltantes MNAR. |
