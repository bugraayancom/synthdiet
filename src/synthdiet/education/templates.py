"""Built-in clinical case templates (15 scenarios)."""

from __future__ import annotations

from typing import Callable, Dict, List

from synthdiet.diets.presets import (
    dash_diet,
    diabetic_diet,
    low_fodmap_diet,
    low_sodium_renal_diet,
    mediterranean_diet,
    standard_diet,
    vegan_diet,
)
from synthdiet.diseases import (
    AnorexiaNervosa,
    CancerCachexia,
    CeliacDisease,
    ChronicKidneyDisease,
    Cirrhosis,
    Dyslipidemia,
    GestationalDiabetes,
    Gout,
    Hyperthyroidism,
    Hypertension,
    Hypothyroidism,
    IBS,
    Obesity,
    Osteoporosis,
    PCOS,
    Sarcopenia,
    Type2Diabetes,
)
from synthdiet.education.cases import CaseSolution, CaseStudy, LearningObjective
from synthdiet.interactions import get_medication
from synthdiet.patients import (
    ActivityLevel,
    Anthropometrics,
    Biomarkers,
    Demographics,
    Lifestyle,
    Patient,
    Sex,
)


def _case_t2dm_ht_dyslip() -> CaseStudy:
    p = Patient(
        demographics=Demographics(age=58, sex=Sex.MALE, country="TR"),
        anthropometrics=Anthropometrics(height_cm=174, weight_kg=98, waist_cm=110),
        lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT,
                            cooking_skill="medium"),
        biomarkers=Biomarkers(values={
            "hba1c_pct": 7.6, "fasting_glucose_mg_dl": 168,
            "ldl_mg_dl": 158, "hdl_mg_dl": 36, "triglycerides_mg_dl": 220,
            "systolic_bp_mmhg": 148, "diastolic_bp_mmhg": 92,
        }),
    )
    p.add_disease(Type2Diabetes(severity="moderate"))
    p.add_disease(Hypertension(severity="moderate"))
    p.add_disease(Dyslipidemia(severity="moderate"))
    p.add_medication(get_medication("metformin"))
    p.add_medication(get_medication("atorvastatin"))
    p.add_medication(get_medication("lisinopril"))
    return CaseStudy(
        case_id="C01",
        title="58 y M with T2DM, hypertension, and dyslipidemia",
        chief_complaint="Newly diagnosed T2DM, struggling to lose weight.",
        history=(
            "Office worker, sedentary. Eats mostly take-out. Family history of "
            "early MI. Started metformin and atorvastatin two months ago."
        ),
        patient=p,
        learning_objectives=[
            LearningObjective("LO1", "Plan a Mediterranean / DASH-aligned diet",
                              competency_area="diet_planning"),
            LearningObjective("LO2", "Counsel on metformin + B12 monitoring",
                              competency_area="drug_food"),
            LearningObjective("LO3", "Set a realistic weight-loss goal",
                              competency_area="goal_setting"),
        ],
        reference_solution=CaseSolution(
            summary="Mediterranean pattern, 1500-1700 kcal, sodium < 2 g.",
            prescribed_diet=mediterranean_diet(daily_energy_kcal=1700),
            rationale="Best evidence in T2DM + CVD risk; matches patient's culture.",
            expected_outcomes=["5% weight loss in 6 months",
                               "HbA1c 6.5-7.0%", "LDL < 100 mg/dL"],
        ),
        tags=["metabolic", "cardiometabolic", "common"],
    )


