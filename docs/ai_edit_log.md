# AI Edit Log

**Instructions:** Use this document to track all your interactions with AI assistants during the project. This log will help you reflect on your AI collaboration process and demonstrate your learning journey.

## How to Use This Log

For each AI interaction, create a new entry with the following structure:

### Entry Template
```
## [Date] - [Brief Description]

**Context:** What were you trying to accomplish?
**AI Tool Used:** Claude/ChatGPT/Copilot/etc.
**Prompt/Request:** What exactly did you ask the AI?
**AI Response:** Summary of what the AI generated (don't copy entire code blocks)
**Changes Made:** What modifications did you make to the AI's suggestions?
**Reasoning:** Why did you make those changes?
**Outcome:** What was the final result?
**Lessons Learned:** What did you learn from this interaction?
```

---

## Example Entry

> This entry shows the expected level of detail. It does **not** count toward your five required entries. Delete it before you submit.

### 2024-01-15 - Flashcard Loader Validation

**Context:** I needed a module that loads flashcards from a JSON file and rejects bad data with a clear message instead of a traceback.

**AI Tool Used:** Claude Code

**Prompt/Request:** "Create `data_loader.py` with a function that loads flashcards from a JSON file. Support both a plain list of `{"front", "back"}` objects and a `{"cards": [...]}` wrapper. Raise a custom exception with a helpful message if the file is missing, the JSON is malformed, or a card has no `back`. Use type hints."

**AI Response:** Claude generated a `load_flashcards()` function and a `FlashcardLoadError` exception. It handled both JSON formats and a missing file, but it caught every exception with a bare `except:` and only checked for `front`.

**Changes Made:** 
- Replaced the bare `except:` with specific `FileNotFoundError` and `json.JSONDecodeError` handlers
- Added validation that every card has non-empty `front` and `back` strings
- Added the card's position to the error message so the user can find the bad entry

**Reasoning:** 
- A bare `except:` hides real bugs, including `KeyboardInterrupt`
- A card without a `back` would break the quiz loop later, far from the cause
- A message that names the bad card is far easier to act on

**Outcome:** The loader now rejects bad decks with one readable line, and `test_load_missing_required_field` passes.

**Lessons Learned:** 
- AI covered the happy path well but under-specified the error handling
- Naming the exact failure cases in the prompt produced better code than asking for "error handling"
- Each requirement in the prompt should map to a test

---

## Your Log Entries

### 2026-11-04 - JSON Flashcard Loader Implementation and Review

**Context:** The project required a reliable loader for the two provided JSON flashcard formats. The loader needed to validate the input data, return a consistent card representation, and provide clear errors for invalid files and card structures.

**AI Tool Used:** Claude Code

**Prompt/Request:** I used a structured XML-style prompt asking Claude Code to plan and then implement only the JSON flashcard loader in `utils/flashcard_loader.py`. The prompt required support for a top-level array and an object containing a `cards` array. It also required type hints, English docstrings, PEP 8 compliance, standard-library-only implementation, clear exceptions, and no changes to unrelated files.

**AI Response:** Claude Code proposed a public `load_flashcards()` function and two private validation helpers. It then created the loader with support for both JSON formats, validation of the `front` and `back` fields, normalization of returned cards, and descriptive exceptions.

**Changes Made:**
- Replaced the proposed `any` type annotation with `typing.Any`
- Clarified that additional card fields should be accepted but excluded from the normalized result
- Added validation that the supplied path is a regular file
- Added validation that whitespace-only `front` and `back` values are rejected
- Reviewed and corrected formatting to make Black and Flake8 compatible
- Added `pyproject.toml` with a Black line length of 79 to align Black with Flake8's default line-length rule
- Added 17 focused unit tests covering valid inputs, malformed JSON, invalid structures, missing fields, invalid types, empty values, whitespace-only values, additional fields, missing files, and directory paths

**Reasoning:** The initial plan was generally correct, but `any` was not a valid type annotation and rejecting cards with additional fields was not required. Checking only whether a path existed could allow a directory to reach the JSON parser. Checking only for empty strings would also accept values containing only whitespace. The Black configuration was necessary because Black defaults to 88 characters while Flake8 defaults to 79 characters. Configuring Black to use 79 characters removed the formatter and linter conflict without changing Flake8's default behavior.

**Outcome:** All 17 loader tests passed. `utils/flashcard_loader.py` achieved 100% test coverage with 49 statements and no missing lines. Black, Flake8, and mypy completed successfully for the loader and its tests.

**Lessons Learned:** 
- A focused prompt with explicit failure cases produces more reliable AI-generated code
- AI-generated plans still require review for typing, validation, and scope accuracy
- Every functional requirement should be connected to at least one test
- Formatter and linter settings must be compatible to avoid repeated formatting conflicts

---

### 2026-11-04 - Strategy Pattern for Quiz Modes

