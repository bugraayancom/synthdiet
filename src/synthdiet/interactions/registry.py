"""Registry of 20 clinically important drug-nutrient interactions."""

from __future__ import annotations

from typing import Callable, Dict, List

from synthdiet.interactions.medications import DrugInteraction, Medication


def _metformin() -> Medication:
    return Medication(
        name="metformin",
        drug_class="biguanide",
        daily_dose_mg=2000,
        interactions=[
            DrugInteraction(
                nutrient="vitamin_b12",
                biomarker="vitamin_b12_pg_ml",
                direction="depletes",
                monthly_biomarker_delta=-8.0,
                severity="moderate",
                recommendation="Monitor B12 yearly; supplement if levels < 300 pg/mL.",
            ),
        ],
    )


def _atorvastatin() -> Medication:
    return Medication(
        name="atorvastatin",
        drug_class="HMG-CoA reductase inhibitor (statin)",
        daily_dose_mg=20,
        interactions=[
            DrugInteraction(
                nutrient="coq10",
                direction="depletes",
                severity="moderate",
                recommendation="Consider CoQ10 supplementation if muscle symptoms occur.",
            ),
            DrugInteraction(
                nutrient="grapefruit",
                direction="competes_absorption",
                severity="severe",
                forbid_foods={"grapefruit", "grapefruit_juice"},
                recommendation="Avoid grapefruit (CYP3A4 inhibition raises statin exposure).",
            ),
        ],
    )


def _simvastatin() -> Medication:
    return Medication(
        name="simvastatin",
        drug_class="HMG-CoA reductase inhibitor (statin)",
        daily_dose_mg=20,
        interactions=[
            DrugInteraction(
                nutrient="grapefruit",
                direction="competes_absorption",
                severity="severe",
                forbid_foods={"grapefruit", "grapefruit_juice"},
                recommendation="Strictly avoid grapefruit; risk of rhabdomyolysis.",
            ),
        ],
    )


def _warfarin() -> Medication:
    return Medication(
        name="warfarin",
        drug_class="vitamin K antagonist",
        daily_dose_mg=5,
        interactions=[
            DrugInteraction(
                nutrient="vitamin_k",
                direction="competes_absorption",
                severity="severe",
                recommendation="Keep vitamin K intake CONSISTENT (not necessarily low).",
                forbid_foods={"high_vitamin_k_changes"},
                timing_advice="Aim for steady leafy-green intake day to day.",
            ),
        ],
    )


def _levothyroxine() -> Medication:
    return Medication(
        name="levothyroxine",
        drug_class="thyroid hormone replacement",
        daily_dose_mg=0.1,
        interactions=[
            DrugInteraction(
                nutrient="calcium",
                direction="competes_absorption",
                severity="moderate",
                forbid_foods={"calcium_supplements"},
                recommendation="Separate calcium/iron supplements by ≥ 4 hours.",
                timing_advice="Take on empty stomach 30-60 min before breakfast.",
            ),
            DrugInteraction(
                nutrient="iron",
                direction="competes_absorption",
                severity="moderate",
                forbid_foods={"iron_supplements"},
                recommendation="Separate iron supplements by ≥ 4 hours.",
            ),
            DrugInteraction(
                nutrient="soy_protein",
                direction="competes_absorption",
                severity="mild",
                forbid_foods={"soy", "soy_milk", "tofu"},
                recommendation="High-soy diets may require dose adjustment.",
            ),
        ],
    )


def _phenelzine() -> Medication:
    return Medication(
        name="phenelzine",
        drug_class="MAO inhibitor",
        daily_dose_mg=45,
        interactions=[
            DrugInteraction(
                nutrient="tyramine",
                direction="competes_absorption",
                severity="severe",
                forbid_foods={
                    "aged_cheese",
                    "cured_meats",
                    "soy_sauce",
                    "miso",
                    "tap_beer",
                    "fermented_foods",
                },
                recommendation="Avoid tyramine-rich foods: hypertensive crisis risk.",
            ),
        ],
    )


def _lithium() -> Medication:
    return Medication(
        name="lithium",
        drug_class="mood stabiliser",
        daily_dose_mg=900,
        interactions=[
            DrugInteraction(
                nutrient="sodium",
                direction="competes_absorption",
                severity="severe",
                recommendation="Keep sodium intake stable; large drops raise lithium levels.",
            ),
            DrugInteraction(
                nutrient="caffeine",
                direction="competes_absorption",
                severity="moderate",
                forbid_foods={"caffeine_changes"},
                recommendation="Avoid sudden caffeine changes; may alter lithium clearance.",
            ),
        ],
    )