def _case_celiac_teen() -> CaseStudy:
    p = Patient(
        demographics=Demographics(age=15, sex=Sex.FEMALE),
        anthropometrics=Anthropometrics(height_cm=160, weight_kg=42),
        lifestyle=Lifestyle(activity_level=ActivityLevel.MODERATE),
        biomarkers=Biomarkers(values={
            "hemoglobin_g_dl": 10.6, "ferritin_ng_ml": 14,
            "vitamin_d_25oh_ng_ml": 18,
        }),
    )
    p.add_disease(CeliacDisease())
    return CaseStudy(
        case_id="C02",
        title="15 y F newly diagnosed celiac disease",
        chief_complaint="Diagnosed by biopsy after iron-deficiency anemia.",
        history=(
            "Vegetarian by preference. Family worried about social impact at school. "
            "Currently below the 10th percentile for weight."
        ),
        patient=p,
        learning_objectives=[
            LearningObjective("LO1", "Teach strict gluten-free diet rules"),
            LearningObjective("LO2", "Plan iron, folate, B12 repletion"),
            LearningObjective("LO3", "Address growth and adolescent psychosocial issues"),
        ],
        reference_solution=CaseSolution(
            summary="Gluten-free, iron and vitamin D supplementation, gradual weight gain.",
            prescribed_diet=standard_diet(daily_energy_kcal=2200),
            rationale="Lifelong gluten exclusion; explicit growth catch-up plan.",
            expected_outcomes=["Hemoglobin > 12 g/dL in 6 months",
                               "Weight gain 3-5 kg in 12 months"],
        ),
        tags=["paediatric", "gastrointestinal"],
    )


def _case_ckd4_dialysis() -> CaseStudy:
    p = Patient(
        demographics=Demographics(age=68, sex=Sex.MALE),
        anthropometrics=Anthropometrics(height_cm=170, weight_kg=82),
        lifestyle=Lifestyle(activity_level=ActivityLevel.SEDENTARY),
        biomarkers=Biomarkers(values={
            "creatinine_mg_dl": 4.6, "egfr_ml_min_1_73m2": 18,
            "bun_mg_dl": 48, "potassium_mmol_l": 5.4, "phosphate_mg_dl": 5.2,
            "albumin_g_dl": 3.5,
        }),
    )
    p.add_disease(ChronicKidneyDisease(stage=4))
    p.add_disease(Hypertension(severity="severe"))
    p.add_medication(get_medication("furosemide"))
    return CaseStudy(
        case_id="C03",
        title="68 y M with CKD stage 4 approaching dialysis",
        chief_complaint="Pre-dialysis dietary review.",
        history="Type 2 diabetic nephropathy. Lives alone.",
        patient=p,
        learning_objectives=[
            LearningObjective("LO1", "Plan low-protein, low-K, low-P diet"),
            LearningObjective("LO2", "Adjust prescription when dialysis starts"),
            LearningObjective("LO3", "Manage food security with limited social support"),
        ],
        reference_solution=CaseSolution(
            summary="Renal diet at 0.6-0.8 g/kg protein, K < 3 g/d, P < 1 g/d.",
            prescribed_diet=low_sodium_renal_diet(daily_energy_kcal=1900),
            rationale="Slow CKD progression while preventing malnutrition.",
            expected_outcomes=["Stable albumin", "K and P within target"],
        ),
        difficulty="advanced",
        tags=["renal", "complex"],
    )


def _case_gestational_dm() -> CaseStudy:
    p = Patient(
        demographics=Demographics(age=33, sex=Sex.FEMALE, pregnancy_trimester=2),
        anthropometrics=Anthropometrics(height_cm=163, weight_kg=78),
        lifestyle=Lifestyle(),
        biomarkers=Biomarkers(values={"fasting_glucose_mg_dl": 102}),
    )
    p.add_disease(GestationalDiabetes())
    return CaseStudy(
        case_id="C04",
        title="33 y F at 24 wk with GDM",
        chief_complaint="Failed OGTT at 24 weeks gestation.",
        history="Pre-pregnancy BMI 28. First pregnancy. No insulin use yet.",
        patient=p,
        learning_objectives=[
            LearningObjective("LO1", "Spread carbohydrates across 3 meals + 2 snacks"),
            LearningObjective("LO2", "Educate on lower-carb breakfast (dawn cortisol)"),
            LearningObjective("LO3", "Set safe gestational weight gain target"),
        ],
        reference_solution=CaseSolution(
            summary="Carb-controlled diet, breakfast carb ≤ 30 g.",
            prescribed_diet=diabetic_diet(daily_energy_kcal=2100),
            rationale="GDM-friendly carbohydrate distribution.",
        ),
        tags=["pregnancy", "diabetes"],
    )