**Context:** The application required three interchangeable quiz-ordering algorithms: sequential, random, and adaptive. The implementation needed to use the Strategy Pattern for a real architectural purpose while keeping card ordering separate from the future quiz loop, CLI, statistics, and persistence layers.

**AI Tool Used:** Claude Code

**Prompt/Request:** I used a structured XML-style prompt asking Claude Code to plan and implement only the Strategy Pattern in `utils/quiz_modes.py`. The prompt required one abstract strategy interface, three concrete strategies, no mutation of the original card list, type hints, English docstrings, standard-library-only implementation, and no unrelated changes.

**AI Response:** Claude Code proposed `QuizModeStrategy` with a shared `order_cards()` method, plus `SequentialStrategy`, `RandomStrategy`, and `AdaptiveStrategy`. SequentialStrategy returned a copy in original order, RandomStrategy shuffled a copy, and AdaptiveStrategy prioritized missed cards using a defensively-copied set of indices.

**Changes Made:**
- Required the abstract `order_cards()` method to raise `NotImplementedError` instead of using `pass`
- Required `AdaptiveStrategy` to defensively copy the supplied `missed_indices` set
- Clarified that negative and out-of-range indices should have no effect
- Reduced the proposed test plan from 19 to 18 tests by combining two duplicate defensive-copy tests
- Required random behavior to be tested deterministically by patching `utils.quiz_modes.random.shuffle`
- Added explicit type annotations to empty card lists in the tests
- Added a targeted `# type: ignore[abstract]` only for the intentional abstract-class instantiation test
- Added `pyproject.toml` with Black configured to use a line length of 79

**Reasoning:** The Strategy Pattern cleanly separates the algorithms used to order flashcards and makes future quiz modes easier to add. Defensive copying prevents later changes to an external set from changing adaptive behavior. Deterministic mocking avoids unreliable tests that assume a random shuffle must change the order. Combining duplicate tests kept the suite focused. The targeted mypy suppression was appropriate because the test intentionally performs an operation that must fail at runtime. Configuring Black to use 79 characters aligned it with Flake8's default line-length rule.

**Outcome:** All 18 Strategy Pattern tests passed. `utils/quiz_modes.py` achieved 96% coverage with 26 statements and one uncovered abstract-method line. The complete test suite passed with 35 tests. Combined coverage for the current `utils` package reached 99% with 75 statements and one missing line. Black, Flake8, and mypy completed successfully for all seven current Python source files.

**Lessons Learned:**
- A design pattern should address a real variation point rather than be added only to satisfy a rubric
- Random behavior should be tested with controlled mocking instead of probabilistic assertions
- Defensive copying can be verified through public behavior without accessing private attributes
- Static type checks may require narrow test-specific suppressions for intentionally invalid operations
- Formatter and linter conflicts should be resolved through one consistent project configuration

---

### 2026-11-04 - Quiz Engine and Session Statistics

**Context:** The application required a testable quiz engine that presents flashcards, collects answers, provides immediate feedback, calculates session statistics, and preserves the original indices of incorrectly answered cards for future adaptive sessions.

**AI Tool Used:** Claude Code

**Prompt/Request:** I used a structured XML-style prompt asking Claude Code to plan and implement only the Quiz Engine in `utils/quiz_engine.py`. The prompt required dependency injection for input and output, case-insensitive answer comparison, immediate feedback, typed session statistics, reliable original-index tracking, no changes to the existing loader or strategies, and no CLI or persistence implementation.

**AI Response:** Claude Code proposed a `SessionResult` dataclass and a `QuizEngine` class with an injected strategy, input callable, and output callable. The engine orders cards through the selected strategy, presents each card, compares answers, provides feedback, and returns totals, accuracy, missed terms, and missed original indices.

**Changes Made:**
- Rejected direct original-index tracking based only on the caller's dictionary identities because the same dictionary instance could appear multiple times
- Required a separate shallow dictionary copy for every input position before strategy ordering
- Required exact feedback values of `Correct` and `Incorrect`
- Required questions to be presented without an invented prefix or prompt string
- Used `strip().casefold()` for case-insensitive answer comparison
- Added 19 focused Quiz Engine tests covering results, feedback, comparison, statistics, index tracking, empty input, injected callables, and input preservation
- Rejected and removed an out-of-scope AI-generated test that expected support for custom strategies returning newly created card dictionaries
- Added explicit type annotations to two empty card lists in the test suite to satisfy mypy

**Reasoning:** Creating one internal dictionary copy per input position makes original-index tracking reliable even when duplicate card content or repeated dictionary references are supplied. Dependency injection keeps terminal input and output testable without introducing global state. The copied-card strategy test was rejected because the approved Strategy contract reorders the supplied card objects rather than replacing them with unrelated objects. Production code should not be expanded only to satisfy an invented test outside the project requirements.

