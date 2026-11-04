# AI-Assisted Development Project Report

**Student Name:** Zied Besbes  
**Project Title:** AI-Assisted Flashcard Quizzer  
**Date:** 2026-11-04

## Executive Summary

The AI-Assisted Flashcard Quizzer is a Python command-line application that loads flashcards from JSON files and quizzes users in sequential, random, or adaptive mode. It validates deck data, compares answers without case sensitivity, provides immediate feedback, and displays total questions, accuracy, and missed terms.

Claude Code supported planning, implementation, testing, review, and documentation. AI output was never accepted automatically. The work was divided into small XML-style prompts with explicit context, requirements, constraints, validation commands, and deliverables. The final project passed 70 automated tests, achieved 99% total project coverage, and passed Black, Flake8, and mypy checks.

## Project Overview

### Problem Statement

Learners need a lightweight and reusable way to review technical terms.

### Solution Approach

The project uses Python 3.10 or later, the Python standard library, pytest, coverage, Black, Flake8, and mypy. Responsibilities are separated across modules.

`flashcard_loader.py` loads and validates JSON data. `quiz_modes.py` contains card-ordering strategies. `quiz_engine.py` executes quiz sessions and returns typed statistics. `main.py` processes command-line arguments, selects the requested components, handles expected errors, and prints the final summary.

The Strategy Pattern separates the three ordering algorithms from the quiz loop. Dependency injection for input and output makes interactive behavior deterministic and testable.

### Final Features

- [x] Load and validate JSON flashcard decks
- [x] Support a top-level JSON array and an object containing a `cards` array
- [x] Run sequential, random, and adaptive quiz modes
- [x] Compare answers without case sensitivity
- [x] Ignore leading and trailing whitespace in answers
- [x] Provide immediate `Correct` or `Incorrect` feedback
- [x] Display total questions, accuracy, and missed terms
- [x] Handle expected file and validation errors without a raw traceback

## AI Collaboration Experience

### AI Tools Used

- [x] Claude Code
- [x] Microsoft Copilot
- [ ] GitHub Copilot
- [ ] ChatGPT

### Collaboration Workflow

1. Each task began with a focused XML-style prompt containing the role, task, context, requirements, constraints, validation steps, and deliverables.
2. Claude Code assisted with component planning, implementation, tests, reviews, corrections, and documentation.
3. Generated changes were reviewed against the project requirements and code-review checklist.
4. Tests were executed individually, then in related groups, and finally as a complete suite.
5. Weak, unnecessary, or out-of-scope suggestions were rejected and documented.
6. Only tested and reviewed changes were committed and pushed to GitHub.

### Most Valuable AI Interactions

#### Example 1: Validated JSON Loader

**Context:** Flashcard files required safe loading and clear validation errors.

**AI Prompt:** Claude Code was asked to support the two required JSON structures, type hints, regular-file validation, and focused error tests.

**AI Response:** Claude Code generated a loader and an initial test plan.

**Changes Made:** Validation was strengthened for directory paths, missing fields, invalid types, empty strings, and whitespace-only values. Additional fields were accepted rather than causing otherwise valid cards to be rejected. The proposed `any` annotation was corrected to `typing.Any`.

**Outcome:** All 17 loader tests passed, and the module achieved 100% coverage.

#### Example 2: Strategy Pattern

**Context:** Three quiz modes required interchangeable card-ordering behavior.

**AI Prompt:** The prompt requested one abstract strategy interface and sequential, random, and adaptive implementations that would not modify the input list.

**AI Response:** Claude Code created the strategy classes and proposed their tests.

**Changes Made:** The adaptive missed-index set was defensively copied, invalid indices were clarified, duplicate tests were combined, and random ordering was tested deterministically by patching `utils.quiz_modes.random.shuffle`.

**Outcome:** All 18 strategy tests passed, and the quiz-mode module achieved 96% coverage.

#### Example 3: Quiz Engine

**Context:** The application required testable interaction, feedback, accuracy, missed terms, and original missed-card indices.

**AI Prompt:** Claude Code was asked to create `SessionResult` and `QuizEngine` with injected input and output callables.

**AI Response:** Claude Code implemented session execution, answer normalization, feedback, and statistics.

**Changes Made:** Exact `Correct` and `Incorrect` output was required, additional question prefixes were avoided, and separate internal card copies were used to preserve original indices. An AI-generated test for a custom strategy that returned unrelated dictionary copies was rejected as outside the approved interface.

**Outcome:** All 19 engine tests passed, and the quiz engine achieved 100% coverage.

### Challenges with AI Collaboration

Claude Code produced useful code quickly but occasionally tried to solve tool failures by changing project standards. For example, Claude Code proposed a `.flake8` file that increased the maximum line length to 88. This suggestion was rejected because it weakened Flake8’s existing rule. Instead, Black was configured through `pyproject.toml` to use a 79-character line length.