def _case_obesity_class_iii_pre_bariatric() -> CaseStudy:
    p = Patient(
        demographics=Demographics(age=42, sex=Sex.FEMALE),
        anthropometrics=Anthropometrics(height_cm=160, weight_kg=132, waist_cm=128),
        lifestyle=Lifestyle(activity_level=ActivityLevel.SEDENTARY,
                            cooking_skill="low"),
    )
    p.add_disease(Obesity(bmi_class="III"))
    p.add_disease(Hypertension(severity="moderate"))
    p.add_medication(get_medication("hydrochlorothiazide"))
    return CaseStudy(
        case_id="C05",
        title="42 y F BMI 51, pre-bariatric evaluation",
        chief_complaint="Referred from bariatric surgery clinic.",
        history="Multiple failed diet attempts. Binge eating denied.",
        patient=p,
        learning_objectives=[
            LearningObjective("LO1", "Conduct pre-bariatric nutrition assessment"),
            LearningObjective("LO2", "Design liver-shrinking diet 2 wk pre-op"),
            LearningObjective("LO3", "Plan post-op stages and supplementation"),
        ],
        reference_solution=CaseSolution(
            summary="800 kcal liver-shrinking diet for 14 days pre-op.",
            prescribed_diet=diabetic_diet(daily_energy_kcal=800),
            rationale="Reduces hepatic glycogen and intra-abdominal fat.",
        ),
        difficulty="advanced",
        tags=["bariatric", "obesity"],
    )


def _case_anorexia_refeeding() -> CaseStudy:
    p = Patient(
        demographics=Demographics(age=19, sex=Sex.FEMALE),
        anthropometrics=Anthropometrics(height_cm=168, weight_kg=42),
        lifestyle=Lifestyle(activity_level=ActivityLevel.SEDENTARY),
        biomarkers=Biomarkers(values={
            "phosphate_mg_dl": 2.3, "potassium_mmol_l": 3.3,
            "magnesium_mg_dl": 1.5,
        }),
    )
    p.add_disease(AnorexiaNervosa())
    return CaseStudy(
        case_id="C06",
        title="19 y F admitted with BMI 14.9, anorexia nervosa",
        chief_complaint="Inpatient refeeding plan.",
        history="3 year history; first hospitalisation. Family on board.",
        patient=p,
        learning_objectives=[
            LearningObjective("LO1", "Recognise refeeding syndrome risk"),
            LearningObjective("LO2", "Start at ≤ 20 kcal/kg/day and titrate slowly"),
            LearningObjective("LO3", "Coordinate with MDT (psychiatry, paediatrics)"),
        ],
        reference_solution=CaseSolution(
            summary="Start 800 kcal/day, advance by 200 kcal every 2 days.",
            prescribed_diet=standard_diet(daily_energy_kcal=800),
            rationale="Avoid refeeding syndrome; correct electrolytes first.",
        ),
        difficulty="advanced",
        tags=["eating_disorder", "inpatient"],
    )


def _case_pcos() -> CaseStudy:
    p = Patient(
        demographics=Demographics(age=27, sex=Sex.FEMALE),
        anthropometrics=Anthropometrics(height_cm=164, weight_kg=84),
        lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT),
        biomarkers=Biomarkers(values={
            "fasting_insulin_uIU_ml": 22, "fasting_glucose_mg_dl": 96,
            "ldl_mg_dl": 128,
        }),
    )
    p.add_disease(PCOS())
    return CaseStudy(
        case_id="C07",
        title="27 y F with PCOS and insulin resistance",
        chief_complaint="Difficulty losing weight, irregular menses.",
        history="Diagnosed 1 year ago. Wishes to conceive in 12 months.",
        patient=p,
        learning_objectives=[
            LearningObjective("LO1", "Plan low-GI, insulin-sensitising diet"),
            LearningObjective("LO2", "Target 5-10% weight loss"),
            LearningObjective("LO3", "Educate on inositol and Mediterranean pattern"),
        ],
        reference_solution=CaseSolution(
            summary="Mediterranean-style at 1600 kcal, low GI emphasis.",
            prescribed_diet=mediterranean_diet(daily_energy_kcal=1600),
            rationale="Improves insulin sensitivity and ovulatory function.",
        ),
        tags=["endocrine", "reproductive"],
    )


