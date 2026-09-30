"""World interface shared by later World A, B-E, B-P, and C implementations.

A world owns time passage, forgetting, practice-driven learning gain, and how
those steps are composed into a learner-state update. Response probability is
delegated to an exchangeable ResponseModel so the observation model can change
without copying world dynamics.

This module does not implement BKT, PFA, HLR, policies, or a concrete world
formula. World C in particular stays unspecified until a separate design note
fixes its state variables.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from als.generative.response import ResponseModel
from als.generative.rng import SeededRng
from als.generative.types import ConceptState, Item


class GenerativeWorld(Protocol):
    """Replaceable generative world.

    Implementations must keep concept states independent: an update for one
    ``concept_id`` must not rewrite another concept's state.
    """

    name: str

    def advance_time(self, state: ConceptState, delta: float) -> ConceptState:
        """Move the state's clock forward by ``delta`` without changing ability."""

    def apply_forgetting(self, state: ConceptState, delta: float) -> ConceptState:
        """Apply this world's forgetting rule over an elapsed interval ``delta``."""

    def apply_learning(self, state: ConceptState, item: Item) -> ConceptState:
        """Apply learning gain from a practice opportunity.

        The observed correctness is not an input. See
        docs/generative-learner.md, 学習増分.
        """

    def response_probability(self, state: ConceptState, item: Item) -> float:
        """P(correct) under this world's response model."""

    def update_state(
        self, state: ConceptState, item: Item, delta: float
    ) -> ConceptState:
        """Compose time, forgetting, and learning for one practice opportunity."""


@dataclass(frozen=True, slots=True)
class PracticeUpdate:
    """One practice opportunity and the response drawn from the pre-update state.

    Learning uses the state after the world's own ``update_state``. The boolean
    response is recorded from the state *before* that update, so correctness
    does not feed the gain unless a future sensitivity-analysis world says so.
    """

    before: ConceptState
    after: ConceptState
    item: Item
    probability: float
    correct: bool


def draw_response(
    world: GenerativeWorld,
    state: ConceptState,
    item: Item,
    rng: SeededRng,
) -> tuple[bool, float]:
    """Sample a response. Does not change learner state."""
    probability = world.response_probability(state, item)
    return rng.bernoulli(probability), probability


def practice_opportunity(
    world: GenerativeWorld,
    state: ConceptState,
    item: Item,
    delta: float,
    rng: SeededRng,
) -> PracticeUpdate:
    """Observe, then let the world update state. Order is fixed at this boundary.

    Worlds still choose how ``update_state`` orders forgetting and learning.
    """
    correct, probability = draw_response(world, state, item, rng)
    after = world.update_state(state, item, delta)
    return PracticeUpdate(
        before=state,
        after=after,
        item=item,
        probability=probability,
        correct=correct,
    )


class ResponseDelegatingWorld:
    """Optional base for worlds that only swap dynamics and share a ResponseModel.

    Subclasses implement the three dynamic steps and may override ``update_state``
    when the composition order differs. The default composition is
    advance time, then forgetting, then learning.
    """

    def __init__(self, name: str, response_model: ResponseModel) -> None:
        self.name = name
        self._response_model = response_model

    def response_probability(self, state: ConceptState, item: Item) -> float:
        return self._response_model.probability(state, item)

    def update_state(
        self, state: ConceptState, item: Item, delta: float
    ) -> ConceptState:
        timed = self.advance_time(state, delta)
        forgotten = self.apply_forgetting(timed, delta)
        return self.apply_learning(forgotten, item)