def _omeprazole() -> Medication:
    return Medication(
        name="omeprazole",
        drug_class="proton pump inhibitor",
        daily_dose_mg=20,
        interactions=[
            DrugInteraction(
                nutrient="vitamin_b12",
                biomarker="vitamin_b12_pg_ml",
                direction="depletes",
                monthly_biomarker_delta=-6.0,
                severity="moderate",
                recommendation="Monitor B12 if PPI use > 2 years.",
            ),
            DrugInteraction(
                nutrient="magnesium",
                biomarker="magnesium_mg_dl",
                direction="depletes",
                monthly_biomarker_delta=-0.02,
                severity="moderate",
                recommendation="Check magnesium yearly with chronic PPI use.",
            ),
            DrugInteraction(
                nutrient="iron",
                direction="competes_absorption",
                severity="mild",
                recommendation="Reduced iron absorption; monitor ferritin in at-risk patients.",
            ),
        ],
    )


def _furosemide() -> Medication:
    return Medication(
        name="furosemide",
        drug_class="loop diuretic",
        daily_dose_mg=40,
        interactions=[
            DrugInteraction(
                nutrient="potassium",
                biomarker="potassium_mmol_l",
                direction="depletes",
                monthly_biomarker_delta=-0.10,
                severity="moderate",
                recommendation="Encourage potassium-rich foods; check potassium regularly.",
            ),
            DrugInteraction(
                nutrient="magnesium",
                biomarker="magnesium_mg_dl",
                direction="depletes",
                monthly_biomarker_delta=-0.03,
                severity="moderate",
                recommendation="Monitor magnesium with long-term loop diuretic use.",
            ),
        ],
    )


def _hydrochlorothiazide() -> Medication:
    return Medication(
        name="hydrochlorothiazide",
        drug_class="thiazide diuretic",
        daily_dose_mg=25,
        interactions=[
            DrugInteraction(
                nutrient="potassium",
                biomarker="potassium_mmol_l",
                direction="depletes",
                monthly_biomarker_delta=-0.07,
                severity="moderate",
                recommendation="Encourage potassium-rich foods.",
            ),
            DrugInteraction(
                nutrient="uric_acid",
                biomarker="uric_acid_mg_dl",
                direction="increases",
                monthly_biomarker_delta=0.10,
                severity="moderate",
                recommendation="Caution in patients with gout history.",
            ),
        ],
    )


def _prednisone() -> Medication:
    return Medication(
        name="prednisone",
        drug_class="corticosteroid",
        daily_dose_mg=20,
        interactions=[
            DrugInteraction(
                nutrient="calcium",
                biomarker="calcium_mg_dl",
                direction="depletes",
                monthly_biomarker_delta=-0.05,
                severity="severe",
                recommendation="Increase Ca + vitamin D; assess bone density during chronic use.",
            ),
            DrugInteraction(
                nutrient="potassium",
                biomarker="potassium_mmol_l",
                direction="depletes",
                monthly_biomarker_delta=-0.06,
                severity="moderate",
                recommendation="Monitor potassium with prolonged steroid therapy.",
            ),
            DrugInteraction(
                nutrient="glucose",
                biomarker="fasting_glucose_mg_dl",
                direction="increases",
                monthly_biomarker_delta=4.0,
                severity="severe",
                recommendation="Steroid-induced hyperglycaemia; monitor in diabetics.",
            ),
        ],
    )


def _isoniazid() -> Medication:
    return Medication(
        name="isoniazid",
        drug_class="anti-tuberculous",
        daily_dose_mg=300,
        interactions=[
            DrugInteraction(
                nutrient="vitamin_b6",
                direction="depletes",
                severity="severe",
                recommendation="Supplement pyridoxine 25-50 mg/day to prevent neuropathy.",
            ),
        ],
    )


def _methotrexate() -> Medication:
    return Medication(
        name="methotrexate",
        drug_class="antifolate immunosuppressant",
        daily_dose_mg=15,
        interactions=[
            DrugInteraction(
                nutrient="folate",
                biomarker="folate_ng_ml",
                direction="depletes",
                monthly_biomarker_delta=-1.0,
                severity="severe",
                recommendation="Co-prescribe folic acid 1-5 mg/day to mitigate toxicity.",
            ),
        ],
    )


