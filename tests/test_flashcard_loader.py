"""Unit tests for the JSON flashcard loader."""

import json
import pytest
from pathlib import Path

from utils.flashcard_loader import load_flashcards


class TestValidCases:
    """Test loading valid flashcard files."""

    def test_load_valid_top_level_array(self, tmp_path: Path) -> None:
        """Load and validate a top-level array of flashcards."""
        test_data = [
            {"front": "Question 1", "back": "Answer 1"},
            {"front": "Question 2", "back": "Answer 2"},
        ]
        json_file = tmp_path / "cards.json"
        json_file.write_text(json.dumps(test_data))

        result = load_flashcards(str(json_file))

        assert len(result) == 2
        assert result[0] == {"front": "Question 1", "back": "Answer 1"}
        assert result[1] == {"front": "Question 2", "back": "Answer 2"}

    def test_load_valid_object_with_cards_key(self, tmp_path: Path) -> None:
        """Load and validate an object with a 'cards' key."""
        test_data = {
            "cards": [
                {"front": "Q1", "back": "A1"},
                {"front": "Q2", "back": "A2"},
            ]
        }
        json_file = tmp_path / "cards.json"
        json_file.write_text(json.dumps(test_data))

        result = load_flashcards(str(json_file))

        assert len(result) == 2
        assert result[0] == {"front": "Q1", "back": "A1"}
        assert result[1] == {"front": "Q2", "back": "A2"}

    def test_additional_fields_ignored_in_normalized_card(
        self, tmp_path: Path
    ) -> None:
        """Verify that additional fields in cards are ignored."""
        test_data = [
            {
                "front": "Question",
                "back": "Answer",
                "difficulty": "hard",
                "category": "science",
            }
        ]
        json_file = tmp_path / "cards.json"
        json_file.write_text(json.dumps(test_data))

        result = load_flashcards(str(json_file))

        assert len(result) == 1
        assert result[0] == {"front": "Question", "back": "Answer"}
        assert "difficulty" not in result[0]
        assert "category" not in result[0]


class TestFileAndPathErrors:
    """Test file and path validation."""

    def test_missing_file_raises_file_not_found_error(
        self, tmp_path: Path
    ) -> None:
        """Raise FileNotFoundError when file does not exist."""
        missing_file = tmp_path / "nonexistent.json"

        with pytest.raises(FileNotFoundError, match="not found"):
            load_flashcards(str(missing_file))

    def test_directory_path_raises_value_error(self, tmp_path: Path) -> None:
        """Raise ValueError when path points to a directory."""
        with pytest.raises(ValueError, match="not a regular file"):
            load_flashcards(str(tmp_path))


class TestJSONParseErrors:
    """Test JSON parsing validation."""

    def test_malformed_json_raises_value_error(self, tmp_path: Path) -> None:
        """Raise ValueError for malformed JSON."""
        json_file = tmp_path / "bad.json"
        json_file.write_text("{invalid json content]")

        with pytest.raises(ValueError, match="Malformed JSON"):
            load_flashcards(str(json_file))


class TestJSONStructureErrors:
    """Test JSON structure validation."""

    def test_unsupported_top_level_string_raises_value_error(
        self, tmp_path: Path
    ) -> None:
        """Raise ValueError for top-level string."""
        json_file = tmp_path / "cards.json"
        json_file.write_text(json.dumps("just a string"))

        with pytest.raises(ValueError, match="must be either a list"):
            load_flashcards(str(json_file))

    def test_object_without_cards_key_raises_value_error(
        self, tmp_path: Path
    ) -> None:
        """Raise ValueError when object lacks 'cards' key."""
        test_data = {"data": [{"front": "Q", "back": "A"}]}
        json_file = tmp_path / "cards.json"
        json_file.write_text(json.dumps(test_data))

        with pytest.raises(ValueError, match="'cards' key"):
            load_flashcards(str(json_file))

    def test_cards_value_not_list_raises_value_error(
        self, tmp_path: Path
    ) -> None:
        """Raise ValueError when 'cards' value is not a list."""
        test_data = {"cards": {"front": "Q", "back": "A"}}
        json_file = tmp_path / "cards.json"
        json_file.write_text(json.dumps(test_data))

        with pytest.raises(ValueError, match="must be a list"):
            load_flashcards(str(json_file))


