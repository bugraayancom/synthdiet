---
title: 'synthdiet: A Python library for generating synthetic patients and simulating dietary interventions'
tags:
  - Python
  - dietetics
  - nutrition
  - synthetic patients
  - randomised controlled trials
  - clinical simulation
authors:
  - name: Buğra Ayan
    orcid: 0000-0000-0000-0000
    corresponding: true
    affiliation: 1
affiliations:
  - name: Independent Researcher, Ankara, Türkiye
    index: 1
date: 21 May 2026
bibliography: paper.bib
---

# Summary

`synthdiet` is a Python library that generates fully synthetic patients with
realistic clinical conditions and simulates dietary interventions on them.
The package targets two audiences: methodologists who want to prototype
randomised controlled trial (RCT) designs before recruiting real participants,
and dietetics educators who want a deep stock of clinically realistic case
studies for teaching and assessment.

Twenty-five built-in diseases — covering endocrine, cardiovascular, renal,
hepatic, gastrointestinal, metabolic, musculoskeletal, oncologic, and
psychiatric conditions — each expose nutritional constraints and biomarker
modifiers. Five patient generators (uniform, distribution-based,
Gaussian-copula correlated, cohort-with-prevalences, and Markov disease
progression) let users tune the realism vs. simplicity trade-off. A dynamic
body-composition model based on @hall2011 underpins the diet simulator;
a parallel-arm, crossover, and factorial RCT engine supports
intention-to-treat, per-protocol, and as-treated analyses, with adherence and
Weibull dropout modelling included by default.

To support causal-inference research, `synthdiet` ships counterfactual
simulation, average-treatment-effect estimators, conditional ATE by subgroup,
inverse-probability-of-treatment weighting, and a lightweight directed
acyclic graph representation. Six published diet-quality indices
(HEI-2020, AHEI-2010, MEDAS, DASH, PHDI, DII) score any plan on a common
interface, and a registry of nineteen clinically important drug-nutrient
interactions captures effects such as metformin-induced B12 depletion or
warfarin-vitamin K interaction.

# Statement of need

Dietetics research has long suffered from a tension between the desire for
large, well-powered trials and the cost of running them. Synthetic data offers
an attractive complement: it is reproducible, allows arbitrary cohort
composition, and exposes the *true* data-generating process — a precondition
for teaching causal inference rigorously.

Existing synthetic patient frameworks such as Synthea [@synthea2018] target
electronic health record (EHR) data and care pathways, not nutritional
interventions; mechanistic body-weight simulators such as the NIH Body Weight
Planner [@hall2011] model a single patient and a single diet without
trial-level abstractions. There is, to our knowledge, no integrated Python
toolbox for this niche.

`synthdiet` fills that gap by combining a flexible patient model, a published
body-weight equation, a full RCT engine, statistical inference helpers
(power analysis, bootstrap, ANCOVA, FDR adjustment), and educational tooling
(15 clinical case studies + OSCE rubric). It is fully tested, fully typed,
and small enough to be auditable line by line.

# Validation

The library ships a regression-style validation suite that reproduces the
qualitative effects of five landmark dietary RCTs: DASH-Sodium [@sacks2001],
PREDIMED [@estruch2018], DiRECT [@lean2018], Look AHEAD [@lookahead2007], and
the Diabetes Prevention Program [@dpp2002]. Effect *direction* is asserted
in CI; effect *magnitude* tolerance bands serve as soft regression alarms.

# Acknowledgements

The author thanks the open-source nutrition-research community for making the
key reference datasets publicly available.

# References