**Outcome:** All 19 Quiz Engine tests passed, and `utils/quiz_engine.py` achieved 100% coverage with 41 statements and no missing lines. The complete test suite passed with 54 tests. Combined coverage for the current `utils` package reached 99% with 116 statements and one missing abstract-method line. Black, Flake8, and mypy completed successfully for all nine current Python source files.

**Lessons Learned:**
- Dependency injection makes interactive command-line logic easy to test
- Original-index tracking must account for duplicate content and repeated object references
- AI-generated tests must be reviewed against the approved interface and project scope
- Production code should not be changed merely to satisfy an invented requirement
- Verified test, coverage, formatter, linter, and type-checking results should be documented immediately

---

### 2026-11-04 - CLI Integration and Summary Output

**Context:** The completed loader, quiz strategies, and quiz engine needed to be integrated into a usable command-line application. The CLI had to support long and short arguments, select the requested quiz mode, handle expected loading errors without a traceback, and display a final session summary.

**AI Tool Used:** Claude Code

**Prompt/Request:** I used a structured XML-style prompt asking Claude Code to plan and implement only the CLI integration in `main.py`. The prompt required `argparse`, required mode and file arguments, all three quiz strategies, explicit exit codes, standard-error output for expected failures, a testable `main()` function, and exact summary labels.

**AI Response:** Claude Code added argument parsing, strategy selection, session-summary output, expected error handling, and the executable `main()` entry point. It integrated the existing loader, quiz-mode strategies, and quiz engine without duplicating their logic.

**Changes Made:**
- Required `parse_arguments()` to accept an optional argument list for direct unit testing
- Simplified `select_strategy()` so adaptive mode starts with an empty missed-index set
- Required expected loading and validation errors to be written to standard error as one line
- Required exact summary labels for total questions, accuracy, and missed terms
- Preserved the original `main.py` module docstring exactly
- Added 16 focused CLI tests covering arguments, strategy selection, summary output, successful execution, expected errors, and component integration
- Formatted `main.py` and `tests/test_main.py` with the project Black configuration

**Reasoning:** Accepting an optional argument list makes argument parsing testable without changing normal command-line behavior. Keeping strategy selection small avoids introducing an unnecessary Factory Pattern. Expected file and validation errors belong on standard error and should return a non-zero exit code without exposing a traceback. Exact summary labels provide predictable output for users and automated tests.

**Outcome:** All 16 CLI tests passed. The complete test suite passed with 70 tests. Total project coverage reached 99% across 688 statements with two missing lines. `main.py` achieved 97% coverage. Black, Flake8, and mypy completed successfully for all ten current Python source files. The `python main.py --help` command displayed the required mode and file options.

**Lessons Learned:**
- Small orchestration functions make CLI behavior easier to test
- Expected user errors should produce concise standard-error messages and appropriate exit codes
- CLI tests should validate both long and short argument forms
- Existing application components should be integrated rather than reimplemented
- A technically passing implementation is not complete until real CLI smoke tests and documentation are also verified

---

## Tips for Effective AI Collaboration

### 1. Be Specific in Your Requests
- ❌ "Write a function"
- ✅ "Write a function that validates email addresses using regex, returns a boolean, and includes proper error handling"

### 2. Provide Context
- Include relevant code snippets
- Explain the larger goal
- Mention any constraints or requirements

### 3. Review and Understand
- Never copy AI code without understanding it
- Ask for explanations of complex logic
- Test the code before accepting it

### 4. Iterate and Refine
- Use follow-up questions to improve the code
- Ask for alternative implementations
- Request code reviews and suggestions

### 5. Document Your Process
- Keep detailed notes in this log
- Explain your decision-making process
- Track what works and what doesn't

## Common AI Collaboration Patterns

### Code Generation
- Initial implementation of classes/functions
- Boilerplate code creation
- Test case generation

### Code Review
- Ask AI to review your code for issues
- Request suggestions for improvements
- Get feedback on code structure

### Problem Solving
- Debugging help
- Algorithm suggestions
- Architecture advice

### Learning and Explanation
- Ask for explanations of complex concepts
- Request examples of design patterns
- Get guidance on best practices

## Reflection Questions

As you work through the project, consider these questions:

1. **What types of tasks did AI help with most effectively?**
2. **Where did you need to make the most modifications to AI suggestions?**
3. **What patterns did you notice in AI strengths and weaknesses?**
4. **How did your prompting technique improve over time?**
5. **What would you do differently in future AI collaborations?**

## Summary Statistics

At the end of your project, fill out these statistics:

- **Total AI interactions:** ___
- **Lines of AI-generated code used:** ___
- **Lines of AI-generated code modified:** ___
- **Most helpful AI interaction:** ___
- **Most challenging AI interaction:** ___
- **Biggest lesson learned:** ___

---

**Note:** This log is a required component of your final project report. Be thorough and honest in your documentation to demonstrate your learning process and AI collaboration skills.