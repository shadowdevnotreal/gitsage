# GitSage Tests

This directory is reserved for future test implementation.

## Planned Test Structure

```
tests/
├── test_launcher.py          # Tests for launcher.py
├── test_repo_manager.py      # Tests for bash scripts (via subprocess)
├── test_wiki_generator.py    # Tests for wiki generation
└── conftest.py               # Pytest configuration and fixtures
```

## Running Tests

Once tests are implemented, run them with:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_launcher.py
```

## Contributing Tests

When adding tests:

1. Follow pytest conventions
2. Use descriptive test names (test_feature_does_something)
3. Include docstrings explaining what is being tested
4. Aim for >80% code coverage
5. Test both success and failure cases

## Current Status

**v1.0**: No tests implemented yet. Test structure planned for v2.0.

See ROADMAP.md for test implementation timeline.
