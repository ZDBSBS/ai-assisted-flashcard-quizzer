"""Unit tests for main.py CLI application."""

import pytest
from unittest.mock import Mock, patch

import main
from utils.quiz_modes import (
    SequentialStrategy,
    RandomStrategy,
    AdaptiveStrategy,
)
from utils.quiz_engine import SessionResult


class TestParseArguments:
    """Test argument parsing."""

    def test_parse_arguments_long_options_sequential(self) -> None:
        """Verify long options work for sequential mode and file."""
        args = main.parse_arguments(
            ["--mode", "sequential", "--file", "data/test.json"]
        )
        assert args.mode == "sequential"
        assert args.file == "data/test.json"

    def test_parse_arguments_short_options_adaptive(self) -> None:
        """Verify short options work for adaptive mode and file."""
        args = main.parse_arguments(["-m", "adaptive", "-f", "data/test.json"])
        assert args.mode == "adaptive"
        assert args.file == "data/test.json"

    def test_parse_arguments_missing_mode(self) -> None:
        """Verify missing mode raises SystemExit with code 2."""
        with pytest.raises(SystemExit) as exc_info:
            main.parse_arguments(["--file", "data/test.json"])
        assert exc_info.value.code == 2

    def test_parse_arguments_missing_file(self) -> None:
        """Verify missing file raises SystemExit with code 2."""
        with pytest.raises(SystemExit) as exc_info:
            main.parse_arguments(["--mode", "sequential"])
        assert exc_info.value.code == 2

    def test_parse_arguments_invalid_mode(self) -> None:
        """Verify invalid mode raises SystemExit with code 2."""
        with pytest.raises(SystemExit) as exc_info:
            main.parse_arguments(
                ["--mode", "invalid", "--file", "data/test.json"]
            )
        assert exc_info.value.code == 2


class TestSelectStrategy:
    """Test strategy selection."""

    def test_select_strategy_sequential(self) -> None:
        """Verify sequential mode returns SequentialStrategy."""
        strategy = main.select_strategy("sequential")
        assert isinstance(strategy, SequentialStrategy)

    def test_select_strategy_random(self) -> None:
        """Verify random mode returns RandomStrategy."""
        strategy = main.select_strategy("random")
        assert isinstance(strategy, RandomStrategy)

    def test_select_strategy_adaptive(self) -> None:
        """Verify adaptive mode returns AdaptiveStrategy."""
        strategy = main.select_strategy("adaptive")
        assert isinstance(strategy, AdaptiveStrategy)

    def test_select_strategy_unknown_mode(self) -> None:
        """Verify unknown mode raises ValueError."""
        with pytest.raises(ValueError):
            main.select_strategy("unknown")


class TestPrintSummary:
    """Test summary output."""

    def test_print_summary_with_missed_terms(self, capsys) -> None:
        """Verify summary displays questions, accuracy, and missed terms."""
        result = SessionResult(
            total_questions=5,
            correct_answers=3,
            accuracy=60.0,
            missed_terms=["Question 1", "Question 3"],
            missed_indices={0, 2},
        )
        main.print_summary(result)

        captured = capsys.readouterr()
        assert "Total Questions: 5" in captured.out
        assert "Accuracy: 60.0%" in captured.out
        assert "Missed Terms: Question 1, Question 3" in captured.out

    def test_print_summary_no_missed_terms(self, capsys) -> None:
        """Verify summary displays None when no terms missed."""
        result = SessionResult(
            total_questions=3,
            correct_answers=3,
            accuracy=100.0,
            missed_terms=[],
            missed_indices=set(),
        )
        main.print_summary(result)

        captured = capsys.readouterr()
        assert "Total Questions: 3" in captured.out
        assert "Accuracy: 100.0%" in captured.out
        assert "Missed Terms: None" in captured.out

    def test_print_summary_accuracy_one_decimal_place(self, capsys) -> None:
        """Verify accuracy is formatted to one decimal place."""
        result = SessionResult(
            total_questions=3,
            correct_answers=2,
            accuracy=66.66666666666667,
            missed_terms=["Question 3"],
            missed_indices={2},
        )
        main.print_summary(result)

        captured = capsys.readouterr()
        assert "Accuracy: 66.7%" in captured.out


class TestMain:
    """Test main application logic."""

    @patch("main.load_flashcards")
    @patch("main.QuizEngine")
    def test_main_success_returns_zero(
        self,
        mock_engine_class,
        mock_load,
        capsys,
    ) -> None:
        """Verify main returns 0 and prints summary on success."""
        # Setup mocks
        cards = [{"front": "Q1", "back": "A1"}]
        mock_load.return_value = cards

        mock_quiz = Mock()
        mock_quiz.run_quiz.return_value = SessionResult(
            total_questions=1,
            correct_answers=1,
            accuracy=100.0,
            missed_terms=[],
            missed_indices=set(),
        )
        mock_engine_class.return_value = mock_quiz

        # Run main
        exit_code = main.main(["-m", "sequential", "-f", "data/test.json"])

        # Verify
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Total Questions: 1" in captured.out
        assert "Accuracy: 100.0%" in captured.out

    @patch("main.load_flashcards")
    def test_main_file_not_found_returns_one(
        self,
        mock_load,
        capsys,
    ) -> None:
        """Verify main returns 1 for FileNotFoundError."""
        mock_load.side_effect = FileNotFoundError(
            "Flashcard file not found: missing.json"
        )

        exit_code = main.main(["-m", "sequential", "-f", "missing.json"])

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error: Flashcard file not found: missing.json" in (
            captured.err
        )

    @patch("main.load_flashcards")
    def test_main_value_error_returns_one(
        self,
        mock_load,
        capsys,
    ) -> None:
        """Verify main returns 1 for ValueError."""
        mock_load.side_effect = ValueError("Card 0: missing 'back' field")

        exit_code = main.main(["-m", "sequential", "-f", "bad.json"])

        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error: Card 0: missing 'back' field" in captured.err

    @patch("main.load_flashcards")
    @patch("main.QuizEngine")
    def test_main_integration_with_mocked_input(
        self,
        mock_engine_class,
        mock_load,
        capsys,
    ) -> None:
        """Verify main integrates components without interactive input."""
        # Setup loader
        cards = [
            {"front": "Q1", "back": "A1"},
            {"front": "Q2", "back": "A2"},
        ]
        mock_load.return_value = cards

        # Setup quiz engine
        mock_quiz = Mock()
        mock_quiz.run_quiz.return_value = SessionResult(
            total_questions=2,
            correct_answers=1,
            accuracy=50.0,
            missed_terms=["Q2"],
            missed_indices={1},
        )
        mock_engine_class.return_value = mock_quiz

        # Run main
        exit_code = main.main(["-m", "random", "-f", "data/test.json"])

        # Verify integration
        assert exit_code == 0
        mock_load.assert_called_once_with("data/test.json")
        mock_engine_class.assert_called_once()
        mock_quiz.run_quiz.assert_called_once()

        captured = capsys.readouterr()
        assert "Total Questions: 2" in captured.out
        assert "Accuracy: 50.0%" in captured.out
        assert "Missed Terms: Q2" in captured.out
