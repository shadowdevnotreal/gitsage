# Contributing to GitHub Repository Manager

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Requests
Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/github-repo-manager.git
   cd github-repo-manager
   ```

2. **Install prerequisites**
   - Git: https://git-scm.com/
   - GitHub CLI: https://cli.github.com/
   - Python 3.6+: https://python.org/

3. **Set up development environment**
   ```bash
   # Create virtual environment (optional but recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install development dependencies
   pip install -r requirements-dev.txt
   ```

4. **Run tests**
   ```bash
   python -m pytest tests/
   ```

## Contribution Guidelines

### Code Style
- **Bash scripts**: Follow standard bash conventions
  - Use `set -e` for error handling
  - Include comments for complex logic
  - Use meaningful function and variable names
  
- **Python code**: Follow PEP 8
  - Use type hints where appropriate
  - Include docstrings for functions and classes
  - Maximum line length: 88 characters (Black formatter)
  
- **PowerShell scripts**: Follow PowerShell best practices
  - Use approved verbs for function names
  - Include comment-based help
  - Use proper error handling

### Documentation
- Update relevant documentation for any changes
- Include examples for new features
- Update the CHANGELOG.md for notable changes

### Commit Messages
Use clear and meaningful commit messages:
```
feat: add bulk repository deletion feature
fix: resolve authentication issue on Windows
docs: update installation guide for macOS
refactor: improve error handling in deletion script
```

## Bug Reports

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

### Bug Report Template
```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment (please complete the following information):**
- OS: [e.g. Windows 10, macOS 11.6, Ubuntu 20.04]
- Git version: [e.g. 2.33.0]
- GitHub CLI version: [e.g. 2.0.0]
- Python version: [e.g. 3.9.7]

**Additional context**
Add any other context about the problem here.
```

## Feature Requests

We welcome feature requests! Please provide:

- **Use case**: Describe the problem you're trying to solve
- **Proposed solution**: How you envision the feature working
- **Alternatives considered**: Other solutions you've considered
- **Additional context**: Screenshots, mockups, examples, etc.

## Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_deletion.py

# Run with coverage
python -m pytest --cov=scripts tests/
```

### Writing Tests
- Add tests for new features
- Update tests when changing existing functionality
- Ensure tests cover both success and failure cases
- Mock external dependencies (GitHub API calls, file system operations)

### Test Structure
```
tests/
├── test_deletion.py          # Tests for deletion functionality
├── test_history_reset.py     # Tests for Git history reset
├── test_environment.py       # Tests for environment detection
├── test_gui.py              # Tests for GUI components
└── fixtures/                # Test data and fixtures
```

## Platform-Specific Contributions

### Windows
- Test on both Command Prompt and PowerShell
- Ensure compatibility with Git Bash and WSL
- Test both Python launcher and batch file

### macOS
- Test on multiple macOS versions
- Verify Homebrew installation paths work correctly
- Test with both bash and zsh shells

### Linux
- Test on major distributions (Ubuntu, CentOS, Arch)
- Verify package manager installation instructions
- Test with different shells (bash, zsh, fish)

## Code of Conduct

### Our Pledge
We are committed to making participation in this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards
Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Enforcement
Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances.

## Questions?

Don't hesitate to ask questions! You can:

- Open an issue with the "question" label
- Start a discussion in GitHub Discussions
- Reach out to maintainers directly

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for notable contributions
- README.md contributors section
- GitHub contributors graph

Thank you for contributing to GitHub Repository Manager! 🎉
