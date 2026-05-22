"""Educational tooling for dietetics students and trainers.

Includes:

* :class:`CaseStudy` — a realistic clinical vignette bundled with an example
  solution and learning objectives.
* :func:`built_in_cases` — 15 ready-to-teach case templates.
* :class:`OSCEStation` — a simple rubric-based station for OSCE-style timed
  practice; given a student's diet plan it returns scored feedback.
"""

from synthdiet.education.cases import CaseStudy, CaseSolution, LearningObjective
from synthdiet.education.osce import OSCERubric, OSCEScore, OSCEStation
from synthdiet.education.templates import built_in_cases, get_case, list_cases

__all__ = [
    "CaseSolution",
    "CaseStudy",
    "LearningObjective",
    "OSCERubric",
    "OSCEScore",
    "OSCEStation",
    "built_in_cases",
    "get_case",
    "list_cases",
]
