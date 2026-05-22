# synthdiet

[![PyPI](https://img.shields.io/pypi/v/synthdiet.svg)](https://pypi.org/project/synthdiet/)
[![Python](https://img.shields.io/pypi/pyversions/synthdiet.svg)](https://pypi.org/project/synthdiet/)
[![Licencia: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/bugraayancom/synthdiet/actions/workflows/ci.yml/badge.svg)](https://github.com/bugraayancom/synthdiet/actions/workflows/ci.yml)

> Otros idiomas: [English](README.md) · [Türkçe](README.tr.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Português](README.pt.md) · [Italiano](README.it.md) · [中文](README.zh.md) · [日本語](README.ja.md)
Una biblioteca de Python para **generar pacientes sintéticos** con
condiciones clínicas realistas y **simular intervenciones dietéticas**
sobre ellos.

`synthdiet` está pensado para nutricionistas-dietistas, investigadores
de nutrición clínica y educadores que quieran prototipar dietas,
ejecutar ensayos virtuales y poner a prueba recomendaciones nutricionales
sobre cientos o miles de pacientes sintéticos antes de llevarlas a la
clínica.

> Aviso: `synthdiet` es una herramienta de investigación y enseñanza.
> Los números que produce **no son recomendaciones clínicas** y los
> pacientes sintéticos **no son personas reales**. Para la atención al
> paciente consulte siempre a un dietista-nutricionista cualificado.

![synthdiet hero](app/assets/screenshots/00_hero.png)

---

## Autor

**Buğra Ayan** — Ankara / Turquía
- Sitio web: <https://bugraayan.com>
- Correo: <bugraayan.com@gmail.com>
- Google Scholar: <https://scholar.google.com/citations?user=VHGqzNMAAAAJ&hl=tr>

---

## Características

### Modelo de dominio principal
- Una clase `Patient` tipada que agrega demografía, antropometría,
  estilo de vida, biomarcadores de laboratorio, diagnósticos y
  medicación actual.
- Un registro de **más de 25 enfermedades** que cubren las categorías
  endocrina, cardiovascular, renal, hepática, gastrointestinal,
  metabólica, musculoesquelética, oncológica, psiquiátrica y alérgica.
- Un registro de **19 interacciones fármaco-nutriente** clínicamente
  relevantes (metformina → B12, estatinas → pomelo, warfarina →
  vitamina K, momento de la levotiroxina, crisis tiramínica con IMAO,
  etc.).
- 5 generadores de pacientes sintéticos (aleatorio, por distribución,
  por cópula, cohorte, progresión de Markov).
- Una base de datos de 45 alimentos con desglose macro/micronutriente
  y 8 dietas predefinidas (mediterránea, DASH, cetogénica, baja en
  FODMAP, renal baja en sodio, diabética, vegana, estándar).

### Profundidad metodológica (expansión v0.1)
- **Modelo de composición corporal de Hall (2011)** opcional
  (`DietSimulator(engine="hall_2011")`), con partición de masa
  grasa/magra mediante la ecuación de Forbes y termogénesis
  adaptativa.
- **Dinámica de adherencia y abandono**: constante, decreciente,
  abandono Weibull, salto estocástico, carga percibida.
- **Motor de ECA** (`synthdiet.trials`) con diseños paralelos,
  cruzados y factoriales 2×2; aleatorización estratificada / por
  bloques / por minimización; modelado de abandono; análisis ITT/PP/AT.
- **Inferencia causal** (`synthdiet.causal`): simulación
  contrafactual, estimadores ATE/CATE, experimentos de confusión con
  IPTW y g-fórmula, DAGs ligeros.
- **Índices de calidad de la dieta** (`synthdiet.indices`): HEI-2020,
  AHEI-2010, MEDAS, puntuación DASH, PHDI, DII.
- **Ayudas estadísticas** (`synthdiet.stats`): cálculo de potencia
  para resultados continuos y binarios, IC bootstrap, pruebas de
  permutación, ajustes de Benjamini-Hochberg + Holm-Bonferroni,
  ANCOVA ajustada por línea base.
- **Inyección de error de medida y datos faltantes**
  (`synthdiet.noise`): CV% por ensayo, sesgo de auto-reporte,
  patrones MCAR/MAR/MNAR.
- **15 casos clínicos + evaluación tipo OSCE**
  (`synthdiet.education`).
- **Suite de validación** contra 5 ECAs históricos
  (`synthdiet.validation`): DASH-Sodium, PREDIMED, DiRECT,
  Look AHEAD, Diabetes Prevention Program.
- **Visualización** (`synthdiet.viz`, opcional): diagrama CONSORT,
  forest plot, banda de trayectorias, Tabla 1.

---

## Instalación

```bash
pip install synthdiet
```

Extras opcionales:

```bash
pip install "synthdiet[viz]"     # visualizaciones con matplotlib
pip install "synthdiet[causal]"  # exportación de DAG con networkx
pip install "synthdiet[docs]"    # Sphinx + furo + myst-parser
pip install "synthdiet[dev]"     # pytest + ruff + mypy + matplotlib
```

`synthdiet` requiere Python 3.9+ y depende de `numpy`, `pandas` y `scipy`.

---

## Recorrido en 60 segundos

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

Ejemplos completos en [`examples/`](examples/) y tutoriales en español
en [`docs/es/`](docs/es/).

---

## Citación

```bibtex
@software{ayan_synthdiet_2026,
  author  = {Buğra Ayan},
  title   = {synthdiet: A Python library for simulating diets on synthetic patients},
  year    = {2026},
  version = {0.1.0},
  url     = {https://bugraayan.com}
}
```

## Licencia

MIT — véase [`LICENSE`](LICENSE).
