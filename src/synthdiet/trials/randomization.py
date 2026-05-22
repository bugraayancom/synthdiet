"""Randomisation strategies for RCT arm assignment."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Callable, Dict, List, Optional, Sequence

import numpy as np

from synthdiet.patients.patient import Patient
from synthdiet.utils.random_state import RandomState, as_random_state


def simple_randomization(
    patients: Sequence[Patient],
    arms: Sequence[str],
    *,
    weights: Optional[Sequence[float]] = None,
    seed: RandomState = None,
) -> Dict[str, str]:
    """Assign each patient to an arm by independent Bernoulli draw."""
    rng = as_random_state(seed)
    probs = None
    if weights is not None:
        total = float(sum(weights))
        probs = [w / total for w in weights]
    arm_list = list(arms)
    assignments: Dict[str, str] = {}
    for p in patients:
        arm = str(rng.choice(arm_list, p=probs))
        assignments[p.patient_id] = arm
    return assignments


def block_randomization(
    patients: Sequence[Patient],
    arms: Sequence[str],
    *,
    block_size: Optional[int] = None,
    seed: RandomState = None,
) -> Dict[str, str]:
    """Permuted-block randomisation; guarantees balance within each block."""
    rng = as_random_state(seed)
    arm_list = list(arms)
    if block_size is None:
        block_size = len(arm_list) * 2
    if block_size % len(arm_list) != 0:
        raise ValueError("block_size must be a multiple of the number of arms")
    per_arm = block_size // len(arm_list)
    assignments: Dict[str, str] = {}
    idx = 0
    while idx < len(patients):
        block = arm_list * per_arm
        rng.shuffle(block)
        for j in range(min(block_size, len(patients) - idx)):
            assignments[patients[idx + j].patient_id] = block[j]
        idx += block_size
    return assignments


def stratified_randomization(
    patients: Sequence[Patient],
    arms: Sequence[str],
    *,
    strata: Sequence[Callable[[Patient], object]],
    block_size: Optional[int] = None,
    seed: RandomState = None,
) -> Dict[str, str]:
    """Randomise within strata defined by one or more keying functions.

    ``strata`` is a sequence of callables that return the stratification key
    for a patient (e.g. ``lambda p: p.sex``). All callables are evaluated and
    combined into a tuple key.
    """
    rng = as_random_state(seed)
    buckets: Dict[tuple, List[Patient]] = defaultdict(list)
    for p in patients:
        key = tuple(fn(p) for fn in strata)
        buckets[key].append(p)
    assignments: Dict[str, str] = {}
    for bucket in buckets.values():
        sub_seed = int(rng.integers(0, 1 << 32))
        assignments.update(
            block_randomization(bucket, arms, block_size=block_size, seed=sub_seed)
        )
    return assignments


def minimization(
    patients: Sequence[Patient],
    arms: Sequence[str],
    *,
    factors: Sequence[Callable[[Patient], object]],
    seed: RandomState = None,
    bias_probability: float = 0.8,
) -> Dict[str, str]:
    """Pocock-Simon minimisation: each new patient is assigned to the arm
    minimising the post-assignment imbalance across the supplied factors.

    With probability ``bias_probability`` the optimal arm is chosen;
    otherwise a uniform random arm is chosen (introducing residual
    randomness to defeat investigator prediction).
    """
    rng = as_random_state(seed)
    arm_list = list(arms)
    counts: Dict[str, Dict[tuple, Counter]] = {
        arm: defaultdict(Counter) for arm in arm_list
    }
    assignments: Dict[str, str] = {}
    for p in patients:
        factor_values = [(i, fn(p)) for i, fn in enumerate(factors)]
        imbalances = {}
        for arm in arm_list:
            score = 0
            for idx, value in factor_values:
                # Imagine assigning p to ``arm`` and measure the max - min
                hypothetical = dict(counts[arm][idx])
                hypothetical[value] = hypothetical.get(value, 0) + 1
                # Compare against the other arms' current counts for this value
                other_counts = [
                    counts[other][idx].get(value, 0) for other in arm_list if other != arm
                ]
                imbalance = max([hypothetical[value]] + other_counts) - min(
                    [hypothetical[value]] + other_counts
                )
                score += imbalance
            imbalances[arm] = score
        min_score = min(imbalances.values())
        best = [a for a, s in imbalances.items() if s == min_score]
        if rng.random() < bias_probability:
            arm = str(rng.choice(best))
        else:
            arm = str(rng.choice(arm_list))
        assignments[p.patient_id] = arm
        for idx, value in factor_values:
            counts[arm][idx][value] += 1
    return assignments
