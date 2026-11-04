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
- Added `.flake8` with a maximum line length of 88 to match Black's default formatting
- Added 17 focused unit tests covering valid inputs, malformed JSON, invalid structures, missing fields, invalid types, empty values, whitespace-only values, additional fields, missing files, and directory paths

**Reasoning:** The initial plan was generally correct, but `any` was not a valid type annotation and rejecting cards with additional fields was not required. Checking only whether a path existed could allow a directory to reach the JSON parser. Checking only for empty strings would also accept values containing only whitespace. The Flake8 configuration was necessary because Black formats code using an 88-character line length while Flake8 defaults to 79 characters.

**Outcome:** All 17 loader tests passed. `utils/flashcard_loader.py` achieved 100% test coverage with 49 statements and no missing lines. Black, Flake8, and mypy completed successfully for the loader and its tests.

**Lessons Learned:** 
- A focused prompt with explicit failure cases produces more reliable AI-generated code
- AI-generated plans still require review for typing, validation, and scope accuracy
- Every functional requirement should be connected to at least one test
- Formatter and linter settings must be compatible to avoid repeated formatting conflicts

---

### [Date] - [Brief Description]

**Context:** 

**AI Tool Used:** 

**Prompt/Request:** 

**AI Response:** 

**Changes Made:** 

**Reasoning:** 

**Outcome:** 

**Lessons Learned:** 

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