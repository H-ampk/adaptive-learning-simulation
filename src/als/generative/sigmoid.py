"""Numerically stable logistic sigmoid.

docs/generative-learner.md uses sigmoid both for competence K = sigmoid(a)
and inside the candidate response model.
"""

from __future__ import annotations

import math


def sigmoid(x: float) -> float:
    """Return 1 / (1 + exp(-x)) without overflow for large |x|."""
    if x >= 0.0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)
