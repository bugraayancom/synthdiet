"""Random-state helpers.

The library accepts ``int``, :class:`numpy.random.Generator`, or ``None`` wherever
randomness is required. :func:`as_random_state` normalises all of these to a
fresh :class:`numpy.random.Generator` instance for reproducibility.
"""

from __future__ import annotations

from typing import Union

import numpy as np

RandomState = Union[int, np.random.Generator, None]


def as_random_state(seed: RandomState) -> np.random.Generator:
    """Return a NumPy ``Generator`` from any supported seed type."""
    if isinstance(seed, np.random.Generator):
        return seed
    return np.random.default_rng(seed)
