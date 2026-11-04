"""Entry point for the Flashcard Quizzer CLI.

This file is intentionally empty. Direct your AI agent to build the
application here, following the project Instructions in the classroom.
"""

import argparse
import sys

from utils.flashcard_loader import load_flashcards
from utils.quiz_modes import (
    QuizModeStrategy,
    SequentialStrategy,
    RandomStrategy,
    AdaptiveStrategy,
)
from utils.quiz_engine import QuizEngine, SessionResult


def parse_arguments(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        args: Command-line arguments (None for sys.argv[1:]).

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Quiz yourself with flashcards in various modes."
    )
    parser.add_argument(
        "--mode",
        "-m",
        required=True,
        choices=["sequential", "random", "adaptive"],
        help="Quiz mode: sequential, random, or adaptive",
    )
    parser.add_argument(
        "--file",
        "-f",
        required=True,
        help="Path to JSON file containing flashcards",
    )
    return parser.parse_args(args)


def select_strategy(mode: str) -> QuizModeStrategy:
    """Select and return the appropriate quiz strategy.

    Args:
        mode: Quiz mode name (sequential, random, or adaptive).

    Returns:
        Strategy instance for the specified mode.
    """
    if mode == "sequential":
        return SequentialStrategy()
    elif mode == "random":
        return RandomStrategy()
    elif mode == "adaptive":
        return AdaptiveStrategy(set())
    else:
        raise ValueError(f"Unknown mode: {mode}")


def print_summary(result: SessionResult) -> None:
    """Print quiz session summary.

    Args:
        result: SessionResult from quiz execution.
    """
    missed_terms_str = (
        ", ".join(result.missed_terms) if result.missed_terms else "None"
    )
    print(f"Total Questions: {result.total_questions}")
    print(f"Accuracy: {result.accuracy:.1f}%")
    print(f"Missed Terms: {missed_terms_str}")


def main(args: list[str] | None = None) -> int:
    """Run the Flashcard Quizzer CLI application.

    Args:
        args: Command-line arguments (None for sys.argv[1:]).

    Returns:
        Exit code (0 for success, 1 for expected errors).
    """
    try:
        parsed_args = parse_arguments(args)

        cards = load_flashcards(parsed_args.file)

        strategy = select_strategy(parsed_args.mode)

        engine = QuizEngine(cards, strategy)

        result = engine.run_quiz()

        print_summary(result)

        return 0

    except (FileNotFoundError, ValueError) as e:
        sys.stderr.write(f"Error: {e}\n")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
