---
name: project-bootstrap
description: Analyze a project and set up Claude Code configuration following Techne best practices. Use when the user asks to set up Claude Code for a project, bootstrap a new repo, configure CLAUDE.md, set up hooks, or mentions "project-bootstrap". Also triggers on "set up my repo for Claude", "configure Claude Code", "bootstrap this project", or "initialize Claude config".
---

# Project Bootstrap

Analyze a project and set up Claude Code configuration (CLAUDE.md, hooks, MCP servers, settings) following Techne best practices.

## Prerequisites

This skill creates and modifies files. Confirm with the user before proceeding if running in an existing project with uncommitted changes.

## Step 1: Project Analysis

Analyze the repository to understand:

1. **Tech stack** -- Read package.json, requirements.txt, Cargo.toml, go.mod, Gemfile, or equivalent. Note languages, frameworks, and key dependencies.
2. **Project structure** -- Glob for source directories, test directories, config files, CI pipelines.
3. **Existing Claude config** -- Check for CLAUDE.md, .claude/, .mcp.json. Note what already exists.
4. **Git workflow** -- Check for branch protection patterns, PR templates, conventional commits.
5. **Testing setup** -- Identify test runner, test location conventions, coverage tools.
6. **CI/CD** -- Check .github/workflows/, .gitlab-ci.yml, Jenkinsfile, etc.

Store analysis as `project_analysis` for use in subsequent steps.

## Step 2: Generate CLAUDE.md

Using the project analysis, generate a CLAUDE.md at the repo root. Use the template in [references/claude-md-template.md](references/claude-md-template.md) as a starting point, filling in project-specific details:

- Tech stack and versions
- Build, test, lint commands (exact commands from package.json scripts, Makefile targets, etc.)
- Architecture overview (inferred from directory structure)
- Code style conventions (inferred from linter configs, existing code)
- Branch and PR workflow (inferred from CI config, existing branches)
- Testing instructions (exact test commands, where to add new tests)

If a CLAUDE.md already exists, read it first and propose additions rather than overwriting. Show the user what will be added and get confirmation.

Write the file to `CLAUDE.md` at the repo root.

## Step 3: Configure Hooks and Deny Rules

Set up safety guardrails in `.claude/settings.json` (or `.claude/settings.local.json` for personal preferences). Use the recommendations in [references/recommended-hooks.md](references/recommended-hooks.md).

**Always configure these deny rules:**
- Block `git push --force` and `git push -f`
- Block writing `.env`, `.pem`, `.key` files

**Recommend these hooks based on project analysis:**
- If linter detected: PostToolUse hook to auto-lint after file edits
- If test runner detected: Suggest running tests after implementation changes
- UserPromptSubmit hook for context injection if applicable

Present the proposed configuration to the user and get confirmation before writing.

## Step 4: Configure MCP Servers

Check if `.mcp.json` exists. Based on the tech stack, recommend MCP servers from [references/recommended-mcp.md](references/recommended-mcp.md).

Common recommendations:
- **Context7** -- for any project (documentation retrieval)
- **Database MCP** -- if database connection strings or ORMs detected
- **GitHub MCP** -- if .github/ directory exists

Present recommendations and let the user choose which to configure. Write selected servers to `.mcp.json`.

## Step 5: Marketplace Configuration

Add the Techne public marketplace to `.claude/settings.json` so the user can discover and install more plugins:

```json
{
  "extraKnownMarketplaces": {
    "techne-ai-agent-tools": {
      "source": {
        "source": "github",
        "repo": "Techne-Analytics/techne-ai-agent-tools"
      }
    }
  }
}
```

Merge with existing settings if the file already exists.

## Step 6: Summary Checklist

Output a summary of everything configured:

```markdown
## Project Bootstrap Complete

### Configured
- [ ] CLAUDE.md -- generated at repo root with {N} sections
- [ ] Deny rules -- {list of deny rules configured}
- [ ] Hooks -- {list of hooks configured, or "none recommended"}
- [ ] MCP servers -- {list of servers configured, or "none configured"}
- [ ] Marketplace -- Techne marketplace added to settings

### Manual Steps Remaining
- [ ] Review CLAUDE.md and adjust any inferred details
- [ ] Add ANTHROPIC_API_KEY if using Claude Code in CI
- [ ] Configure branch protection on main (require PR, require CI)
- [ ] Commit the new configuration files
```

## Output Contract

The final output shown to the user should include:
1. The project analysis summary
2. Each configuration file created/modified with a diff or preview
3. The summary checklist
4. A recommendation to commit the changes

## What This Skill Does NOT Do

- It does not install plugins (it adds the marketplace so the user can install later)
- It does not run tests or CI
- It does not push code or create PRs
- It does not configure secrets or credentials
- It does not modify source code -- only Claude Code configuration files
