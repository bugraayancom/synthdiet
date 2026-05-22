"""Behavioural modelling: adherence and dropout dynamics.

These models govern how closely a synthetic patient follows a prescribed diet
over time. They are designed to plug directly into
:class:`~synthdiet.simulation.DietSimulator` and the RCT engine in
:mod:`synthdiet.trials` for realistic trial simulations.
"""

from synthdiet.behavior.adherence import (
    AdherenceModel,
    ConstantAdherence,
    DecayingAdherence,
    PerceivedBurdenAdherence,
    StochasticSkipAdherence,
    WeibullDropoutAdherence,
)

__all__ = [
    "AdherenceModel",
    "ConstantAdherence",
    "DecayingAdherence",
    "PerceivedBurdenAdherence",
    "StochasticSkipAdherence",
    "WeibullDropoutAdherence",
]
