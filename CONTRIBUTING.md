# Contributing to SmartGen

Thank you for your interest in contributing to SmartGen! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the behavior
- **Expected behavior** vs **actual behavior**
- **Environment details** (OS, Python version, SmartGen version)
- **Error messages** or logs
- **Screenshots** if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating a suggestion, include:

- **Clear title and description**
- **Use case**: Why is this feature useful?
- **Proposed solution** (if you have one)
- **Alternatives considered**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the coding standards below
3. **Add tests** for new functionality
4. **Update documentation** as needed
5. **Ensure all tests pass** and linting checks pass
6. **Submit a pull request** with a clear description

## Development Setup

### Prerequisites

- Python 3.12 or higher
- Git
- (Optional) Ollama for local LLM testing

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/smartgen.git
cd smartgen

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Verify installation
smartgen --help
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=smartgen --cov-report=html

# Run specific test file
pytest tests/test_cli.py
```

### Linting and Formatting

```bash
# Check linting
ruff check .

# Auto-fix linting issues
ruff check . --fix

# Check code formatting
black --check .

# Format code
black .

# Type checking
mypy src/
```

## Coding Standards

### Python Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guide
- Use [Black](https://black.readthedocs.io/) for code formatting (line length: 88)
- Use [Ruff](https://docs.astral.sh/ruff/) for linting
- Type hints are encouraged (use `mypy` for type checking)

### Code Organization

```
smartgen/
├── src/smartgen/
│   ├── cli.py              # CLI entry point
│   ├── config.py           # Configuration management
│   ├── commands/           # CLI command implementations
│   ├── services/           # Core business logic
│   └── policies/           # DDD policy files
├── tests/                  # Test files
└── examples/              # Example projects
```

### Documentation

- **Docstrings**: All public functions, classes, and methods must have docstrings
- **Type Hints**: Use type hints for function parameters and return values
- **Comments**: Add comments for complex logic or business rules
- **README Updates**: Update readme.md for user-facing changes

### Testing

- Write tests for new features
- Aim for good test coverage (>80%)
- Use descriptive test names
- Follow Arrange-Act-Assert pattern
- Mock external dependencies (LLM calls, file I/O)

**Example:**
```python
def test_generate_entity_creates_correct_structure():
    # Arrange
    entity_name = "User"
    domain = "users"
    
    # Act
    result = generate_entity(entity_name, domain)
    
    # Assert
    assert result.entity_file.exists()
    assert "class User" in result.entity_file.read_text()
```

## Commit Messages

Use clear, descriptive commit messages:

- Start with a verb in imperative mood (e.g., "Add", "Fix", "Update")
- Reference issue numbers when applicable
- Keep the first line under 72 characters
- Add detailed description if needed

**Examples:**
```
Add support for TypeScript entity generation

- Implement TypeScript template engine
- Add tests for TypeScript generation
- Update documentation

Closes #45
```

```
Fix JSON parsing error in domain generator

Handle cases where LLM wraps JSON in markdown code blocks.

Fixes #123
```

## Adding New Features

### Adding a New Generator

1. Create a new generator class in `src/smartgen/services/`
2. Implement the generator interface
3. Add CLI command in `src/smartgen/commands/generate.py`
4. Create templates in `src/smartgen/policies/` if needed
5. Add tests in `tests/`
6. Update documentation

### Adding Language Support

1. Create language-specific templates in `src/smartgen/policies/ddd/{language}/`
2. Add language to CLI choices
3. Implement language-specific generator logic
4. Add tests
5. Update documentation with examples

### Adding LLM Provider Support

1. Add provider detection logic in `services/domain_generator.py`
2. Implement provider-specific API calls
3. Add configuration options
4. Add tests with mocked responses
5. Update documentation

## Project Structure

### Core Components

- **CLI (`cli.py`)**: Main entry point, command routing
- **Commands (`commands/`)**: Individual command implementations
- **Services (`services/`)**: Core business logic (generators, LLM calls)
- **Config (`config.py`)**: Configuration management
- **Policies (`policies/`)**: DDD policy files used for generation

### Adding New Commands

1. Create command function in `commands/` directory
2. Register command in `cli.py`
3. Add command documentation to readme
4. Add tests

## Pull Request Process

1. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and commit:
   ```bash
   git add .
   git commit -m "Add your feature"
   ```

3. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request** on GitHub:
   - Provide a clear title and description
   - Reference related issues
   - Include screenshots if UI changes
   - Ensure CI checks pass

5. **Respond to feedback** and make requested changes

## Review Process

- Maintainers will review your PR
- Address any feedback or requested changes
- Ensure all CI checks pass
- Once approved, your PR will be merged

## Questions?

- Open an issue for questions or clarifications
- Check existing issues and discussions
- Review the [readme](readme.md) for usage examples

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing to SmartGen!
