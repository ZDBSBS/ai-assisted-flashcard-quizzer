"""Unit tests for quiz mode strategies."""

import pytest
from unittest.mock import patch

from utils.quiz_modes import (
    QuizModeStrategy,
    SequentialStrategy,
    RandomStrategy,
    AdaptiveStrategy,
)


class TestQuizModeStrategy:
    """Test abstract base class behavior."""

    def test_quiz_mode_strategy_cannot_be_instantiated(self) -> None:
        """Verify that QuizModeStrategy cannot be instantiated."""
        with pytest.raises(TypeError):
            QuizModeStrategy()  # type: ignore[abstract]


class TestSequentialStrategy:
    """Test sequential card ordering strategy."""

    def test_sequential_strategy_preserves_order(self) -> None:
        """Verify that sequential strategy preserves original card order."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
        ]
        strategy = SequentialStrategy()
        result = strategy.order_cards(cards)

        assert result == cards
        assert [card["front"] for card in result] == ["Q1", "Q2", "Q3"]

    def test_sequential_strategy_returns_new_list(self) -> None:
        """Verify that sequential strategy returns a new list object."""
        cards = [{"front": "Q", "back": "A"}]
        strategy = SequentialStrategy()
        result = strategy.order_cards(cards)

        assert result is not cards
        assert result == cards

    def test_sequential_strategy_handles_empty_list(self) -> None:
        """Verify that sequential strategy handles empty input."""
        cards: list[dict[str, str]] = []
        strategy = SequentialStrategy()
        result = strategy.order_cards(cards)

        assert result == []
        assert result is not cards


class TestRandomStrategy:
    """Test random card ordering strategy."""

    def test_random_strategy_returns_all_original_cards(self) -> None:
        """Verify that random strategy preserves all cards."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
        ]
        strategy = RandomStrategy()
        result = strategy.order_cards(cards)

        assert len(result) == len(cards)
        assert set(tuple(card.items()) for card in result) == set(
            tuple(card.items()) for card in cards
        )

    def test_random_strategy_does_not_modify_original_list(self) -> None:
        """Verify that random strategy does not modify the original list."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
        ]
        original_copy = cards.copy()
        strategy = RandomStrategy()
        result = strategy.order_cards(cards)

        assert cards == original_copy
        assert isinstance(result, list)

    def test_random_strategy_returns_new_list(self) -> None:
        """Verify that random strategy returns a new list object."""
        cards = [{"front": "Q", "back": "A"}]
        strategy = RandomStrategy()
        result = strategy.order_cards(cards)

        assert result is not cards

    def test_random_strategy_handles_empty_list(self) -> None:
        """Verify that random strategy handles empty input."""
        cards: list[dict[str, str]] = []
        strategy = RandomStrategy()
        result = strategy.order_cards(cards)

        assert result == []
        assert result is not cards

    @patch("utils.quiz_modes.random.shuffle")
    def test_random_strategy_shuffles_deterministically(
        self, mock_shuffle
    ) -> None:
        """Verify that random strategy calls random.shuffle()."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
        ]

        # Mock shuffle to reverse the list
        def reverse_list(lst):
            lst.reverse()

        mock_shuffle.side_effect = reverse_list

        strategy = RandomStrategy()
        result = strategy.order_cards(cards)

        # Verify shuffle was called once
        mock_shuffle.assert_called_once()
        # Verify the result is reversed (what our mock does)
        assert [card["front"] for card in result] == ["Q3", "Q2", "Q1"]


class TestAdaptiveStrategy:
    """Test adaptive card ordering strategy."""

    def test_adaptive_strategy_missed_cards_appear_first(self) -> None:
        """Verify that missed cards appear before non-missed cards."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
            {"front": "Q4", "back": "A4"},
        ]
        strategy = AdaptiveStrategy({0, 2})
        result = strategy.order_cards(cards)

        # First two should be missed cards (Q1, Q3)
        assert result[0]["front"] == "Q1"
        assert result[1]["front"] == "Q3"
        # Last two should be non-missed (Q2, Q4)
        assert result[2]["front"] == "Q2"
        assert result[3]["front"] == "Q4"

    def test_adaptive_strategy_preserves_relative_order_within_groups(
        self,
    ) -> None:
        """Verify relative order within missed and non-missed groups."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
            {"front": "Q4", "back": "A4"},
        ]
        strategy = AdaptiveStrategy({0, 1})
        result = strategy.order_cards(cards)

        # Missed group: Q1, Q2 (in original order)
        assert [card["front"] for card in result[:2]] == ["Q1", "Q2"]
        # Non-missed group: Q3, Q4 (in original order)
        assert [card["front"] for card in result[2:]] == ["Q3", "Q4"]

    def test_adaptive_strategy_does_not_modify_original_list(self) -> None:
        """Verify that adaptive strategy does not modify the original list."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
        ]
        original_copy = cards.copy()
        strategy = AdaptiveStrategy({0})
        result = strategy.order_cards(cards)

        assert cards == original_copy
        assert isinstance(result, list)

    def test_adaptive_strategy_returns_new_list(self) -> None:
        """Verify that adaptive strategy returns a new list object."""
        cards = [{"front": "Q", "back": "A"}]
        strategy = AdaptiveStrategy({0})
        result = strategy.order_cards(cards)

        assert result is not cards

    def test_adaptive_strategy_empty_missed_indices_preserves_order(
        self,
    ) -> None:
        """Verify that empty missed set preserves original order."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
        ]
        strategy = AdaptiveStrategy(set())
        result = strategy.order_cards(cards)

        assert result == cards

    def test_adaptive_strategy_all_indices_missed_returns_all_first(
        self,
    ) -> None:
        """Verify that all indices missed returns cards in original order."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
        ]
        strategy = AdaptiveStrategy({0, 1, 2})
        result = strategy.order_cards(cards)

        assert result == cards

    def test_adaptive_strategy_negative_and_out_of_range_indices_ignored(
        self,
    ) -> None:
        """Verify that invalid indices have no effect."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
        ]
        # Indices: -1 (negative), 0 (valid), 10 (out of range)
        strategy = AdaptiveStrategy({-1, 0, 10})
        result = strategy.order_cards(cards)

        # Only index 0 is valid and missed, so Q1 should appear first
        assert result[0]["front"] == "Q1"
        assert [card["front"] for card in result[1:]] == ["Q2", "Q3"]

    def test_adaptive_strategy_defensively_copies_missed_indices(
        self,
    ) -> None:
        """Verify that modifications to external set don't affect strategy."""
        missed = {0, 1}
        strategy = AdaptiveStrategy(missed)

        # Modify the external set
        missed.add(2)
        missed.discard(0)

        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
        ]
        result = strategy.order_cards(cards)

        # Strategy should still have {0, 1}, not {1, 2}
        # So Q1 and Q2 should appear first
        assert [card["front"] for card in result[:2]] == ["Q1", "Q2"]
        assert result[2]["front"] == "Q3"

    def test_adaptive_strategy_handles_empty_card_list(self) -> None:
        """Verify that adaptive strategy handles empty input."""
        cards: list[dict[str, str]] = []
        strategy = AdaptiveStrategy({0, 1})
        result = strategy.order_cards(cards)

        assert result == []
        assert result is not cards
