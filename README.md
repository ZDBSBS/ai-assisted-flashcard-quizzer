# Flashcard Quizzer

A Python command-line application for studying with flashcards in sequential, random, or adaptive quiz modes.

## Project Overview

Flashcard Quizzer loads flashcards from JSON files and presents them in the quiz mode you choose. Each card shows a question (front) and accepts an answer (back). The application provides immediate feedback, calculates your accuracy, and reports which terms you missed.

## Features

- **Three Quiz Modes:**
  - Sequential: Cards in original order
  - Random: Cards in random order
  - Adaptive: Missed cards prioritized (within a single session)

- **Answer Handling:**
  - Case-insensitive matching
  - Automatic whitespace trimming
  - Immediate Correct or Incorrect feedback

- **Session Statistics:**
  - Total questions answered
  - Accuracy percentage
  - List of missed terms

- **Data Validation:**
  - Support for two JSON formats
  - Clear validation error messages without stack traces
  - Rejection of malformed or incomplete card data

## Architecture

The application is structured around four main modules:

| Module | Responsibility |
|--------|-----------------|
| `main.py` | CLI argument parsing, strategy selection, and application orchestration |
| `utils/flashcard_loader.py` | JSON loading, format normalization, and card validation |
| `utils/quiz_modes.py` | Strategy Pattern implementation for card ordering |
| `utils/quiz_engine.py` | Quiz execution, answer comparison, and session statistics |

The Strategy Pattern isolates card-ordering logic from quiz execution, making it easy to add new quiz modes in the future.

## Project Structure

```
project/starter/
├── main.py                          # CLI entry point
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Black configuration
├── README.md                        # This file
├── utils/
│   ├── __init__.py
│   ├── flashcard_loader.py          # JSON loading and validation
│   ├── quiz_modes.py                # Strategy Pattern implementations
│   └── quiz_engine.py               # Quiz execution engine
├── data/
│   ├── glossary.json                # Sample deck (10 cards)
│   └── python_basics.json           # Sample deck (8 cards)
├── tests/
│   ├── __init__.py
│   ├── test_main.py                 # CLI tests
│   ├── test_flashcard_loader.py     # Loader tests
│   ├── test_quiz_modes.py           # Strategy tests
│   └── test_quiz_engine.py          # Engine tests
└── docs/
    └── ai_edit_log.md               # AI collaboration log
```

## Requirements

- Python 3.10 or later
- The application runtime uses only the Python standard library
- Development and quality-assurance tools are listed in `requirements.txt`

## Installation

### 1. Clone or navigate to the project directory

```bash
cd project/starter
```

### 2. Create a virtual environment

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Usage

### Display help

```bash
python main.py --help
```

### Sequential mode (original order)

```bash
python main.py --mode sequential --file data/glossary.json
```

### Random mode (shuffled order)

```bash
python main.py --mode random --file data/glossary.json
```

### Adaptive mode (missed cards first)

```bash
python main.py -m adaptive -f data/python_basics.json
```

### Argument forms

- `--mode` or `-m`: Quiz mode (sequential, random, or adaptive) — **required**
- `--file` or `-f`: Path to JSON deck file — **required**

### Example output

When you complete a quiz, the application displays:

```
Total Questions: 10
Accuracy: 70.0%
Missed Terms: API, DNS, VPN
```

If you answer all questions correctly:

```
Total Questions: 10
Accuracy: 100.0%
Missed Terms: None
```

## JSON Deck Formats

Flashcard Quizzer supports two JSON formats. Both are valid and produce identical results.

### Format 1: Top-level array

```json
[
  {"front": "What is Python?", "back": "A programming language"},
  {"front": "What is a list?", "back": "An ordered collection"}
]
```

### Format 2: Top-level object with "cards" key

```json
{
  "cards": [
    {"front": "What is Python?", "back": "A programming language"},
    {"front": "What is a list?", "back": "An ordered collection"}
  ]
}
```

**Requirements:**
- Each card must have non-empty `front` and `back` fields (strings)
- Leading and trailing whitespace in field values is allowed
- Additional card fields are ignored (only `front` and `back` are used)

## Testing and Quality Checks

### Run all tests

```bash
python -m pytest -v
```

**Result:** 70 tests pass

### Coverage report

```bash
python -m pytest --cov=. --cov-report=term-missing
```

**Result:** 99% coverage across all modules

### Code formatting

```bash
python -m black --check .
```

### Linting

```bash
python -m flake8 .
```

### Type checking

```bash
python -m mypy .
```

All quality checks pass without errors or warnings.

## Adaptive Mode Limitation

`AdaptiveStrategy` prioritizes card indices supplied as previously
missed. The current standalone CLI does not persist quiz results
between separate program executions.

Each adaptive CLI execution therefore starts with an empty missed-index
set and initially preserves the deck order. The quiz engine still
records missed indices in its `SessionResult`, allowing this information
to be supplied to a later adaptive round by future orchestration or
persistence functionality.

Persistent adaptive learning and automatic repeated quiz rounds are not
implemented in this version.

## AI-Assisted Development

This project was developed using AI assistance and human review. The application demonstrates effective collaboration with AI tools while maintaining high code quality and comprehensive testing.

For a detailed record of AI interactions, design decisions, and implementation choices, see [docs/ai_edit_log.md](docs/ai_edit_log.md).

Key AI-assisted phases:
1. JSON flashcard loader with validation
2. Strategy Pattern for quiz modes
3. Quiz engine with session statistics
4. CLI integration and argument parsing
5. Comprehensive test suite and smoke testing

Each phase included:
- Structured planning with explicit requirements
- AI implementation review and refinement
- Automated testing and code-quality validation
- Documentation of decisions and lessons learned
