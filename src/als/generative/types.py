"""Shared generative-learner state and item types.

Canonical latent state is ability ``a`` (real-valued). Competence
``K = sigmoid(a)`` is the probability-scale view of the same quantity
(docs/generative-learner.md, 回答モデル). Worlds that prefer to update ``K``
must map back to ``a`` before a response model that takes ``a`` is applied.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Mapping

from als.generative.sigmoid import sigmoid


def _freeze_floats(values: Mapping[str, float]) -> Mapping[str, float]:
    return MappingProxyType({key: float(value) for key, value in values.items()})


@dataclass(frozen=True, slots=True)
class LearnerParameters:
    """Swappable learner parameters. Values are not research defaults.

    ``forgetting`` is the primary forgetting parameter named in the design.
    ``forgetting_extras`` holds additional named coefficients (for example a
    power-law exponent) so later worlds can add parameters without embedding
    them in control flow here.
    """

    learning_rate: float
    forgetting: float
    guess: float
    slip: float
    forgetting_extras: Mapping[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self, "forgetting_extras", _freeze_floats(self.forgetting_extras)
        )
        if not 0.0 <= self.guess <= 1.0:
            raise ValueError("guess must be in [0, 1]")
        if not 0.0 <= self.slip <= 1.0:
            raise ValueError("slip must be in [0, 1]")
        if self.guess + self.slip > 1.0:
            raise ValueError("guess + slip must be <= 1")


@dataclass(frozen=True, slots=True)
class ConceptState:
    """Latent state of one learner on one concept.

    States for different concepts are separate objects. Nothing in this type
    pools knowledge across concepts.
    """

    learner_id: str
    concept_id: str
    ability: float
    parameters: LearnerParameters
    time: float

    @property
    def competence(self) -> float:
        """K = sigmoid(a). Derived; ``ability`` is the stored state."""
        return sigmoid(self.ability)

    def with_ability(self, ability: float, *, time: float | None = None) -> ConceptState:
        return ConceptState(
            learner_id=self.learner_id,
            concept_id=self.concept_id,
            ability=ability,
            parameters=self.parameters,
            time=self.time if time is None else time,
        )

    def with_time(self, time: float) -> ConceptState:
        return self.with_ability(self.ability, time=time)

    def with_parameters(self, parameters: LearnerParameters) -> ConceptState:
        return ConceptState(
            learner_id=self.learner_id,
            concept_id=self.concept_id,
            ability=self.ability,
            parameters=parameters,
            time=self.time,
        )


@dataclass(frozen=True, slots=True)
class Item:
    """Item presented to a learner. Only id, concept, and difficulty for now."""

    item_id: str
    concept_id: str
    difficulty: float
