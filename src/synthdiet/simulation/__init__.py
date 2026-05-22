"""Diet simulation engine."""

from synthdiet.simulation.engine import DietSimulator, SimulationResult, TimePoint
from synthdiet.simulation.hall_model import (
    HallSimulation,
    HallSimulationParameters,
    HallState,
    estimate_baseline_intake,
    forbes_partition,
    initialise_body_composition,
    project_weight_change,
)
from synthdiet.simulation.metabolism import (
    basal_metabolic_rate,
    harris_benedict,
    mifflin_st_jeor,
    total_daily_energy_expenditure,
)

__all__ = [
    "DietSimulator",
    "HallSimulation",
    "HallSimulationParameters",
    "HallState",
    "SimulationResult",
    "TimePoint",
    "basal_metabolic_rate",
    "estimate_baseline_intake",
    "forbes_partition",
    "harris_benedict",
    "initialise_body_composition",
    "mifflin_st_jeor",
    "project_weight_change",
    "total_daily_energy_expenditure",
]
