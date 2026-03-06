# Setting Up Automated Auditing with GitHub Actions

This guide explains how to run the `audit-claude` skill automatically on a schedule using GitHub Actions.

## Overview

The workflow:
1. Runs on a weekly schedule (configurable)
2. Invokes Claude Code in headless mode
3. Runs the audit-claude skill
4. Files a GitHub issue with the findings
5. Optionally creates follow-up issues for critical findings

## Prerequisites

- **Claude Code CLI** installed in the GitHub Actions runner
- **ANTHROPIC_API_KEY** stored as a repository secret
- **GitHub token** with issue write permissions (the default `GITHUB_TOKEN` works)
- The `audit-report` label must exist on the repo (the audit skill creates it if missing)

## Installation

1. Copy the sample workflow from `scripts/audit-claude-action.yml` to your repo:

   ```bash
   mkdir -p .github/workflows
   cp scripts/audit-claude-action.yml .github/workflows/audit-claude.yml
   ```

2. Add your Anthropic API key as a repository secret:
   - Go to Settings > Secrets and variables > Actions
   - Create a new secret named `ANTHROPIC_API_KEY`
   - Paste your API key

3. (Optional) Adjust the cron schedule in the workflow file. Default is weekly on Monday at 9:00 UTC.

4. Commit and push the workflow file.

## How It Works

The GitHub Action first checks whether an `ANTHROPIC_API_KEY` secret is configured. If the key is missing, the action creates a GitHub issue prompting you to either run `/audit-claude` locally in Claude Code or configure the API key for automated runs. It will not create duplicate reminder issues.

If the key is present, the action runs Claude Code with the `--print` flag (headless, non-interactive mode) and passes a prompt that invokes the audit-claude skill. Claude Code reads the repository, runs both sub-skill audits, performs the AI-first readiness review, compares against previous audit issues, and files a new GitHub issue with the results.

Because the action uses `--print` mode, Claude cannot ask interactive questions. The audit skill is designed to run fully autonomously -- it handles missing labels, missing previous audits, and other edge cases without user input.

## Customization

### Schedule

Edit the cron expression in the workflow:

```yaml
schedule:
  - cron: '0 9 * * 1'  # Every Monday at 9:00 UTC
```

Common alternatives:
- `'0 9 * * 1,4'` -- Monday and Thursday (twice weekly)
- `'0 9 1 * *'` -- First day of each month
- `'0 9 * * *'` -- Daily

### Model selection

The default workflow uses `claude-sonnet-4-20250514`. For more thorough audits, you can switch to `claude-opus-4-20250514` by changing the `--model` flag in the workflow, though this increases cost.

### Additional context

If your repo has specific areas to focus on, you can customize the prompt in the workflow file. For example:

```yaml
- name: Run audit
  run: |
    claude --print --model claude-sonnet-4-20250514 \
      "Run the audit-claude skill. Pay special attention to the /api and /workers directories."
```

## Troubleshooting

**Audit fails with "skill not found"**: Make sure the audit-claude skill is installed. Either install it globally (`~/.claude/skills/audit-claude/`) or include it in the repo (`.claude/skills/audit-claude/`).

**No GitHub issue created**: Check that the `GITHUB_TOKEN` has `issues: write` permission. The default token should work, but custom tokens may need this scope added.

**Sub-skills not available**: The `claude-md-management` and `claude-code-setup` plugins need to be available in the CI environment. If running in a container, ensure plugins are pre-installed or use a setup step.

**Rate limiting**: If running frequently, you may hit GitHub API rate limits when searching issue history. The skill fetches at most 5 previous audit issues, so this is unlikely unless you have other automation hitting the API.
