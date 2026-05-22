"""synthdiet: a Python library for simulating diets on synthetic patients.

Quick start
-----------

>>> from synthdiet import CohortGenerator, CohortSpec, DiseaseSpec
>>> from synthdiet.diets import mediterranean_diet
>>> from synthdiet.simulation import DietSimulator
>>> from synthdiet.evaluation import evaluate_simulation, format_evaluation_report
>>>
>>> spec = CohortSpec(
...     size=10,
...     diseases=[DiseaseSpec("type_2_diabetes", prevalence=0.5)],
... )
>>> cohort = CohortGenerator(spec, seed=42).generate()
>>> sim = DietSimulator(adherence=0.8)
>>> result = sim.run(cohort[0], mediterranean_diet(), duration_weeks=12)
>>> ev = evaluate_simulation(result)
>>> print(format_evaluation_report(ev))  # doctest: +SKIP

See ``examples/`` and ``README.md`` for full examples.
"""

from synthdiet.diets import (
    DIET_PRESETS,
    DietPlan,
    FoodServing,
    Meal,
    dash_diet,
    diabetic_diet,
    keto_diet,
    list_presets,
    low_fodmap_diet,
    low_sodium_renal_diet,
    mediterranean_diet,
    standard_diet,
    vegan_diet,
)
from synthdiet.diseases import (
    DISEASE_REGISTRY,
    Disease,
    NutritionalConstraints,
    available_diseases,
    get_disease,
)
from synthdiet.evaluation import (
    DietEvaluation,
    aggregate_cohort_results,
    evaluate_simulation,
    format_evaluation_report,
    summarise_cohort,
)
from synthdiet.generators import (
    CohortGenerator,
    CohortSpec,
    CopulaPatientGenerator,
    DiseaseSpec,
    DistributionPatientGenerator,
    MarkovProgressionGenerator,
    PatientGenerator,
    ProgressionState,
    RandomPatientGenerator,
)
from synthdiet.nutrition import (
    DRI_TABLE,
    Food,
    FoodDatabase,
    MACRONUTRIENTS,
    MICRONUTRIENTS,
    NutrientProfile,
    daily_reference_intake,
    default_food_database,
    estimate_protein_requirement_g,
)
from synthdiet.patients import (
    ActivityLevel,
    Anthropometrics,
    Biomarkers,
    Demographics,
    Lifestyle,
    Patient,
    Sex,
    SmokingStatus,
)
from synthdiet.behavior import (
    AdherenceModel,
    ConstantAdherence,
    DecayingAdherence,
    PerceivedBurdenAdherence,
    StochasticSkipAdherence,
    WeibullDropoutAdherence,
)
from synthdiet.interactions import (
    Medication,
    available_medications,
    get_medication,
)
from synthdiet.simulation import (
    DietSimulator,
    HallSimulation,
    HallSimulationParameters,
    HallState,
    SimulationResult,
    TimePoint,
    basal_metabolic_rate,
    estimate_baseline_intake,
    forbes_partition,
    harris_benedict,
    initialise_body_composition,
    mifflin_st_jeor,
    project_weight_change,
    total_daily_energy_expenditure,
)

__version__ = "0.1.0"
__author__ = "Buğra Ayan"
__email__ = "bugraayan.com@gmail.com"
__license__ = "MIT"
__url__ = "https://bugraayan.com"
__scholar__ = "https://scholar.google.com/citations?user=VHGqzNMAAAAJ&hl=tr"
__affiliation__ = "Ankara / Türkiye"

__all__ = [
    "ActivityLevel",
    "AdherenceModel",
    "Anthropometrics",
    "Biomarkers",
    "CohortGenerator",
    "CohortSpec",
    "ConstantAdherence",
    "CopulaPatientGenerator",
    "DIET_PRESETS",
    "DISEASE_REGISTRY",
    "DRI_TABLE",
    "DecayingAdherence",
    "Demographics",
    "DietEvaluation",
    "DietPlan",
    "DietSimulator",
    "Disease",
    "DiseaseSpec",
    "DistributionPatientGenerator",
    "Food",
    "FoodDatabase",
    "FoodServing",
    "HallSimulation",
    "HallSimulationParameters",
    "HallState",
    "Lifestyle",
    "MACRONUTRIENTS",
    "MICRONUTRIENTS",
    "MarkovProgressionGenerator",
    "Meal",
    "Medication",
    "NutrientProfile",
    "NutritionalConstraints",
    "Patient",
    "PatientGenerator",
    "PerceivedBurdenAdherence",
    "ProgressionState",
    "RandomPatientGenerator",
    "Sex",
    "SimulationResult",
    "SmokingStatus",
    "StochasticSkipAdherence",
    "TimePoint",
    "WeibullDropoutAdherence",
    "__affiliation__",
    "__author__",
    "__email__",
    "__license__",
    "__scholar__",
    "__url__",
    "__version__",
    "aggregate_cohort_results",
    "available_diseases",
    "available_medications",
    "basal_metabolic_rate",
    "daily_reference_intake",
    "dash_diet",
    "default_food_database",
    "diabetic_diet",
    "estimate_baseline_intake",
    "estimate_protein_requirement_g",
    "evaluate_simulation",
    "forbes_partition",
    "format_evaluation_report",
    "get_disease",
    "get_medication",
    "harris_benedict",
    "initialise_body_composition",
    "keto_diet",
    "list_presets",
    "low_fodmap_diet",
    "low_sodium_renal_diet",
    "mediterranean_diet",
    "mifflin_st_jeor",
    "project_weight_change",
    "standard_diet",
    "summarise_cohort",
    "total_daily_energy_expenditure",
    "vegan_diet",
]
