"""Visualisation utilities (matplotlib is an optional dependency).

Install matplotlib via ``pip install synthdiet[viz]`` to enable these helpers.
Without matplotlib installed, the imports below will raise a clear error only
when a plotting function is called.
"""

from synthdiet.viz.consort import consort_diagram
from synthdiet.viz.forest import forest_plot
from synthdiet.viz.table1 import describe_cohort, table1
from synthdiet.viz.trajectories import trajectory_plot

__all__ = [
    "consort_diagram",
    "describe_cohort",
    "forest_plot",
    "table1",
    "trajectory_plot",
]
