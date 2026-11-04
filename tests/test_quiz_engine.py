"""Unit tests for the quiz engine and session results."""

import pytest
from unittest.mock import Mock

from utils.quiz_engine import QuizEngine, SessionResult
from utils.quiz_modes import QuizModeStrategy


class AllCorrectStrategy(QuizModeStrategy):
    """Test strategy that preserves original order."""

    def order_cards(self, cards: list[dict[str, str]]) -> list[dict[str, str]]:
        """Return cards in original order."""
        return cards.copy()


class ReversingStrategy(QuizModeStrategy):
    """Test strategy that reverses card order."""

    def order_cards(self, cards: list[dict[str, str]]) -> list[dict[str, str]]:
        """Return cards in reversed order."""
        reversed_list = cards.copy()
        reversed_list.reverse()
        return reversed_list


class TestSessionResult:
    """Test SessionResult dataclass."""

    def test_session_result_fields(self) -> None:
        """Verify SessionResult contains all required fields."""
        result = SessionResult(
            total_questions=5,
            correct_answers=3,
            accuracy=60.0,
            missed_terms=["Q1", "Q3"],
            missed_indices={0, 2},
        )

        assert result.total_questions == 5
        assert result.correct_answers == 3
        assert result.accuracy == 60.0
        assert result.missed_terms == ["Q1", "Q3"]
        assert result.missed_indices == {0, 2}


class TestQuizEngineAllCorrect:
    """Test quiz engine with all correct answers."""

    def test_all_answers_correct(self) -> None:
        """Verify statistics when all answers are correct."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
        ]
        answers = ["A1", "A2", "A3"]
        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        result = engine.run_quiz()

        assert result.total_questions == 3
        assert result.correct_answers == 3
        assert result.accuracy == 100.0
        assert result.missed_terms == []
        assert result.missed_indices == set()

    def test_all_correct_feedback(self) -> None:
        """Verify Correct feedback for all answers."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
        ]
        answers = ["A1", "A2"]
        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        engine.run_quiz()

        # Check that "Correct" was output
        correct_calls = [
            call
            for call in output_fn.call_args_list
            if call[0][0] == "Correct"
        ]
        assert len(correct_calls) == 2


class TestQuizEngineAllIncorrect:
    """Test quiz engine with all incorrect answers."""

    def test_all_answers_incorrect(self) -> None:
        """Verify statistics when all answers are incorrect."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
        ]
        answers = ["wrong1", "wrong2", "wrong3"]
        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        result = engine.run_quiz()

        assert result.total_questions == 3
        assert result.correct_answers == 0
        assert result.accuracy == 0.0
        assert result.missed_terms == ["Q1", "Q2", "Q3"]
        assert result.missed_indices == {0, 1, 2}

    def test_all_incorrect_feedback(self) -> None:
        """Verify Incorrect feedback for all answers."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
        ]
        answers = ["wrong1", "wrong2"]
        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        engine.run_quiz()

        # Check that "Incorrect" was output
        incorrect_calls = [
            call
            for call in output_fn.call_args_list
            if call[0][0] == "Incorrect"
        ]
        assert len(incorrect_calls) == 2


