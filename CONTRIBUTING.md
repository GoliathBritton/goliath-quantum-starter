# Contributing to NQBA Stack

Thank you for your interest in contributing to the NQBA (Neuromorphic Quantum Business Architecture) Stack! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Process](#contribution-process)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Licensing](#licensing)

## Code of Conduct

This project adheres to our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Python 3.9+
- Git
- Docker (for containerized development)
- Node.js 18+ (for frontend components)

### Quick Start

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/goliath-quantum-starter.git
   cd goliath-quantum-starter
   ```

2. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Run tests to verify setup**
   ```bash
   pytest tests/
   ```

## Development Setup

### Environment Configuration

1. **Copy environment template**
   ```bash
   cp .env.example .env
   ```

2. **Configure environment variables**
   ```bash
   # Required for development
   NQBA_ENV=development
   NQBA_DEBUG=true
   NQBA_SECRET_KEY=your-secret-key-here
   
   # Optional: Quantum integration
   DYNEX_API_KEY=your-dynex-key
   DYNEX_ENDPOINT=https://dynex.ai/api
   ```

3. **Database setup**
   ```bash
   # For development, SQLite is used by default
   # For production, configure PostgreSQL/MySQL
   ```

### IDE Configuration

#### VS Code
- Install Python extension
- Configure Python interpreter to use virtual environment
- Install recommended extensions from `.vscode/extensions.json`

#### PyCharm
- Set project interpreter to virtual environment
- Enable type checking
- Configure code style to match project standards

## Contribution Process

### 1. Issue Creation

Before submitting code, please:

- **Search existing issues** to avoid duplicates
- **Use issue templates** for bug reports and feature requests
- **Provide clear descriptions** with reproduction steps
- **Include environment details** and error messages

### 2. Branch Strategy

We use a simplified Git flow:

```bash
# Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/your-feature-name

# For bug fixes
git checkout -b fix/issue-description

# For documentation
git checkout -b docs/description
```

### 3. Development Workflow

1. **Make changes** following code standards
2. **Write/update tests** for new functionality
3. **Update documentation** as needed
4. **Run tests locally** before committing
5. **Commit with clear messages**

### 4. Commit Message Format

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Examples:
```
feat(auth): add multi-factor authentication support
fix(api): resolve rate limiting edge case
docs(readme): update installation instructions
test(quantum): add benchmark tests for QUBO solver
```

### 5. Pull Request Process

1. **Create PR** with clear description
2. **Link related issues** using keywords
3. **Request reviews** from maintainers
4. **Address feedback** and make requested changes
5. **Maintainers merge** after approval

## Code Standards

### Python Standards

- **Style**: Follow PEP 8 with Black formatting
- **Type hints**: Use type annotations for all functions
- **Docstrings**: Use Google-style docstrings
- **Imports**: Group imports (standard library, third-party, local)

### Code Quality Tools

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Security scanning
bandit -r src/

# Run all quality checks
pre-commit run --all-files
```

### Pre-commit Hooks

We use pre-commit hooks for code quality:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## Testing

### Test Structure

```
tests/
├── unit/           # Unit tests
├── integration/    # Integration tests
├── e2e/           # End-to-end tests
├── benchmarks/    # Performance tests
└── fixtures/      # Test data and mocks
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_auth_system.py

# Run with coverage
pytest --cov=src/ --cov-report=html

# Run performance tests
pytest tests/benchmarks/ -m "not slow"

# Run tests in parallel
pytest -n auto
```

### Writing Tests

- **Test naming**: `test_<function_name>_<scenario>`
- **Arrange-Act-Assert**: Structure tests clearly
- **Mock external dependencies**: Use pytest-mock
- **Test edge cases**: Include error conditions
- **Use fixtures**: Share common test setup

## Documentation

### Documentation Standards

- **Clear and concise** writing
- **Code examples** for all APIs
- **Diagrams** for complex concepts
- **Regular updates** with code changes

### Documentation Structure

```
docs/
├── api/           # API documentation
├── architecture/  # System architecture
├── deployment/    # Deployment guides
├── development/   # Developer guides
├── user/          # User guides
└── examples/      # Code examples
```

### Updating Documentation

- **Update docs** when changing APIs
- **Include examples** for new features
- **Review accuracy** of existing content
- **Use consistent formatting**

## Licensing

### License Types

- **Core SDKs & Examples**: Apache License 2.0
- **Server Components**: Business Source License 1.1
- **Documentation**: Creative Commons BY 4.0
- **Brand Assets**: All Rights Reserved

### Contributor License Agreement

By contributing to this project, you agree that:

1. **Your contributions** are your original work
2. **You have the right** to grant the licenses
3. **You understand** the license terms
4. **You grant licenses** as specified in the project license

### Copyright Assignment

- **Individual contributors** retain copyright
- **Corporate contributors** should specify employer
- **License grants** are non-exclusive and perpetual
- **Attribution** is maintained in source code

## Getting Help

### Communication Channels

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and ideas
- **Discord**: For real-time chat (invite link in README)
- **Email**: dev@flyfox.ai for private matters

### Resources

- **API Documentation**: `/docs` endpoint when running locally
- **Architecture Guide**: `docs/architecture/`
- **Development Guide**: `docs/development/`
- **Contributor FAQ**: `docs/contributing/faq.md`

## Recognition

### Contributors

- **Code contributors** are listed in GitHub contributors
- **Documentation contributors** are acknowledged in docs
- **Bug reporters** are credited in release notes
- **Security researchers** are recognized in security policy

### Hall of Fame

- **Top contributors** get special recognition
- **Long-term contributors** receive maintainer status
- **Security researchers** are added to security hall of fame
- **Community leaders** get ambassador status

---

**Thank you for contributing to NQBA Stack!**

Your contributions help build the operating system of the intelligence economy. Together, we're creating the future of quantum-powered business automation.

For questions about contributing, please open an issue or contact us at dev@flyfox.ai.
