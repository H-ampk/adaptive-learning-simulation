"""Exchangeable response generators.

The logistic guess/slip form is the leading candidate in
docs/generative-learner.md. It is one ResponseModel, not a fixed research model.
"""

from __future__ import annotations

from typing import Protocol

from als.generative.sigmoid import sigmoid
from als.generative.types import ConceptState, Item


def clamp_probability(probability: float) -> float:
    if probability < 0.0 or probability > 1.0:
        raise ValueError(f"response probability {probability} is outside [0, 1]")
    return probability


class ResponseModel(Protocol):
    """P(correct | latent ability, item). Independent of any world dynamics."""

    def probability(self, state: ConceptState, item: Item) -> float:
        """Return a probability in [0, 1]."""


class LogisticGuessSlipResponse:
    """P(correct) = G + (1 - G - S) * sigmoid(a - d)."""

    def probability(self, state: ConceptState, item: Item) -> float:
        guess = state.parameters.guess
        slip = state.parameters.slip
        latent = sigmoid(state.ability - item.difficulty)
        return clamp_probability(guess + (1.0 - guess - slip) * latent)