def _case_cirrhosis_ascites() -> CaseStudy:
    p = Patient(
        demographics=Demographics(age=61, sex=Sex.MALE),
        anthropometrics=Anthropometrics(height_cm=172, weight_kg=70),
        lifestyle=Lifestyle(activity_level=ActivityLevel.SEDENTARY),
        biomarkers=Biomarkers(values={
            "albumin_g_dl": 2.8, "alt_u_l": 110, "ast_u_l": 95,
            "sodium_mmol_l": 130,
        }),
    )
    p.add_disease(Cirrhosis(child_pugh_class="B", ascites=True))
    return CaseStudy(
        case_id="C08",
        title="61 y M with cirrhosis Child B, ascites",
        chief_complaint="Worsening ascites, sarcopenia.",
        history="Hepatitis C related. Compensated cirrhosis until 3 months ago.",
        patient=p,
        learning_objectives=[
            LearningObjective("LO1", "Tailor protein to 1.2-1.5 g/kg without precipitating HE"),
            LearningObjective("LO2", "Restrict sodium to 1.5 g/day"),
            LearningObjective("LO3", "Add late-evening snack to reduce muscle catabolism"),
        ],
        reference_solution=CaseSolution(
            summary="2200 kcal, 95 g protein, < 1500 mg Na, late snack 200 kcal.",
            prescribed_diet=low_sodium_renal_diet(daily_energy_kcal=2200),
            rationale="Supports muscle mass while managing ascites.",
        ),
        difficulty="advanced",
        tags=["hepatology", "complex"],
    )


def _case_ibs_low_fodmap() -> CaseStudy:
    p = Patient(
        demographics=Demographics(age=29, sex=Sex.FEMALE),
        anthropometrics=Anthropometrics(height_cm=170, weight_kg=63),
        lifestyle=Lifestyle(),
    )
    p.add_disease(IBS(subtype="mixed"))
    return CaseStudy(
        case_id="C09",
        title="29 y F with IBS-M unresponsive to fibre changes",
        chief_complaint="Daily bloating, alternating BMs for 2 years.",
        history="Diet attempts: gluten-free (partial relief), dairy-free (no effect).",
        patient=p,
        learning_objectives=[
            LearningObjective("LO1", "Structured low-FODMAP elimination"),
            LearningObjective("LO2", "Plan systematic reintroduction"),
            LearningObjective("LO3", "Maintain nutritional adequacy"),
        ],
        reference_solution=CaseSolution(
            summary="4-6 wk elimination then re-introduction of one FODMAP/week.",
            prescribed_diet=low_fodmap_diet(daily_energy_kcal=2000),
            rationale="Best-evidence dietary therapy for IBS.",
        ),
        tags=["gastrointestinal"],
    )


def _case_osteoporosis_geriatric() -> CaseStudy:
    p = Patient(
        demographics=Demographics(age=74, sex=Sex.FEMALE),
        anthropometrics=Anthropometrics(height_cm=158, weight_kg=52),
        lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT),
        biomarkers=Biomarkers(values={
            "vitamin_d_25oh_ng_ml": 16, "calcium_mg_dl": 8.7,
        }),
    )
    p.add_disease(Osteoporosis())
    p.add_disease(Sarcopenia())
    p.add_medication(get_medication("alendronate"))
    return CaseStudy(
        case_id="C10",
        title="74 y F with osteoporosis, sarcopenia, on alendronate",
        chief_complaint="Recent vertebral fracture; concerned about further falls.",
        history="Lives alone, limited cooking. Vegetarian by preference.",
        patient=p,
        learning_objectives=[
            LearningObjective("LO1", "Plan 1200 mg Ca + 800-1000 IU vitamin D"),
            LearningObjective("LO2", "Target ≥ 1.2 g/kg protein for sarcopenia"),
            LearningObjective("LO3", "Time alendronate properly (fasting, no Ca for 30 min)"),
        ],
        reference_solution=CaseSolution(
            summary="Protein-forward Mediterranean pattern + Ca/Vit D + alendronate timing.",
            prescribed_diet=mediterranean_diet(daily_energy_kcal=1700),
            rationale="Supports bone matrix and muscle mass.",
        ),
        tags=["geriatric", "musculoskeletal"],
    )


