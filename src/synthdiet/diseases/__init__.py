"""Disease catalogue.

Every disease subclass exposes:

* nutritional constraints (macro/micro targets, restricted foods, fluid limits)
* biomarker modifiers used when a synthetic patient is generated
* a ``response_to_diet`` hook used by the simulation engine to project how
  biomarkers evolve when a particular diet is applied.

All public diseases are registered with :data:`DISEASE_REGISTRY` so they can be
looked up by name (case-insensitive).
"""

from synthdiet.diseases.base import Disease, NutritionalConstraints
from synthdiet.diseases.cardiovascular import (
    Dyslipidemia,
    Hypertension,
    MetabolicSyndrome,
)
from synthdiet.diseases.diabetes import (
    GestationalDiabetes,
    PreDiabetes,
    Type1Diabetes,
    Type2Diabetes,
)
from synthdiet.diseases.eating_disorders import (
    AnorexiaNervosa,
    BingeEatingDisorder,
    BulimiaNervosa,
)
from synthdiet.diseases.endocrine import Hyperthyroidism, Hypothyroidism, PCOS
from synthdiet.diseases.food_allergies import (
    EggAllergy,
    LactoseIntolerance,
    PeanutAllergy,
    SoyAllergy,
    TreeNutAllergy,
)
from synthdiet.diseases.gastrointestinal import (
    CeliacDisease,
    CrohnsDisease,
    GERD,
    IBS,
    UlcerativeColitis,
)
from synthdiet.diseases.hepatic import Cirrhosis, NAFLD
from synthdiet.diseases.musculoskeletal import Gout, Osteoporosis, Sarcopenia
from synthdiet.diseases.obesity import Obesity, Overweight
from synthdiet.diseases.oncology import CancerCachexia
from synthdiet.diseases.registry import (
    DISEASE_REGISTRY,
    available_diseases,
    get_disease,
)
from synthdiet.diseases.renal import (
    ChronicKidneyDisease,
    KidneyStones,
    NephroticSyndrome,
)

__all__ = [
    "AnorexiaNervosa",
    "BingeEatingDisorder",
    "BulimiaNervosa",
    "CancerCachexia",
    "CeliacDisease",
    "ChronicKidneyDisease",
    "Cirrhosis",
    "CrohnsDisease",
    "DISEASE_REGISTRY",
    "Disease",
    "Dyslipidemia",
    "EggAllergy",
    "GERD",
    "GestationalDiabetes",
    "Gout",
    "Hyperthyroidism",
    "Hypertension",
    "Hypothyroidism",
    "IBS",
    "KidneyStones",
    "LactoseIntolerance",
    "MetabolicSyndrome",
    "NAFLD",
    "NephroticSyndrome",
    "NutritionalConstraints",
    "Obesity",
    "Osteoporosis",
    "Overweight",
    "PCOS",
    "PeanutAllergy",
    "PreDiabetes",
    "Sarcopenia",
    "SoyAllergy",
    "TreeNutAllergy",
    "Type1Diabetes",
    "Type2Diabetes",
    "UlcerativeColitis",
    "available_diseases",
    "get_disease",
]
