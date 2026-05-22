"""Internal helper to load matplotlib lazily and give a friendly error."""

from __future__ import annotations


def get_matplotlib():
    try:
        import matplotlib.pyplot as plt  # noqa: F401
        return plt
    except ImportError as exc:
        raise ImportError(
            "matplotlib is required for the synthdiet.viz subpackage. "
            "Install with: pip install 'synthdiet[viz]'"
        ) from exc