Claude Code also generated a test that required support for custom strategies returning newly created card dictionaries. This behavior was outside the agreed Strategy interface. The test was removed rather than expanding production code for an invented requirement.

## Software Engineering Practices

### Code Quality Measures

- [x] Code formatting with Black
- [x] Linting with Flake8
- [x] Static type checking with mypy
- [x] Python type hints
- [x] English docstrings
- [x] Input validation
- [x] Expected-error handling
- [x] Modular separation of concerns

### Testing Strategy

Testing covered successful behavior, malformed JSON, missing files, invalid paths, wrong types, empty values, whitespace-only values, deterministic random ordering, adaptive prioritization, answer comparison, feedback, statistics, empty sessions, input preservation, injected callables, CLI arguments, error exit codes, and summary output.

Tests were run first by component, then as related groups, and finally as a complete suite. The final run passed 70 tests. Total project coverage was 99%, including 100% for the loader, 100% for the quiz engine, 96% for quiz modes, and 97% for `main.py`.

Manual smoke tests also verified sequential, random, and adaptive execution with the supplied decks.

### Design Patterns Used

- **Strategy Pattern:** `QuizModeStrategy` provides one shared interface for sequential, random, and adaptive card ordering.
- **Dependency Injection:** `QuizEngine` receives a strategy plus input and output functions, reducing coupling and enabling deterministic testing.

### Code Structure and Organization

`main.py` coordinates the CLI. The `utils` package separates loading, ordering, and quiz execution. The `tests` directory mirrors these responsibilities.

## Technical Challenges and Solutions

### Challenge 1: Formatter and Linter Conflict

**Problem:** Black’s default 88-character line length conflicted with Flake8’s 79-character rule.

**Solution:** The proposed Flake8 relaxation was removed. Black was configured in `pyproject.toml` to use 79 characters.

**Lessons Learned:** Development tools should use one consistent policy without weakening existing quality checks.

### Challenge 2: Original Index Tracking

**Problem:** Missed cards needed their original indices after strategy-based reordering.

**Solution:** The quiz engine creates a separate working dictionary for every input position and maps those internal objects to their original indices before ordering.

**Lessons Learned:** Object identity and equality are different concerns and require behavior-based tests.

## Code Quality Analysis

### Metrics

- Automated tests: 70 passing
- Total project coverage: 99%
- Loader coverage: 100%
- Quiz engine coverage: 100%
- Quiz-mode coverage: 96%
- `main.py` coverage: 97%
- Flake8 errors: 0
- mypy issues: 0

### Self-Assessment

- **Code Readability:** 5/5, supported by clear names, focused modules, type hints, and docstrings.
- **Code Maintainability:** 5/5, because loading, ordering, execution, and CLI responsibilities are separated.
- **Test Quality:** 5/5, because deterministic tests cover successful, edge, and error paths.
- **Documentation:** 5/5, because setup, usage, AI decisions, limitations, and verified outcomes are documented.

## Learning Outcomes

### Technical Skills Developed

The project strengthened practical skills in Python typing, dataclasses, abstract base classes, JSON validation, CLI design, Strategy Pattern implementation, dependency injection, mocking, coverage analysis, layered testing, and Git-based version control.

### AI Collaboration Skills

The main lesson was to treat AI output as a proposal rather than a final answer. Explicit scope, focused prompts, deterministic tests, and documented acceptance or rejection decisions produced more reliable results.

## Reflection

### What Worked Well

Small XML-style prompts reduced unintended changes. Running tests individually, in groups, and as a complete suite made failures easier to isolate.

### What Could Be Improved

Future work should define formatting rules at the beginning of the project. More subprocess-based tests could verify complete terminal sessions. Code metrics could also be collected automatically before documentation is written.

### Future Enhancements

Potential enhancements include persistent adaptive history, spaced repetition, deck export, richer summary tables, configurable logging, and performance tests for large decks. New functionality should remain isolated through strategies or dedicated services.

## Conclusion

AI assistance accelerated planning, implementation, testing, and documentation, while human review protected scope, quality, and rubric compliance. The completed project demonstrates that reliable AI-assisted development requires explicit requirements, critical review, deterministic testing, static analysis, manual validation, and verification before commits.

The final Flashcard Quizzer meets the functional and technical goals with a simple, modular, and testable architecture.

## Appendices

### Appendix A: AI Interaction Log

`docs/ai_edit_log.md` contains the detailed loader, strategy, quiz engine, CLI, review, correction, and validation interactions.

### Appendix B: Code Statistics

The final verified results are 70 passing tests, 99% total project coverage, 100% loader coverage, 100% quiz-engine coverage, 96% quiz-mode coverage, 97% coverage for `main.py`, zero Flake8 errors, and zero mypy issues.