def _case_hyperthyroid_pre_treatment() -> CaseStudy:
    p = Patient(
        demographics=Demographics(age=34, sex=Sex.FEMALE),
        anthropometrics=Anthropometrics(height_cm=167, weight_kg=54),
        lifestyle=Lifestyle(activity_level=ActivityLevel.MODERATE),
        biomarkers=Biomarkers(values={"tsh_uIU_ml": 0.05, "free_t4_ng_dl": 2.8}),
    )
    p.add_disease(Hyperthyroidism(severity="moderate"))
    return CaseStudy(
        case_id="C11",
        title="34 y F with Graves' disease, unexplained weight loss",
        chief_complaint="6 kg loss in 3 months despite increased intake.",
        history="Awaiting antithyroid drug initiation.",
        patient=p,
        learning_objectives=[
            LearningObjective("LO1", "Increase energy intake +20% to match hypermetabolism"),
            LearningObjective("LO2", "Caution on iodine-rich foods pre-treatment"),
            LearningObjective("LO3", "Protect bone health (Ca/Vit D)"),
        ],
        reference_solution=CaseSolution(
            summary="2700 kcal high-protein diet; limit excess iodine.",
            prescribed_diet=standard_diet(daily_energy_kcal=2700),
            rationale="Compensate for hypermetabolic state.",
        ),
        tags=["endocrine"],
    )


def _case_hypothyroid_weight_gain() -> CaseStudy:
    p = Patient(
        demographics=Demographics(age=48, sex=Sex.FEMALE),
        anthropometrics=Anthropometrics(height_cm=161, weight_kg=82),
        lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT),
        biomarkers=Biomarkers(values={"tsh_uIU_ml": 12.0, "ldl_mg_dl": 142}),
    )
    p.add_disease(Hypothyroidism(severity="moderate"))
    p.add_medication(get_medication("levothyroxine"))
    return CaseStudy(
        case_id="C12",
        title="48 y F on levothyroxine, slow weight loss",
        chief_complaint="Plateaued despite 1500 kcal diet.",
        history="Diagnosed 5 years ago. Compliant with medication.",
        patient=p,
        learning_objectives=[
            LearningObjective("LO1", "Counsel on levothyroxine timing vs Ca/Fe"),
            LearningObjective("LO2", "Set realistic weight-loss target"),
            LearningObjective("LO3", "Promote fibre and selenium-rich foods"),
        ],
        reference_solution=CaseSolution(
            summary="Mediterranean pattern 1400 kcal; separate Ca/Fe by 4 h from LT4.",
            prescribed_diet=mediterranean_diet(daily_energy_kcal=1400),
            rationale="Improves lipid profile and energy balance.",
        ),
        tags=["endocrine", "drug_food"],
    )


def _case_cancer_cachexia() -> CaseStudy:
    p = Patient(
        demographics=Demographics(age=63, sex=Sex.MALE),
        anthropometrics=Anthropometrics(height_cm=176, weight_kg=58),
        lifestyle=Lifestyle(activity_level=ActivityLevel.SEDENTARY),
        biomarkers=Biomarkers(values={"crp_mg_l": 22, "albumin_g_dl": 2.9}),
    )
    p.add_disease(CancerCachexia())
    p.add_medication(get_medication("prednisone"))
    return CaseStudy(
        case_id="C13",
        title="63 y M with stage III pancreatic cancer, cachexia",
        chief_complaint="15 kg loss in 4 months; anorexia.",
        history="On chemotherapy; severe taste changes.",
        patient=p,
        learning_objectives=[
            LearningObjective("LO1", "Provide 30-35 kcal/kg/day, ≥ 1.5 g/kg protein"),
            LearningObjective("LO2", "Address taste changes with high-density meals"),
            LearningObjective("LO3", "Manage steroid-induced glucose intolerance"),
        ],
        reference_solution=CaseSolution(
            summary="Energy-dense small meals + ONS; EPA 2 g/day.",
            prescribed_diet=standard_diet(daily_energy_kcal=2200),
            rationale="Slows muscle loss; improves quality of life.",
        ),
        difficulty="advanced",
        tags=["oncology", "palliative"],
    )


