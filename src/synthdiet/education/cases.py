"""Core data classes for clinical case studies."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from synthdiet.diets.base import DietPlan
from synthdiet.patients.patient import Patient


@dataclass
class LearningObjective:
    """One discrete learning objective tied to a case."""

    code: str
    description: str
    competency_area: str = "general"


@dataclass
class CaseSolution:
    """A reference solution to a case study."""

    summary: str
    prescribed_diet: DietPlan
    rationale: str
    follow_up_weeks: int = 12
    expected_outcomes: List[str] = field(default_factory=list)


@dataclass
class CaseStudy:
    """A complete clinical vignette suitable for classroom or self-study."""

    case_id: str
    title: str
    chief_complaint: str
    history: str
    patient: Patient
    learning_objectives: List[LearningObjective] = field(default_factory=list)
    reference_solution: Optional[CaseSolution] = None
    difficulty: str = "intermediate"  # "introductory", "intermediate", "advanced"
    estimated_minutes: int = 30
    tags: List[str] = field(default_factory=list)

    def as_markdown(self) -> str:
        diseases = ", ".join(self.patient.disease_names()) or "no diagnoses recorded"
        meds = ", ".join(self.patient.medication_names()) or "no medications"
        objectives = "\n".join(
            f"- ({lo.code}) {lo.description}" for lo in self.learning_objectives
        ) or "*(no formal learning objectives)*"
        biomarker_lines = "\n".join(
            f"  - {k}: {v}" for k, v in sorted(self.patient.biomarkers.values.items())
        ) or "  *(no labs recorded)*"

        return (
            f"# Case {self.case_id}: {self.title}\n\n"
            f"**Difficulty:** {self.difficulty}  |  "
            f"**Estimated time:** {self.estimated_minutes} min\n\n"
            f"## Chief complaint\n{self.chief_complaint}\n\n"
            f"## History\n{self.history}\n\n"
            f"## Patient profile\n"
            f"- Age: {self.patient.demographics.age}\n"
            f"- Sex: {self.patient.demographics.sex.value}\n"
            f"- Height: {self.patient.anthropometrics.height_cm} cm\n"
            f"- Weight: {self.patient.anthropometrics.weight_kg} kg\n"
            f"- BMI: {self.patient.anthropometrics.bmi:.1f} "
            f"({self.patient.anthropometrics.bmi_category})\n"
            f"- Diagnoses: {diseases}\n"
            f"- Medications: {meds}\n\n"
            f"## Labs\n{biomarker_lines}\n\n"
            f"## Learning objectives\n{objectives}\n"
        )

    def as_html(self) -> str:
        import html
        md = self.as_markdown()
        # Very lightweight Markdown -> HTML, enough for printing.
        lines = []
        for line in md.splitlines():
            stripped = line.lstrip("#")
            n_hashes = len(line) - len(stripped)
            if n_hashes:
                lines.append(f"<h{n_hashes}>{html.escape(stripped.strip())}</h{n_hashes}>")
            elif line.startswith("- "):
                lines.append(f"<li>{html.escape(line[2:])}</li>")
            elif line.strip():
                lines.append(f"<p>{html.escape(line)}</p>")
        return "<html><body>" + "\n".join(lines) + "</body></html>"
