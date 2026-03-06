# CLAUDE.md Template

Use this as a starting point. Fill in project-specific details from the analysis.

## Sections to Include

### Tech Stack
- Language and version (e.g., Python 3.11+, Node 20, Rust 1.75)
- Key frameworks and libraries
- Package manager

### Build & Test Commands
- How to install dependencies
- How to run tests (exact command)
- How to lint/format (exact command)
- How to build (if applicable)

### Architecture
- Directory structure overview
- Key modules and their responsibilities
- Data flow (if applicable)

### Code Style
- Naming conventions
- Import ordering
- Formatting tool and config

### Branch & PR Workflow
- Branch naming convention (feat/, fix/, docs/, etc.)
- Commit message format (conventional commits recommended)
- PR requirements (reviews, CI, testing plan)

### Testing
- Test runner and framework
- Where to put new tests
- How to run a single test
- Coverage expectations (if any)

### CI/CD
- CI system and key workflows
- How to check CI status
- Deploy process (if applicable)

### Agent Safety Rules
- Do not merge PRs unless the user explicitly asks
- Do not deploy unless the user explicitly asks
- Do not force-push to main
- Do not commit sensitive files (.env, credentials, keys)

## Example

```markdown
# CLAUDE.md -- {Project Name}

## Tech Stack
- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Testing**: pytest
- **CI**: GitHub Actions

## Build & Test
\`\`\`bash
pip install -r requirements-dev.txt  # install deps
pytest tests/ -v                      # run tests
ruff check .                          # lint
\`\`\`

## Architecture
- `src/` -- application source
- `tests/` -- pytest test suite
- `docs/` -- documentation

## Code Style
- Conventional commits: feat(), fix(), docs(), chore()
- Ruff for linting and formatting

## Branch Workflow
1. Branch from main: feat/, fix/, docs/
2. Open PR with testing plan
3. CI must pass before merge
```