def _case_gout_metabolic() -> CaseStudy:
    p = Patient(
        demographics=Demographics(age=52, sex=Sex.MALE),
        anthropometrics=Anthropometrics(height_cm=178, weight_kg=104),
        lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT,
                            alcohol_units_per_week=14),
        biomarkers=Biomarkers(values={"uric_acid_mg_dl": 9.1, "ldl_mg_dl": 168}),
    )
    p.add_disease(Gout())
    p.add_disease(Dyslipidemia(severity="moderate"))
    return CaseStudy(
        case_id="C14",
        title="52 y M with recurrent gout flares and metabolic syndrome",
        chief_complaint="Third flare this year; right great toe.",
        history="Drinks 2 beers/day. Loves seafood. Sedentary office job.",
        patient=p,
        learning_objectives=[
            LearningObjective("LO1", "Limit organ meats, shellfish, beer"),
            LearningObjective("LO2", "Encourage low-fat dairy, cherries, water > 2 L/day"),
            LearningObjective("LO3", "Address overall metabolic risk"),
        ],
        reference_solution=CaseSolution(
            summary="DASH-flavoured diet, alcohol < 7 units/week, target 5 kg loss.",
            prescribed_diet=dash_diet(daily_energy_kcal=1800),
            rationale="Reduces urate and CV risk simultaneously.",
        ),
        tags=["rheumatologic", "metabolic"],
    )


def _case_vegan_pregnancy() -> CaseStudy:
    p = Patient(
        demographics=Demographics(age=31, sex=Sex.FEMALE, pregnancy_trimester=3),
        anthropometrics=Anthropometrics(height_cm=168, weight_kg=72),
        lifestyle=Lifestyle(activity_level=ActivityLevel.LIGHT,
                            dietary_preferences=["vegan"]),
        biomarkers=Biomarkers(values={"vitamin_b12_pg_ml": 220, "ferritin_ng_ml": 18}),
    )
    return CaseStudy(
        case_id="C15",
        title="31 y F vegan, 32 wk pregnancy, mild anemia",
        chief_complaint="Routine prenatal nutrition review.",
        history=(
            "Vegan for 8 years. Concerned about B12 and iron. Wants to continue "
            "vegan diet through breastfeeding."
        ),
        patient=p,
        learning_objectives=[
            LearningObjective("LO1", "Ensure B12, iron, omega-3, choline adequacy"),
            LearningObjective("LO2", "Plan calorie + protein increase for 3rd trimester"),
            LearningObjective("LO3", "Continuity into lactation"),
        ],
        reference_solution=CaseSolution(
            summary="2400 kcal vegan diet + B12 + iron + DHA + choline supplements.",
            prescribed_diet=vegan_diet(daily_energy_kcal=2400),
            rationale="Maintains patient preferences while meeting prenatal needs.",
        ),
        tags=["pregnancy", "vegan"],
    )


_CASE_BUILDERS: Dict[str, Callable[[], CaseStudy]] = {
    "t2dm_ht_dyslipidemia": _case_t2dm_ht_dyslip,
    "celiac_teen": _case_celiac_teen,
    "ckd4_pre_dialysis": _case_ckd4_dialysis,
    "gestational_dm": _case_gestational_dm,
    "obesity_iii_pre_bariatric": _case_obesity_class_iii_pre_bariatric,
    "anorexia_refeeding": _case_anorexia_refeeding,
    "pcos_insulin_resistance": _case_pcos,
    "cirrhosis_ascites": _case_cirrhosis_ascites,
    "ibs_low_fodmap": _case_ibs_low_fodmap,
    "osteoporosis_geriatric": _case_osteoporosis_geriatric,
    "hyperthyroid": _case_hyperthyroid_pre_treatment,
    "hypothyroid_weight_gain": _case_hypothyroid_weight_gain,
    "cancer_cachexia": _case_cancer_cachexia,
    "gout_metabolic": _case_gout_metabolic,
    "vegan_pregnancy": _case_vegan_pregnancy,
}


def built_in_cases() -> List[CaseStudy]:
    """Return a fresh list of all built-in case studies."""
    return [builder() for builder in _CASE_BUILDERS.values()]


def get_case(case_key: str) -> CaseStudy:
    """Look up one case by its registry key (e.g. ``"t2dm_ht_dyslipidemia"``)."""
    try:
        return _CASE_BUILDERS[case_key]()
    except KeyError as exc:
        raise KeyError(
            f"unknown case {case_key!r}. Available: {sorted(_CASE_BUILDERS)}"
        ) from exc


def list_cases() -> List[str]:
    """Return the registry keys of all built-in cases."""
    return sorted(_CASE_BUILDERS)
