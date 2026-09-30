"""Tests for the generative-learner foundation. No concrete world formulas."""

from __future__ import annotations

import math

import pytest

from als.generative.response import LogisticGuessSlipResponse, clamp_probability
from als.generative.rng import SeededRng
from als.generative.sigmoid import sigmoid
from als.generative.types import ConceptState, Item, LearnerParameters
from als.generative.world import (
    ResponseDelegatingWorld,
    draw_response,
    practice_opportunity,
)


def _parameters(**overrides: float) -> LearnerParameters:
    values = {
        "learning_rate": 0.2,
        "forgetting": 0.01,
        "guess": 0.1,
        "slip": 0.05,
    }
    values.update(overrides)
    return LearnerParameters(
        learning_rate=values["learning_rate"],
        forgetting=values["forgetting"],
        guess=values["guess"],
        slip=values["slip"],
    )


def _state(concept_id: str = "c1", ability: float = 0.0) -> ConceptState:
    return ConceptState(
        learner_id="u1",
        concept_id=concept_id,
        ability=ability,
        parameters=_parameters(),
        time=0.0,
    )


def _item(concept_id: str = "c1", difficulty: float = 0.0) -> Item:
    return Item(item_id=f"q-{concept_id}", concept_id=concept_id, difficulty=difficulty)


class ShiftAbilityWorld(ResponseDelegatingWorld):
    """Test double: learning adds a constant; forgetting subtracts another."""

    def __init__(self, name: str, learning_shift: float, forgetting_shift: float) -> None:
        super().__init__(name, LogisticGuessSlipResponse())
        self.learning_shift = learning_shift
        self.forgetting_shift = forgetting_shift

    def advance_time(self, state: ConceptState, delta: float) -> ConceptState:
        return state.with_time(state.time + delta)

    def apply_forgetting(self, state: ConceptState, delta: float) -> ConceptState:
        return state.with_ability(state.ability - self.forgetting_shift * delta)

    def apply_learning(self, state: ConceptState, item: Item) -> ConceptState:
        return state.with_ability(state.ability + self.learning_shift)


class TestSigmoid:
    @pytest.mark.parametrize(
        ("x", "expected"),
        [
            (0.0, 0.5),
            (math.log(3), 0.75),
            (-math.log(3), 0.25),
        ],
    )
    def test_known_values(self, x: float, expected: float) -> None:
        assert sigmoid(x) == pytest.approx(expected)

    def test_large_magnitudes_stay_in_unit_interval(self) -> None:
        assert 0.0 < sigmoid(-40.0) < 1e-9
        assert math.isclose(sigmoid(40.0), 1.0)


class TestResponseProbability:
    def test_probability_stays_inside_unit_interval(self) -> None:
        model = LogisticGuessSlipResponse()
        state = _state(ability=50.0)
        hard = _item(difficulty=-50.0)
        easy = _item(difficulty=50.0)
        for item in (hard, easy, _item(difficulty=0.0)):
            probability = model.probability(state, item)
            assert 0.0 <= probability <= 1.0
            clamp_probability(probability)

    def test_guess_and_slip_bound_the_probability(self) -> None:
        guess = 0.2
        slip = 0.3
        state = ConceptState(
            learner_id="u1",
            concept_id="c1",
            ability=0.0,
            parameters=_parameters(guess=guess, slip=slip),
            time=0.0,
        )
        model = LogisticGuessSlipResponse()
        high = model.probability(state.with_ability(80.0), _item())
        low = model.probability(state.with_ability(-80.0), _item())
        assert high == pytest.approx(1.0 - slip)
        assert low == pytest.approx(guess)

    def test_midpoint_matches_candidate_formula(self) -> None:
        state = _state(ability=1.5)
        item = _item(difficulty=0.5)
        probability = LogisticGuessSlipResponse().probability(state, item)
        expected = 0.1 + (1.0 - 0.1 - 0.05) * sigmoid(1.0)
        assert probability == pytest.approx(expected)

    def test_rejects_guess_plus_slip_above_one(self) -> None:
        with pytest.raises(ValueError):
            _parameters(guess=0.6, slip=0.6)


class TestSeededRng:
    def test_same_seed_reproduces_response_sequence(self) -> None:
        world = ShiftAbilityWorld("shift-a", learning_shift=0.0, forgetting_shift=0.0)
        state = _state(ability=-0.2)
        item = _item(difficulty=0.4)

        def sequence(seed: int) -> list[bool]:
            rng = SeededRng(seed)
            return [draw_response(world, state, item, rng)[0] for _ in range(12)]

        assert sequence(7) == sequence(7)
        assert sequence(7) != sequence(8)

    def test_fork_does_not_consume_parent_draws(self) -> None:
        parent = SeededRng(3)
        first = parent.random()
        child = parent.fork("learner-u1")
        second = parent.random()
        again = SeededRng(3)
        assert again.random() == first
        again.fork("ignored")
        assert again.random() == second
        assert child.random() == SeededRng(3).fork("learner-u1").random()


class TestWorldExchange:
    def test_swapping_worlds_changes_the_state_update(self) -> None:
        state = _state(ability=1.0)
        item = _item()
        learning_only = ShiftAbilityWorld("learning", learning_shift=0.4, forgetting_shift=0.0)
        with_forgetting = ShiftAbilityWorld(
            "forgetting", learning_shift=0.4, forgetting_shift=0.5
        )
        learned = learning_only.update_state(state, item, delta=2.0)
        forgotten = with_forgetting.update_state(state, item, delta=2.0)
        assert learned.ability == pytest.approx(1.4)
        assert forgotten.ability == pytest.approx(1.4 - 1.0)
        assert learned.time == pytest.approx(2.0)
        assert with_forgetting.name != learning_only.name

    def test_practice_opportunity_does_not_feed_correctness_into_gain(self) -> None:
        world = ShiftAbilityWorld("shift", learning_shift=0.25, forgetting_shift=0.0)
        state = _state()
        item = _item()
        first = practice_opportunity(world, state, item, delta=1.0, rng=SeededRng(1))
        second = practice_opportunity(world, state, item, delta=1.0, rng=SeededRng(2))
        assert first.after.ability == pytest.approx(second.after.ability)
        assert first.after.ability == pytest.approx(state.ability + 0.25)


class TestConceptIndependence:
    def test_states_are_kept_per_concept(self) -> None:
        algebra = _state("algebra", ability=0.0)
        geometry = _state("geometry", ability=2.0)
        world = ShiftAbilityWorld("shift", learning_shift=1.0, forgetting_shift=0.0)
        updated = world.update_state(algebra, _item("algebra"), delta=1.0)
        assert updated.concept_id == "algebra"
        assert updated.ability == pytest.approx(1.0)
        assert geometry.ability == pytest.approx(2.0)
        assert geometry.concept_id == "geometry"
        assert updated.competence == pytest.approx(sigmoid(updated.ability))
