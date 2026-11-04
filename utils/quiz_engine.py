"""Quiz engine for running flashcard quizzes and tracking statistics."""

from dataclasses import dataclass
from typing import Callable

from utils.quiz_modes import QuizModeStrategy


@dataclass
class SessionResult:
    """Statistics from a completed quiz session.

    Fields:
        total_questions: Total number of cards in the quiz.
        correct_answers: Number of correctly answered cards.
        accuracy: Percentage accuracy (0.0 if no questions).
        missed_terms: Front values of incorrectly answered cards.
        missed_indices: Original indices of missed cards.
    """

    total_questions: int
    correct_answers: int
    accuracy: float
    missed_terms: list[str]
    missed_indices: set[int]


class QuizEngine:
    """Execute a flashcard quiz with strategy-based card ordering.

    Presents cards in the order determined by the supplied strategy,
    collects user answers, provides immediate feedback, and tracks
    session statistics including original card indices for later
    use with adaptive strategies.
    """

    def __init__(
        self,
        cards: list[dict[str, str]],
        strategy: QuizModeStrategy,
        input_fn: Callable[[], str] = input,
        output_fn: Callable[[str], None] = print,
    ) -> None:
        """Initialize the quiz engine.

        Args:
            cards: List of validated flashcard dictionaries.
            strategy: QuizModeStrategy instance for card ordering.
            input_fn: Callable that returns user text input.
            output_fn: Callable that prints output messages.
        """
        self._original_cards = cards
        self._strategy = strategy
        self._input_fn = input_fn
        self._output_fn = output_fn

    def run_quiz(self) -> SessionResult:
        """Run the quiz session and return statistics.

        Presents each card's front value, collects the user's answer,
        compares it to the back value (case-insensitive, whitespace-
        trimmed), provides immediate feedback, and returns session
        statistics.

        Returns:
            SessionResult with quiz statistics.
        """
        if not self._original_cards:
            return SessionResult(
                total_questions=0,
                correct_answers=0,
                accuracy=0.0,
                missed_terms=[],
                missed_indices=set(),
            )

        # Create working copies to ensure unique object identities
        working_cards = [card.copy() for card in self._original_cards]

        # Build mapping from card object id to original index
        card_id_to_original_index = {
            id(card): idx for idx, card in enumerate(working_cards)
        }

        # Order cards using the strategy
        ordered_cards = self._strategy.order_cards(working_cards)

        # Initialize tracking variables
        total_questions = len(ordered_cards)
        correct_answers = 0
        missed_terms = []
        missed_indices = set()

        # Run quiz
        for card in ordered_cards:
            self._output_fn(card["front"])
            user_answer = self._input_fn()

            if self._compare_answers(user_answer, card["back"]):
                correct_answers += 1
                self._output_fn("Correct")
            else:
                missed_terms.append(card["front"])
                original_idx = card_id_to_original_index[id(card)]
                missed_indices.add(original_idx)
                self._output_fn("Incorrect")

        # Calculate accuracy
        accuracy = (
            (correct_answers / total_questions) * 100.0
            if total_questions > 0
            else 0.0
        )

        return SessionResult(
            total_questions=total_questions,
            correct_answers=correct_answers,
            accuracy=accuracy,
            missed_terms=missed_terms,
            missed_indices=missed_indices,
        )

    @staticmethod
    def _compare_answers(user_answer: str, correct_answer: str) -> bool:
        """Compare user answer to correct answer (case-insensitive).

        Strips whitespace and performs case-insensitive comparison
        using casefold() for robust handling of unicode characters.

        Args:
            user_answer: The user's text input.
            correct_answer: The card's back value.

        Returns:
            True if answers match (ignoring case and whitespace).
        """
        return (
            user_answer.strip().casefold() == correct_answer.strip().casefold()
        )