def _digoxin() -> Medication:
    return Medication(
        name="digoxin",
        drug_class="cardiac glycoside",
        daily_dose_mg=0.125,
        interactions=[
            DrugInteraction(
                nutrient="fiber",
                direction="competes_absorption",
                severity="mild",
                recommendation="Separate digoxin dose from high-fibre meals by 2 hours.",
            ),
            DrugInteraction(
                nutrient="potassium",
                direction="competes_absorption",
                severity="severe",
                recommendation="Hypokalaemia potentiates digoxin toxicity.",
            ),
        ],
    )


def _ace_inhibitor() -> Medication:
    return Medication(
        name="lisinopril",
        drug_class="ACE inhibitor",
        daily_dose_mg=10,
        interactions=[
            DrugInteraction(
                nutrient="potassium",
                biomarker="potassium_mmol_l",
                direction="increases",
                monthly_biomarker_delta=0.05,
                severity="moderate",
                recommendation="Avoid high-dose K supplements; monitor K with K-sparing agents.",
            ),
        ],
    )


def _spironolactone() -> Medication:
    return Medication(
        name="spironolactone",
        drug_class="K-sparing diuretic",
        daily_dose_mg=25,
        interactions=[
            DrugInteraction(
                nutrient="potassium",
                biomarker="potassium_mmol_l",
                direction="increases",
                monthly_biomarker_delta=0.10,
                severity="severe",
                recommendation="Risk of hyperkalaemia; avoid K supplements and salt substitutes.",
            ),
        ],
    )


def _bisphosphonate() -> Medication:
    return Medication(
        name="alendronate",
        drug_class="bisphosphonate",
        daily_dose_mg=70,  # weekly dose, model as average
        interactions=[
            DrugInteraction(
                nutrient="calcium",
                direction="competes_absorption",
                severity="severe",
                forbid_foods={"calcium_supplements"},
                recommendation="Take with plain water; wait 30+ min before food/calcium.",
                timing_advice="Take first thing in morning, fasting.",
            ),
        ],
    )


def _ssri() -> Medication:
    return Medication(
        name="fluoxetine",
        drug_class="SSRI",
        daily_dose_mg=20,
        interactions=[
            DrugInteraction(
                nutrient="tryptophan",
                direction="competes_absorption",
                severity="moderate",
                forbid_foods={"st_johns_wort", "tryptophan_supplements"},
                recommendation="Avoid St John's wort; combination risks serotonin syndrome.",
            ),
        ],
    )


def _bile_acid_resin() -> Medication:
    return Medication(
        name="cholestyramine",
        drug_class="bile acid sequestrant",
        daily_dose_mg=4000,
        interactions=[
            DrugInteraction(
                nutrient="fat_soluble_vitamins",
                direction="competes_absorption",
                severity="moderate",
                recommendation="Supplement A, D, E, K with long-term use.",
                timing_advice="Separate other medications by ≥ 4 hours.",
            ),
        ],
    )


INTERACTION_REGISTRY: Dict[str, Callable[[], Medication]] = {
    "metformin": _metformin,
    "atorvastatin": _atorvastatin,
    "simvastatin": _simvastatin,
    "warfarin": _warfarin,
    "levothyroxine": _levothyroxine,
    "phenelzine": _phenelzine,
    "lithium": _lithium,
    "omeprazole": _omeprazole,
    "furosemide": _furosemide,
    "hydrochlorothiazide": _hydrochlorothiazide,
    "prednisone": _prednisone,
    "isoniazid": _isoniazid,
    "methotrexate": _methotrexate,
    "digoxin": _digoxin,
    "lisinopril": _ace_inhibitor,
    "spironolactone": _spironolactone,
    "alendronate": _bisphosphonate,
    "fluoxetine": _ssri,
    "cholestyramine": _bile_acid_resin,
}


def get_medication(name: str) -> Medication:
    try:
        return INTERACTION_REGISTRY[name.lower()]()
    except KeyError as exc:
        raise KeyError(
            f"unknown medication {name!r}. Known: {sorted(INTERACTION_REGISTRY)}"
        ) from exc


def available_medications() -> List[str]:
    return sorted(INTERACTION_REGISTRY)
