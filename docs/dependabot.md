# Dependabot Configuration

This document explains the Dependabot configuration for automated dependency updates in the Jane Monorepo.

## Overview

Dependabot is configured to automatically create pull requests for dependency updates across:
- npm packages (Node.js dependencies)
- pip packages (Python dependencies for all 4 applications)
- GitHub Actions (workflow action versions)

## Configuration Location

The Dependabot configuration is stored in `.github/dependabot.yml`.

## Update Schedule

All dependency ecosystems are checked **weekly on Mondays at 9:00 AM**.

## Ecosystems Monitored

### 1. npm (Node.js)
- **Directory**: `/` (root)
- **Monitored packages**: Next.js, React, TypeScript, NX, ESLint, and all dev dependencies
- **Open PR limit**: 10
- **Labels**: `dependencies`, `npm`

### 2. pip - jane-orchestrator
- **Directory**: `/apps/jane-orchestrator`
- **Monitored packages**: FastAPI, Uvicorn, Pydantic, SQLAlchemy, Django, Requests, HTTPx
- **Open PR limit**: 10
- **Labels**: `dependencies`, `python`

### 3. pip - cyber-llm-server
- **Directory**: `/apps/cyber-llm-server`
- **Monitored packages**: FastAPI, Uvicorn, Pydantic, vLLM, Requests
- **Open PR limit**: 10
- **Labels**: `dependencies`, `python`

### 4. pip - mtg-llm-server
- **Directory**: `/apps/mtg-llm-server`
- **Monitored packages**: FastAPI, Uvicorn, Pydantic, vLLM, Requests
- **Open PR limit**: 10
- **Labels**: `dependencies`, `python`

### 5. pip - code-llm-server
- **Directory**: `/apps/code-llm-server`
- **Monitored packages**: FastAPI, Uvicorn, Pydantic, vLLM, Requests
- **Open PR limit**: 10
- **Labels**: `dependencies`, `python`

### 6. GitHub Actions
- **Directory**: `/` (root)
- **Monitored**: All GitHub Actions used in workflows
- **Open PR limit**: 5
- **Labels**: `dependencies`, `github-actions`

## Ignored Updates

To prevent breaking changes, major version updates are ignored for:

### npm
- `next` - Major version updates ignored
- `react` - Major version updates ignored
- `react-dom` - Major version updates ignored

### Python
- `fastapi` - Major version updates ignored
- `django` - Major version updates ignored
- `pydantic` - Major version updates ignored
- `vllm` - Major version updates ignored

## Commit Message Format

All Dependabot commits follow the format:
```
chore(deps): update <dependency> from <old-version> to <new-version>
```

## Reviewers

All Dependabot PRs are automatically assigned to: `mbarnes-code`

## How It Works

1. **Monday 9:00 AM**: Dependabot checks for updates
2. **PR Creation**: Creates PRs for available updates
3. **CI/CD**: GitHub Actions workflows run automatically
4. **Review**: Assigned reviewer checks the changes
5. **Merge**: After approval, PR can be merged

## Best Practices

1. **Review PRs Promptly**: Check Dependabot PRs within a few days
2. **Test Thoroughly**: Ensure CI/CD passes before merging
3. **Batch Updates**: Consider merging related PRs together
4. **Check Changelogs**: Review breaking changes in major updates
5. **Monitor**: Keep an eye on automated updates

## Manual Override

To manually trigger a dependency check:
1. Go to the repository's **Insights** tab
2. Click **Dependency graph**
3. Click **Dependabot**
4. Click **Check for updates** on the desired ecosystem

## Updating Configuration

To modify the Dependabot configuration:

1. Edit `.github/dependabot.yml`
2. Commit and push changes
3. Dependabot will automatically pick up the new configuration

## Troubleshooting

### Dependabot Not Creating PRs

- Check if you've reached the PR limit
- Verify the configuration syntax is valid
- Check repository permissions

### CI/CD Failing on Dependabot PRs

- Check if tests need updates
- Review breaking changes in the dependency
- Consider ignoring that specific version

## Additional Resources

- [Dependabot Documentation](https://docs.github.com/en/code-security/dependabot)
- [Dependabot Configuration Options](https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file)
- [Security Advisories](https://docs.github.com/en/code-security/security-advisories)