class TestQuizEngineMixed:
    """Test quiz engine with mixed correct and incorrect answers."""

    def test_mixed_answers(self) -> None:
        """Verify statistics with mixed correct/incorrect answers."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
            {"front": "Q4", "back": "A4"},
        ]
        answers = ["A1", "wrong", "A3", "wrong"]
        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        result = engine.run_quiz()

        assert result.total_questions == 4
        assert result.correct_answers == 2
        assert result.accuracy == 50.0
        assert result.missed_terms == ["Q2", "Q4"]
        assert result.missed_indices == {1, 3}


class TestAnswerComparison:
    """Test answer comparison rules."""

    def test_case_insensitive_comparison(self) -> None:
        """Verify case-insensitive answer matching."""
        cards = [
            {"front": "Q1", "back": "Python"},
        ]
        answers = ["PYTHON"]
        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        result = engine.run_quiz()

        assert result.correct_answers == 1

    def test_whitespace_trimming(self) -> None:
        """Verify leading and trailing whitespace is ignored."""
        cards = [
            {"front": "Q1", "back": "answer"},
        ]
        answers = ["  answer  "]
        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        result = engine.run_quiz()

        assert result.correct_answers == 1

    def test_case_and_whitespace_combined(self) -> None:
        """Verify case-insensitive with whitespace trimming."""
        cards = [
            {"front": "Q1", "back": "Answer"},
        ]
        answers = ["  ANSWER  "]
        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        result = engine.run_quiz()

        assert result.correct_answers == 1


class TestImmediateFeedback:
    """Test immediate feedback output."""

    def test_correct_feedback_exact_text(self) -> None:
        """Verify Correct feedback uses exact text."""
        cards = [
            {"front": "Q1", "back": "A1"},
        ]
        answers = ["A1"]
        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        engine.run_quiz()

        # Verify "Correct" appears in output
        output_calls = [call[0][0] for call in output_fn.call_args_list]
        assert "Correct" in output_calls

    def test_incorrect_feedback_exact_text(self) -> None:
        """Verify Incorrect feedback uses exact text."""
        cards = [
            {"front": "Q1", "back": "A1"},
        ]
        answers = ["wrong"]
        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        engine.run_quiz()

        # Verify "Incorrect" appears in output
        output_calls = [call[0][0] for call in output_fn.call_args_list]
        assert "Incorrect" in output_calls


class TestAccuracyCalculation:
    """Test accuracy calculation."""

    def test_accuracy_percentage(self) -> None:
        """Verify accuracy is calculated as percentage."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
        ]
        answers = ["A1", "wrong", "A3"]
        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        result = engine.run_quiz()

        assert result.accuracy == pytest.approx(66.66666666666666)

    def test_accuracy_zero_questions(self) -> None:
        """Verify accuracy is 0.0 for empty card list."""
        cards: list[dict[str, str]] = []
        input_fn = Mock()
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        result = engine.run_quiz()

        assert result.accuracy == 0.0


class TestMissedTermsAndIndices:
    """Test missed terms and indices tracking."""

    def test_missed_terms_in_order(self) -> None:
        """Verify missed terms appear in quiz order."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
        ]
        answers = ["wrong", "A2", "wrong"]
        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        result = engine.run_quiz()

        assert result.missed_terms == ["Q1", "Q3"]

    def test_missed_indices_from_reversed_strategy(self) -> None:
        """Verify original indices after strategy reordering."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
            {"front": "Q3", "back": "A3"},
        ]
        # Answers in reversed order: wrong, A2, wrong
        # Reversed order is Q3, Q2, Q1 (indices 2, 1, 0)
        # So missing Q3 (orig idx 2) and Q1 (orig idx 0)
        answers = ["wrong", "A2", "wrong"]
        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        engine = QuizEngine(cards, ReversingStrategy(), input_fn, output_fn)
        result = engine.run_quiz()

        assert result.missed_indices == {0, 2}


class TestEmptyCardList:
    """Test handling of empty card list."""

    def test_empty_cards(self) -> None:
        """Verify empty card list returns correct result."""
        cards: list[dict[str, str]] = []
        input_fn = Mock()
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        result = engine.run_quiz()

        assert result.total_questions == 0
        assert result.correct_answers == 0
        assert result.accuracy == 0.0
        assert result.missed_terms == []
        assert result.missed_indices == set()


class TestOriginalCardsPreservation:
    """Test that original input cards are not modified."""

    def test_original_cards_unchanged(self) -> None:
        """Verify original card list is not modified."""
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
        ]
        original_cards_copy = [card.copy() for card in cards]
        answers = ["A1", "A2"]
        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        engine.run_quiz()

        assert cards == original_cards_copy


class TestQuestionPresentation:
    """Test question presentation to user."""

    def test_front_value_presented(self) -> None:
        """Verify card front values are presented."""
        cards = [
            {"front": "First Question", "back": "A1"},
            {"front": "Second Question", "back": "A2"},
        ]
        answers = ["A1", "A2"]
        input_fn = Mock(side_effect=answers)
        output_fn = Mock()

        engine = QuizEngine(cards, AllCorrectStrategy(), input_fn, output_fn)
        engine.run_quiz()

        # Verify front values were output
        output_calls = [call[0][0] for call in output_fn.call_args_list]
        assert "First Question" in output_calls
        assert "Second Question" in output_calls


class TestInjectedCallables:
    """Test injected input and output callables."""

    def test_default_input_output_callable(self) -> None:
        """Verify default input/output callables work."""
        cards = [
            {"front": "Q1", "back": "A1"},
        ]
        input_fn = Mock(return_value="A1")
        output_fn = Mock()

        engine = QuizEngine(
            cards,
            AllCorrectStrategy(),
            input_fn,
            output_fn,
        )
        result = engine.run_quiz()

        assert input_fn.called
        assert output_fn.called
        assert result.correct_answers == 1
