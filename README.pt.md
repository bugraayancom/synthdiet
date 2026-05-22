# synthdiet

[![PyPI](https://img.shields.io/pypi/v/synthdiet.svg)](https://pypi.org/project/synthdiet/)
[![Python](https://img.shields.io/pypi/pyversions/synthdiet.svg)](https://pypi.org/project/synthdiet/)
[![Licença: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/bugraayancom/synthdiet/actions/workflows/ci.yml/badge.svg)](https://github.com/bugraayancom/synthdiet/actions/workflows/ci.yml)

> Outros idiomas: [English](README.md) · [Türkçe](README.tr.md) · [Español](README.es.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [中文](README.zh.md) · [日本語](README.ja.md)
Uma biblioteca Python para **gerar pacientes sintéticos** com
quadros clínicos realistas e **simular intervenções dietéticas**
sobre eles.

`synthdiet` foi criado para nutricionistas, pesquisadores em nutrição
clínica e educadores que queiram prototipar dietas, executar ensaios
virtuais e estressar recomendações nutricionais sobre centenas ou
milhares de pacientes sintéticos antes de levá-las à prática clínica.

> Aviso: `synthdiet` é uma ferramenta de pesquisa e ensino. Os
> números que produz **não são recomendações clínicas** e os pacientes
> sintéticos **não são pessoas reais**. Para o cuidado de pacientes
> reais, consulte sempre um(a) nutricionista qualificado(a).

![synthdiet hero](app/assets/screenshots/00_hero.png)

---

## Autor

**Buğra Ayan** — Ancara / Turquia
- Site: <https://bugraayan.com>
- E-mail: <bugraayan.com@gmail.com>
- Google Scholar: <https://scholar.google.com/citations?user=VHGqzNMAAAAJ&hl=tr>

---

## Recursos

### Modelo de domínio
- Uma classe `Patient` tipada agregando demografia, antropometria,
  estilo de vida, biomarcadores laboratoriais, diagnósticos e
  medicações.
- Registro de **mais de 25 doenças** cobrindo categorias endócrina,
  cardiovascular, renal, hepática, gastrointestinal, metabólica,
  musculoesquelética, oncológica, psiquiátrica e alérgica.
- Registro de **19 interações fármaco-nutriente** clinicamente
  relevantes (metformina → B12, estatinas → toranja, varfarina →
  vitamina K, horário da levotiroxina, crise tiramínica com IMAO etc.).
- 5 geradores de pacientes sintéticos (aleatório, por distribuição,
  por cópula, coorte, progressão de Markov).
- Banco de 45 alimentos com discriminação macro/micronutricional e
  8 dietas pré-definidas (mediterrânea, DASH, cetogênica, baixa em
  FODMAP, renal hipossódica, diabética, vegana, padrão).

### Profundidade metodológica (v0.1)
- **Modelo de composição corporal de Hall (2011)** opcional
  (`DietSimulator(engine="hall_2011")`), com partição massa
  gorda/magra via equação de Forbes e termogênese adaptativa.
- **Dinâmicas de adesão e abandono**: constante, decrescente,
  abandono Weibull, salto estocástico, carga percebida.
- **Mecanismo de ECR** (`synthdiet.trials`): braços paralelos,
  cruzados (crossover) e fatorial 2×2; randomização estratificada /
  por blocos / por minimização; modelagem de abandono; análises
  ITT/PP/AT.
- **Inferência causal** (`synthdiet.causal`): simulação
  contrafactual, estimadores ATE/CATE, experimentos de confundimento
  com IPTW e g-fórmula, DAGs leves.
- **Índices de qualidade da dieta** (`synthdiet.indices`): HEI-2020,
  AHEI-2010, MEDAS, escore DASH, PHDI, DII.
- **Auxiliares estatísticos** (`synthdiet.stats`): cálculo de poder
  para desfechos contínuos e binários, IC bootstrap, testes de
  permutação, ajustes Benjamini-Hochberg + Holm-Bonferroni, ANCOVA
  ajustada à linha de base.
- **Injeção de erro de medida e dados ausentes**
  (`synthdiet.noise`): CV% por ensaio, viés de auto-relato, padrões
  MCAR/MAR/MNAR.
- **15 casos clínicos + avaliação tipo OSCE**
  (`synthdiet.education`).
- **Suíte de validação** contra 5 ECRs marcantes
  (`synthdiet.validation`): DASH-Sodium, PREDIMED, DiRECT,
  Look AHEAD, Diabetes Prevention Program.
- **Visualização** (`synthdiet.viz`, opcional): diagrama CONSORT,
  forest plot, faixa de trajetórias, Tabela 1.

---

## Instalação

```bash
pip install synthdiet
```

Extras opcionais:

```bash
pip install "synthdiet[viz]"     # visualizações com matplotlib
pip install "synthdiet[causal]"  # exportação de DAG via networkx
pip install "synthdiet[docs]"    # Sphinx + furo + myst-parser
pip install "synthdiet[dev]"     # pytest + ruff + mypy + matplotlib
```

`synthdiet` requer Python 3.9+ e depende de `numpy`, `pandas` e `scipy`.

---

## Tour de 60 segundos

```python
from synthdiet import (
    CohortGenerator, CohortSpec, DiseaseSpec,
    DietSimulator, mediterranean_diet,
    evaluate_simulation, format_evaluation_report,
)

spec = CohortSpec(
    size=100,
    diseases=[
        DiseaseSpec("type_2_diabetes", prevalence=0.40),
        DiseaseSpec("hypertension",     prevalence=0.45),
    ],
)
cohort = CohortGenerator(spec, seed=42).generate()

simulator = DietSimulator(adherence=0.8)
diet = mediterranean_diet(daily_energy_kcal=1800)

for patient in cohort[:3]:
    result = simulator.run(patient, diet, duration_weeks=12)
    evaluation = evaluate_simulation(result)
    print(format_evaluation_report(evaluation))
    print("-" * 60)
```

Exemplos completos em [`examples/`](examples/); tutoriais em português
em [`docs/pt/`](docs/pt/).

---

## Citação

```bibtex
@software{ayan_synthdiet_2026,
  author  = {Buğra Ayan},
  title   = {synthdiet: A Python library for simulating diets on synthetic patients},
  year    = {2026},
  version = {0.1.0},
  url     = {https://bugraayan.com}
}
```

## Licença

MIT — veja [`LICENSE`](LICENSE).
