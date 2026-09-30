"""Seeded randomness for simulations.

Same seed and the same sequence of draws reproduce the same values.
Call order is part of the reproducibility contract.
"""

from __future__ import annotations

import random


class SeededRng:
    """Wrapper around ``random.Random`` so simulation code does not share the global RNG."""

    def __init__(self, seed: int) -> None:
        self.seed = seed
        self._rng = random.Random(seed)

    def random(self) -> float:
        """Uniform draw in [0, 1)."""
        return self._rng.random()

    def bernoulli(self, probability: float) -> bool:
        if probability < 0.0 or probability > 1.0:
            raise ValueError(f"bernoulli probability {probability} is outside [0, 1]")
        return self.random() < probability

    def fork(self, stream_id: str) -> SeededRng:
        """Independent stream derived from this seed and ``stream_id``.

        Forks do not consume draws from the parent, so creating them does not
        change the parent's sequence.
        """
        mixer = random.Random(f"{self.seed}:{stream_id}")
        return SeededRng(mixer.randrange(2**63))
