# CLAUDE.md -- Techne AI Agent Tools

Public plugin marketplace for Claude Code. Contains reusable plugins, patterns, and templates for AI-agent-assisted development.

## Tech Stack

- **Language**: Python 3.11+
- **Testing**: pytest
- **Data formats**: YAML, JSON, Markdown
- **CI**: GitHub Actions

## File Organization

```
plugins/        -- Claude Code plugins (audit-claude, project-bootstrap)
patterns/       -- Implementation patterns with trade-offs
templates/      -- Project bootstrap templates
scripts/        -- Validation and automation scripts
tests/          -- pytest test suite
```

## Build & Test

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

make validate-plugins   # validate marketplace and plugin structure
make test               # run full test suite
make test-skills-spec   # validate skill structure
```

## Branch & PR Workflow

1. Branch from main: `feat/`, `fix/`, `docs/`, `chore/`
2. Conventional commits: `feat(scope):`, `fix(scope):`, `docs(scope):`
3. All changes require a PR -- no direct commits to main
4. CI must pass before merge
5. Include a testing plan in every PR body

## Adding a New Plugin

1. Create `plugins/<name>/.claude-plugin/plugin.json`
2. Add command in `plugins/<name>/commands/<name>.md`
3. Add skill in `plugins/<name>/skills/<name>/SKILL.md`
4. Add entry to `.claude-plugin/marketplace.json`
5. Add spec test in `tests/skills/test_<name>_spec.py`
6. Run `make validate-plugins && make test`

## Agent Safety Rules

Deny rules enforced in `.claude/settings.json`:
- `git push --force` / `git push -f` — blocked
- Writing `.env`, `.pem`, `.key` files — blocked

Additional rules:
- Do not merge PRs unless the user explicitly asks
- Do not force-push to main
- Do not commit sensitive files (.env, credentials, keys)

## Compliance

This repo follows SOC 2-ready practices. Run `/compliance-github-auditor` against it to verify. See the internal `agentic-ai-tooling` repo for full compliance tooling.
