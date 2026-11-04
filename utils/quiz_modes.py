"""Quiz mode strategies for card ordering."""

import random
from abc import ABC, abstractmethod


class QuizModeStrategy(ABC):
    """Abstract base class for quiz mode strategies.

    Defines the interface for ordering flashcards in different quiz modes.
    """

    @abstractmethod
    def order_cards(self, cards: list[dict[str, str]]) -> list[dict[str, str]]:
        """Order cards according to the strategy.

        Args:
            cards: List of flashcard dictionaries to order.

        Returns:
            A new list of flashcards in the desired order.
            The original list is never modified.
        """
        raise NotImplementedError


class SequentialStrategy(QuizModeStrategy):
    """Strategy that returns cards in their original order."""

    def order_cards(self, cards: list[dict[str, str]]) -> list[dict[str, str]]:
        """Return cards in their original order.

        Args:
            cards: List of flashcard dictionaries.

        Returns:
            A copy of the input list in the same order.
        """
        return cards.copy()


class RandomStrategy(QuizModeStrategy):
    """Strategy that returns cards in random order."""

    def order_cards(self, cards: list[dict[str, str]]) -> list[dict[str, str]]:
        """Return cards in randomized order.

        Args:
            cards: List of flashcard dictionaries.

        Returns:
            A shuffled copy of the input list.
        """
        ordered = cards.copy()
        random.shuffle(ordered)
        return ordered


class AdaptiveStrategy(QuizModeStrategy):
    """Strategy that prioritizes previously missed cards.

    Missed cards are presented first in their original relative order,
    followed by non-missed cards in their original relative order.
    """

    def __init__(self, missed_indices: set[int]) -> None:
        """Initialize the adaptive strategy.

        Args:
            missed_indices: Set of zero-based card indices that were missed.
                            Defensively copied to prevent external
                            modification.
        """
        self._missed_indices = missed_indices.copy()

    def order_cards(self, cards: list[dict[str, str]]) -> list[dict[str, str]]:
        """Return missed cards first, then remaining cards.

        Missed cards appear first in their original relative order.
        Non-missed cards appear second in their original relative order.
        Indices outside the range of the card list have no effect.

        Args:
            cards: List of flashcard dictionaries.

        Returns:
            A new list with missed cards first, followed by non-missed cards.
        """
        ordered = []

        # Add missed cards first (preserving their original order)
        for i, card in enumerate(cards):
            if i in self._missed_indices:
                ordered.append(card)

        # Add non-missed cards (preserving their original order)
        for i, card in enumerate(cards):
            if i not in self._missed_indices:
                ordered.append(card)

        return ordered
