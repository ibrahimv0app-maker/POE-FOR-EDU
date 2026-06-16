# Contributing to POE-EDU

## Welcome! 👋

Thank you for your interest in contributing to **POE-EDU**. This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

All contributors must adhere to the following principles:

- **Respect**: Treat all contributors with respect and courtesy
- **Educational Focus**: Keep contributions aligned with educational purposes
- **Legal Compliance**: Ensure all contributions comply with applicable laws and terms of service
- **Ethical Use**: Reject contributions that promote harmful, illegal, or unethical activities

## How to Contribute

### 1. **Report Bugs**

If you find a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs. actual behavior
- Screenshots (if applicable)
- Your environment (Python version, OS, etc.)

### 2. **Suggest Features**

We welcome feature suggestions! Please include:
- Use case and motivation
- Proposed implementation (if you have ideas)
- Any potential drawbacks or considerations

### 3. **Submit Pull Requests**

#### Before Starting:
1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Set up your development environment

#### Development Guidelines:
- Follow PEP 8 style guide for Python
- Write clear, descriptive commit messages
- Include comments for complex logic
- Add docstrings to functions and classes
- Test your changes locally

#### Commit Message Format:
```
[type]: Short description

Detailed explanation if needed

Related to #issue_number (if applicable)
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

#### Before Submitting:
1. Ensure all tests pass: `pytest`
2. Check code quality: `pylint`
3. Update documentation if needed
4. Rebase on main: `git rebase origin/main`

### 4. **Documentation Improvements**

Documentation is crucial! You can help by:
- Fixing typos or unclear sections
- Improving code examples
- Adding tutorials or guides
- Translating documentation

## Development Setup

```bash
# Clone the repository
git clone https://github.com/ibrahimv0app-maker/POE-FOR-EDU.git
cd POE-FOR-EDU

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Run the application
uvicorn app:app --reload
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_chat.py
```

## Code Style

```bash
# Format code with black
black .

# Check with pylint
pylint src/

# Type checking with mypy
mypy src/
```

## Questions?

- Open an issue with the `question` label
- Check existing discussions
- Review the documentation

## License

By contributing to POE-EDU, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🚀
