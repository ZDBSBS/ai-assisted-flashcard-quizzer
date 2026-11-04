"""Load and validate flashcards from JSON files."""

import json
from pathlib import Path
from typing import Any


def load_flashcards(filepath: str) -> list[dict[str, str]]:
    """Load and validate flashcards from a JSON file.

    Supports two JSON formats:
    - Top-level array: [{"front": "...", "back": "..."}, ...]
    - Top-level object: {"cards": [{"front": "...", "back": "..."}, ...]}

    Args:
        filepath: Path to the JSON file containing flashcards.

    Returns:
        List of normalized flashcard dictionaries, each containing
        only "front" and "back" keys with non-empty string values.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the JSON is malformed, has unsupported structure,
                    or contains invalid flashcard data.
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"Flashcard file not found: {filepath}")

    if not path.is_file():
        raise ValueError(f"Path is not a regular file: {filepath}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Malformed JSON in {filepath}: {e}")

    # Normalize JSON structure to a list of cards
    cards_list = _normalize_json_to_list(data)

    # Validate and normalize each card
    validated_cards = []
    for index, card in enumerate(cards_list):
        validated_card = _validate_card(card, index)
        validated_cards.append(validated_card)

    return validated_cards


def _normalize_json_to_list(data: Any) -> list[Any]:
    """Convert JSON data to a list of card objects.

    Handles two formats:
    - List: returned as-is
    - Dict with "cards" key: returns the "cards" value

    Args:
        data: The parsed JSON data.

    Returns:
        A list of card objects.

    Raises:
        ValueError: If the structure is not a list or dict with "cards" key.
    """
    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        if "cards" not in data:
            raise ValueError(
                "JSON object must contain a 'cards' key with a " "list of flashcards"
            )
        cards = data["cards"]
        if not isinstance(cards, list):
            raise ValueError("The 'cards' field must be a list of flashcard objects")
        return cards

    raise ValueError(
        "JSON must be either a list of flashcards or an " "object with a 'cards' key"
    )


def _validate_card(card: Any, index: int) -> dict[str, str]:
    """Validate and normalize a single flashcard.

    Ensures the card is a dictionary with non-empty "front" and "back" fields.
    Additional fields are ignored. Returns a normalized card with only
    "front" and "back" keys.

    Args:
        card: The card object to validate.
        index: The card's position in the list (for error messages).

    Returns:
        A normalized dictionary with "front" and "back" keys.

    Raises:
        ValueError: If the card is invalid or missing required fields.
    """
    if not isinstance(card, dict):
        raise ValueError(
            f"Card {index}: expected a dictionary, got {type(card).__name__}"
        )

    # Check for required fields
    if "front" not in card:
        raise ValueError(f"Card {index}: missing 'front' field")
    if "back" not in card:
        raise ValueError(f"Card {index}: missing 'back' field")

    front = card["front"]
    back = card["back"]

    # Validate types
    if not isinstance(front, str):
        raise ValueError(
            f"Card {index}: 'front' must be a string, " f"got {type(front).__name__}"
        )
    if not isinstance(back, str):
        raise ValueError(
            f"Card {index}: 'back' must be a string, " f"got {type(back).__name__}"
        )

    # Validate non-empty (treat whitespace-only as empty)
    if not front.strip():
        raise ValueError(f"Card {index}: 'front' must be a non-empty string")
    if not back.strip():
        raise ValueError(f"Card {index}: 'back' must be a non-empty string")

    # Return normalized card with only "front" and "back"
    return {"front": front, "back": back}
