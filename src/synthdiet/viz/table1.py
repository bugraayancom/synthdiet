"""Table 1: cohort descriptive statistics."""

from __future__ import annotations

from typing import Iterable, Optional, Sequence

import numpy as np
import pandas as pd

from synthdiet.patients.patient import Patient


def describe_cohort(patients: Sequence[Patient]) -> pd.DataFrame:
    """Return a tidy DataFrame of per-patient features for analysis."""
    rows = []
    for p in patients:
        row = {
            "age": p.demographics.age,
            "sex": p.demographics.sex.value,
            "height_cm": p.anthropometrics.height_cm,
            "weight_kg": p.anthropometrics.weight_kg,
            "bmi": p.anthropometrics.bmi,
            "bmi_category": p.anthropometrics.bmi_category,
            "activity_level": p.lifestyle.activity_level.value,
            "n_diseases": len(p.diseases),
            "n_medications": len(p.medications),
        }
        for k, v in p.biomarkers.values.items():
            row[k] = v
        rows.append(row)
    return pd.DataFrame(rows)


def table1(
    patients: Sequence[Patient],
    *,
    group_by: Optional[str] = None,
    continuous_vars: Optional[Iterable[str]] = None,
    categorical_vars: Optional[Iterable[str]] = None,
) -> pd.DataFrame:
    """Render a publication-style Table 1.

    Continuous variables are summarised as mean (SD); categorical variables as
    n (%). If ``group_by`` is given, the table is split into columns per
    group level.
    """
    df = describe_cohort(patients)
    cont = list(continuous_vars or ["age", "height_cm", "weight_kg", "bmi"])
    cat = list(categorical_vars or ["sex", "bmi_category", "activity_level"])

    if group_by is None:
        groups = {"overall": df}
    else:
        groups = {str(k): v for k, v in df.groupby(group_by)}

    rows = []
    for var in cont:
        row = {"variable": f"{var} (mean (SD))"}
        for g, sub in groups.items():
            values = sub[var].dropna()
            row[g] = f"{values.mean():.1f} ({values.std():.1f})"
        rows.append(row)
    for var in cat:
        for level in sorted(df[var].dropna().unique().tolist()):
            row = {"variable": f"{var} = {level}, n (%)"}
            for g, sub in groups.items():
                n = (sub[var] == level).sum()
                pct = 100.0 * n / max(len(sub), 1)
                row[g] = f"{n} ({pct:.0f}%)"
            rows.append(row)
    return pd.DataFrame(rows)
