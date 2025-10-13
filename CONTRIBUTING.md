# Contributing to Jane Monorepo

Thank you for your interest in contributing to the Jane Monorepo! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Development Workflow](#development-workflow)
- [Branching Strategy](#branching-strategy)
- [Pull Request Process](#pull-request-process)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Commit Message Format](#commit-message-format)

## Development Workflow

### 1. Setting Up Your Environment

```bash
# Clone the repository
git clone https://github.com/your-org/jane-monorepo.git
cd jane-monorepo

# Install dependencies
make install

# Or manually:
npm install
pip install -r apps/jane-orchestrator/requirements.txt
pip install -r apps/cyber-llm-server/requirements.txt
pip install -r apps/mtg-llm-server/requirements.txt
pip install -r apps/code-llm-server/requirements.txt
```

### 2. Running Development Environment

```bash
# Start all services with Docker Compose
make dev

# Or run individual services
npx nx serve jane-ui
npx nx serve jane-orchestrator
npx nx serve cyber-llm-server
npx nx serve mtg-llm-server
npx nx serve code-llm-server
```

### 3. Making Changes

1. Create a new branch from `main`
2. Make your changes
3. Write or update tests
4. Run linters and tests
5. Commit your changes
6. Push your branch
7. Open a pull request

## Branching Strategy

We follow a **trunk-based development** strategy with short-lived feature branches.

### Branch Naming Convention

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring
- `test/description` - Test additions or updates
- `chore/description` - Maintenance tasks

### Examples

```
feature/add-user-authentication
fix/orchestrator-timeout-issue
docs/update-deployment-guide
refactor/extract-logging-utility
test/add-ui-component-tests
chore/update-dependencies
```

## Pull Request Process

### Before Submitting

1. **Update your branch** with the latest changes from `main`:
   ```bash
   git checkout main
   git pull origin main
   git checkout your-branch
   git rebase main
   ```

2. **Run linters**:
   ```bash
   make lint
   ```

3. **Run tests**:
   ```bash
   make test
   ```

4. **Build the project**:
   ```bash
   make build
   ```

5. **Run affected commands** (if applicable):
   ```bash
   make affected-build
   make affected-test
   make affected-lint
   ```

### Pull Request Template

When opening a PR, include:

- **Description**: Clear explanation of what changes were made and why
- **Related Issues**: Link to any related issues (e.g., "Closes #123")
- **Type of Change**: Feature, fix, docs, refactor, etc.
- **Testing**: How the changes were tested
- **Screenshots**: For UI changes
- **Breaking Changes**: Any breaking changes and migration steps

### Review Process

1. At least one approval required from a maintainer
2. All CI checks must pass
3. No merge conflicts
4. All conversations resolved

## Code Style Guidelines

### TypeScript/JavaScript

- Use TypeScript for all new code
- Follow ESLint rules (`.eslintrc.json`)
- Use Prettier for formatting (`.prettierrc`)
- Prefer functional components with hooks
- Use NX path aliases for imports (e.g., `@jane-monorepo/shared/types`)

```typescript
// Good
import { UserType } from '@jane-monorepo/shared/types';
import { formatDate } from '@jane-monorepo/shared/utils';

// Bad
import { UserType } from '../../../libs/shared/types';
```

### Python

- Follow PEP 8 style guide
- Use type hints for all function signatures
- Use Black for formatting
- Use exact version pinning in requirements.txt (==, not >= or ~)

```python
# Good
def process_data(input_data: List[str]) -> Dict[str, Any]:
    """Process input data and return results."""
    pass

# requirements.txt
fastapi==0.115.0
uvicorn==0.34.2
```

### General Guidelines

- Write clear, self-documenting code
- Add comments for complex logic
- Keep functions small and focused
- Follow SOLID principles
- Use meaningful variable and function names

## Testing Requirements

### Unit Tests

- All new features must include unit tests
- Aim for >80% code coverage
- Test edge cases and error conditions

```bash
# Run all tests
make test

# Run tests for specific app
npx nx test jane-ui
```

### Integration Tests

- Add integration tests for API endpoints
- Test service interactions
- Verify health checks

### End-to-End Tests

- Add E2E tests for critical user flows
- Use appropriate testing frameworks

## Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Test additions or updates
- `chore`: Maintenance tasks
- `perf`: Performance improvements
- `ci`: CI/CD changes

### Examples

```
feat(orchestrator): add LLM routing logic

Implement intelligent routing to select the appropriate LLM server
based on query type and domain.

Closes #42

---

fix(ui): correct button alignment in header

The login button was misaligned on mobile devices.

---

docs(readme): update installation instructions

Add Python 3.12 requirement and clarify setup steps.
```

## Code Review Guidelines

### For Authors

- Keep PRs small and focused
- Provide context in PR description
- Respond to feedback promptly
- Be open to suggestions

### For Reviewers

- Be respectful and constructive
- Focus on code, not people
- Explain reasoning for suggestions
- Approve when ready, request changes if needed

## Getting Help

- **Documentation**: Check the [docs/](./docs/) folder
- **Issues**: Search existing issues or create a new one
- **Discussions**: Use GitHub Discussions for questions
- **Contact**: Reach out to maintainers

## License

By contributing to this project, you agree that your contributions will be licensed under the project's license.
