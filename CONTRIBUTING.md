# Contributing Guidelines

## Welcome!

Thank you for interest in contributing to Todo Backend! This document provides guidelines and instructions for contributing.

## Getting Started

### Prerequisites
- Python 3.10+
- Git
- Code editor (VS Code recommended)
- Docker & Docker Compose (optional, for containerized development)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd todo-backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Update .env with your values
   ```

5. **Start development server**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the application**
   - Frontend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Development Standards

### Code Style

- Follow [PEP 8](https://pep8.org/) for Python code
- Use `.editorconfig` settings for consistent formatting
- Use meaningful variable and function names
- Keep functions focused and modular

### Docstrings

All functions and classes must include docstrings:

```python
def create_todo(todo: TodoCreate, current_user: str = Depends(get_current_user)) -> Todo:
    """
    Create a new todo (requires authentication)
    
    Args:
        todo: Todo data to create
        current_user: Authenticated user
        
    Returns:
        Created todo with ID and timestamps
    """
```

### Comments

- Use comments for WHY, not WHAT
- Keep comments up-to-date with code
- Avoid obvious comments

### Imports

Organize imports in this order:
1. Standard library
2. Third-party libraries
3. Local application imports

```python
import logging
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

from app.core.config import settings
```

### Logging

Use appropriate log levels:
```python
logger.debug("Detailed debug information")
logger.info("Informational messages")
logger.warning("Warning messages")
logger.error("Error messages")
```

## Git Workflow

### Branch Naming

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation changes
- `refactor/description` - Code refactoring

Example: `feature/add-pagination` or `bugfix/fix-token-validation`

### Commit Messages

Follow conventional commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Example:
```
feat(auth): add JWT token refresh endpoint

Add ability to refresh expired tokens without re-authentication.
Implement refresh token rotation for enhanced security.

Closes #123
```

### Pull Requests

- Create a descriptive title
- Reference related issues
- Add changelog entry
- Test thoroughly before submitting

## Testing

### Running Tests

```bash
# Unit tests (when available)
pytest

# Check code style
flake8 app/

# Type checking
mypy app/
```

### Test Requirements

- Write tests for new features
- Maintain existing test coverage
- Test error cases and edge cases

## Adding Features

### Authentication Features
- Update `app/auth/` modules
- Test with demo credentials
- Update README with new endpoints

### Todo Features
- Update `app/api/routes.py`
- Update Pydantic models in `app/models/`
- Publish Kafka events for new types
- Add frontend UI if applicable

### Frontend Changes
- Update HTML templates in `static/`
- Update CSS in `static/css/style.css`
- Update JavaScript in `static/js/`
- Test responsiveness on mobile

## Documentation

### README Updates
- Document new endpoints with examples
- Update setup instructions if needed
- Update troubleshooting section

### Code Documentation
- Add docstrings to new functions
- Update inline comments if logic changes
- Keep README.md synchronized with code

## Submitting Changes

1. **Fork and branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make changes**
   - Follow style guidelines
   - Write/update tests
   - Update documentation

3. **Commit**
   ```bash
   git commit -m "feat: add new feature"
   ```

4. **Push**
   ```bash
   git push origin feature/your-feature
   ```

5. **Create Pull Request**
   - Reference related issues
   - Provide clear description
   - Request review

## Release Process

### Version Numbering
Follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH` (e.g., 2.0.0)

### Release Steps
1. Update version in `app/core/config.py`
2. Update `CHANGELOG.md`
3. Create git tag: `git tag v2.0.0`
4. Push tag: `git push origin v2.0.0`
5. Create GitHub release with changelog

## Code Review Guidelines

### Reviewers Should Check

- [ ] Code follows style guidelines
- [ ] Docstrings are present and clear
- [ ] Tests are included for new code
- [ ] No security vulnerabilities
- [ ] Performance impact is considered
- [ ] Documentation is updated
- [ ] No commented-out code left behind

### Authors Should

- [ ] Self-review code before submitting
- [ ] Provide context and reasoning
- [ ] Respond to feedback promptly
- [ ] Keep commits focused and logical

## Security Guidelines

- Never commit `.env` file
- Use environment variables for secrets
- Validate all user inputs
- Use parameterized queries (when database is added)
- Keep dependencies updated
- Follow authentication best practices

## Performance Considerations

- Optimize database queries (when database is added)
- Implement caching where appropriate
- Use async/await for I/O operations
- Profile code before optimization

## Questions or Issues?

- Create an issue on GitHub
- Start a discussion
- Contact maintainers

## License

By contributing, you agree that your contributions will be licensed under the project's license.

---

**Thank you for contributing! 🚀**