class TestCardValidationErrors:
    """Test validation of individual flashcard objects."""

    def test_card_not_dictionary_raises_value_error(
        self, tmp_path: Path
    ) -> None:
        """Raise ValueError when a card is not a dictionary."""
        test_data = ["not a dict", {"front": "Q", "back": "A"}]
        json_file = tmp_path / "cards.json"
        json_file.write_text(json.dumps(test_data))

        with pytest.raises(ValueError, match="Card 0.*expected a dictionary"):
            load_flashcards(str(json_file))

    def test_card_missing_front_raises_value_error(
        self, tmp_path: Path
    ) -> None:
        """Raise ValueError when a card is missing 'front'."""
        test_data = [{"back": "Answer"}]
        json_file = tmp_path / "cards.json"
        json_file.write_text(json.dumps(test_data))

        with pytest.raises(ValueError, match="Card 0.*missing 'front'"):
            load_flashcards(str(json_file))

    def test_card_missing_back_raises_value_error(
        self, tmp_path: Path
    ) -> None:
        """Raise ValueError when a card is missing 'back'."""
        test_data = [{"front": "Question"}]
        json_file = tmp_path / "cards.json"
        json_file.write_text(json.dumps(test_data))

        with pytest.raises(ValueError, match="Card 0.*missing 'back'"):
            load_flashcards(str(json_file))

    def test_front_not_string_raises_value_error(self, tmp_path: Path) -> None:
        """Raise ValueError when 'front' is not a string."""
        test_data = [{"front": 42, "back": "Answer"}]
        json_file = tmp_path / "cards.json"
        json_file.write_text(json.dumps(test_data))

        with pytest.raises(
            ValueError, match="Card 0.*'front' must be a string"
        ):
            load_flashcards(str(json_file))

    def test_back_not_string_raises_value_error(self, tmp_path: Path) -> None:
        """Raise ValueError when 'back' is not a string."""
        test_data = [{"front": "Question", "back": True}]
        json_file = tmp_path / "cards.json"
        json_file.write_text(json.dumps(test_data))

        with pytest.raises(
            ValueError, match="Card 0.*'back' must be a string"
        ):
            load_flashcards(str(json_file))

    def test_empty_front_string_raises_value_error(
        self, tmp_path: Path
    ) -> None:
        """Raise ValueError when 'front' is an empty string."""
        test_data = [{"front": "", "back": "Answer"}]
        json_file = tmp_path / "cards.json"
        json_file.write_text(json.dumps(test_data))

        with pytest.raises(
            ValueError, match="Card 0.*'front' must be a non-empty"
        ):
            load_flashcards(str(json_file))

    def test_empty_back_string_raises_value_error(
        self, tmp_path: Path
    ) -> None:
        """Raise ValueError when 'back' is an empty string."""
        test_data = [{"front": "Question", "back": ""}]
        json_file = tmp_path / "cards.json"
        json_file.write_text(json.dumps(test_data))

        with pytest.raises(
            ValueError, match="Card 0.*'back' must be a non-empty"
        ):
            load_flashcards(str(json_file))

    def test_whitespace_only_strings_raise_value_error(
        self, tmp_path: Path
    ) -> None:
        """Raise ValueError for whitespace-only strings."""
        test_data_front = [{"front": "   ", "back": "Answer"}]
        json_file = tmp_path / "cards.json"
        json_file.write_text(json.dumps(test_data_front))

        with pytest.raises(
            ValueError, match="Card 0.*'front' must be a non-empty"
        ):
            load_flashcards(str(json_file))

        test_data_back = [{"front": "Question", "back": "\t\n"}]
        json_file.write_text(json.dumps(test_data_back))

        with pytest.raises(
            ValueError, match="Card 0.*'back' must be a non-empty"
        ):
            load_flashcards(str(json_file))
