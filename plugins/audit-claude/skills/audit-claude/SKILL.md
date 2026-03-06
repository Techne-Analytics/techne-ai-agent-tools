---
name: audit-claude
description: Run a comprehensive CLAUDE.md quality audit, automation recommendations scan, and usage health analysis on any repository, then file a GitHub issue with the combined report. Use this skill when the user asks to audit their Claude Code setup, check CLAUDE.md health, review AI-first development readiness, analyze usage friction patterns, check for stale configuration, run a periodic codebase audit, or mentions "audit-claude". Also triggers on requests like "check my repo's Claude config", "how's my CLAUDE.md doing", "audit my automation setup", "what's causing friction in my Claude sessions", "check my usage patterns", or "run a maintenance scan". This skill is read-only and never modifies repository files.
---

# Audit Claude

A read-only codebase audit that checks CLAUDE.md quality and automation setup, compares against previous audits, and files a GitHub issue with findings.

**Important**: This skill does NOT modify any repository files. It produces a report only.

## Prerequisites

Before starting, verify that both required plugin skills are available:

1. `claude-md-management:claude-md-improver`
2. `claude-code-setup:claude-automation-recommender`

Check whether each skill appears in the available skills list for this session. If either is missing, stop and tell the user:

> To use audit-claude, you need these plugins installed:
> - **claude-md-management** (from claude-plugins-official)
> - **claude-code-setup** (from claude-plugins-official)
>
> Install missing plugins via `/install-plugin` or from the Claude Code plugin marketplace, then re-run this skill.

If both are present, proceed.

## Step 1: CLAUDE.md Quality Audit

Invoke the `claude-md-management:claude-md-improver` skill in **audit-only mode** -- that is, run the quality assessment but do NOT apply any changes. Capture the full quality report output including:

- Files scanned and their locations
- Quality scores or ratings
- Specific findings (missing sections, stale content, formatting issues)
- Recommended improvements

Store this output as `claude_md_report` for the combined report.

## Step 2: Automation Recommendations

Invoke the `claude-code-setup:claude-automation-recommender` skill. Capture the full recommendations report including:

- Hooks analysis (existing hooks, recommended new hooks)
- Subagent opportunities
- Skill gaps
- MCP server recommendations
- Plugin suggestions

Store this output as `automation_report` for the combined report.

## Step 3: AI-First Development Review

After the two sub-skill reports are complete, perform your own assessment of the repository's AI-first development readiness. Use the checklist in [references/ai-first-review-checklist.md](references/ai-first-review-checklist.md).

Evaluate these areas and assign a readiness rating (strong / adequate / needs-work / missing) to each:

- **CLAUDE.md coverage** -- Does CLAUDE.md exist at root and in key subdirectories? Is it substantive?
- **Hook configuration** -- Are pre/post hooks set up for common workflows (commit, test, lint)?
- **MCP server integration** -- Are relevant MCP servers configured for the project's domain?
- **Skill availability** -- Are useful skills installed for the project's tech stack?
- **Subagent setup** -- Are custom subagents defined where they'd help (review, test, deploy)?
- **Git workflow** -- Is the branching/PR model documented for AI agents?
- **Testing integration** -- Can Claude run tests and interpret results?
- **CI/CD awareness** -- Does CLAUDE.md reference CI pipelines and how to work with them?

Store this as `ai_first_review` for the combined report.

## Step 4: Usage Health Analysis

Analyze Claude Code session data to identify friction patterns, configuration gaps, and stale configuration. This step reads usage telemetry that Claude Code stores locally and cross-references it against the repository's existing setup. See [references/usage-health-analysis.md](references/usage-health-analysis.md) for the full methodology.

### 4a: Locate and Read Usage Data

Check whether usage data exists:

```bash
ls ~/.claude/usage-data/facets/ 2>/dev/null | head -5
ls ~/.claude/usage-data/session-meta/ 2>/dev/null | head -5
```

**If neither directory exists or both are empty**, store this as `usage_health_report`:

> **Usage Health: Skipped** -- No Claude Code usage data found at `~/.claude/usage-data/`.
> This is normal for CI environments, new installs, or when usage data collection is disabled.
> Re-run this audit after using Claude Code interactively in this project to get usage-based insights.

Then proceed to Step 5.

**If data exists**, continue with steps 4b-4g.

Also check whether a pre-computed insights report exists:

```bash
ls ~/.claude/usage-data/report.html 2>/dev/null
```

If `report.html` exists, read it as supplementary context for the analysis. It contains pre-computed project areas, friction categories, and suggestions from `/insights`. Use it to enrich your analysis but do not depend on it -- the raw data is the primary source.

### 4b: Filter Sessions for This Project

Read session metadata and filter to sessions matching the current project:

```bash
PROJECT_PATH=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
for f in ~/.claude/usage-data/session-meta/*.json; do
  if jq -e --arg p "$PROJECT_PATH" '.project_path == $p' "$f" > /dev/null 2>&1; then
    echo "$f"
  fi
done
```

If `jq` is not available, fall back to:
```bash
python3 -c "
import json, glob, os
project = '$(git rev-parse --show-toplevel 2>/dev/null || pwd)'
for f in sorted(glob.glob(os.path.expanduser('~/.claude/usage-data/session-meta/*.json')))[-50:]:
    try:
        with open(f) as fh:
            data = json.load(fh)
            if data.get('project_path') == project:
                print(f)
    except (json.JSONDecodeError, KeyError):
        pass  # skip malformed files
"
```

Collect the list of matching session IDs. Cap at the 50 most recent sessions. If no sessions match the current project, report:

> **Usage Health: No matching sessions** -- Usage data exists but contains no sessions for this project path.

Then proceed to Step 5.

### 4c: Aggregate Session Metrics

For each matching session, read both the session-meta and corresponding facets file (match on `session_id`). Compile:

1. **Session count** and **date range** (earliest to most recent)
2. **Total duration** (sum of `duration_minutes`)
3. **Outcome distribution** -- count of `achieved`, `mostly_achieved`, `partially_achieved`, `not_achieved`
4. **Satisfaction distribution** -- aggregate `user_satisfaction_counts`
5. **Helpfulness distribution** -- count of each `claude_helpfulness` value
6. **Tool usage summary** -- aggregate tool call counts by name, sorted by frequency, top 10
7. **Error summary** -- aggregate errors by type, sorted by frequency, top 5
8. **Token usage** -- total input/output tokens, average per session

### 4d: Friction Analysis

From the facets data, extract and analyze friction patterns:

1. Collect all `friction_counts` and `friction_detail` entries across sessions
2. Normalize similar descriptions into groups (e.g., "wrote to wrong directory" and "files saved to /tmp instead of repo" are the same pattern)
3. Rank by frequency
4. Assess severity by correlating with session outcomes:
   - Friction in sessions with outcome `not_achieved` = **high** severity
   - Friction in sessions with outcome `partially_achieved` or `mostly_achieved` = **medium** severity
   - Friction in sessions with outcome `achieved` = **low** severity

Present as a table:

```markdown
| Friction Pattern | Occurrences | Severity | Example |
|-----------------|-------------|----------|---------|
| Wrong file write target | 3 | high | Files written to /tmp instead of repo |
| Branch drift during PR | 2 | medium | Branch switched to main mid-PR |
| ... | ... | ... | ... |
```

### 4e: Gap Analysis

For each friction pattern, check whether existing configuration addresses it:

1. **Read CLAUDE.md** files (root and subdirectories) -- do they contain instructions that would prevent this friction?
2. **Read hooks** (`.claude/settings.local.json` and any files in `.claude/`) -- do existing hooks guard against this friction?
3. **Read installed skills** -- do skills cover the workflow where friction occurred?
4. **Read `.mcp.json`** -- are relevant MCP servers configured?

Classify each friction pattern:
- **Addressed** -- existing config should prevent this. Investigate why friction still occurs (stale instructions? too vague?).
- **Partially addressed** -- config exists but is incomplete or too general.
- **Unaddressed gap** -- no configuration targets this friction.

### 4f: Stale Configuration Detection

Cross-reference existing configuration against actual usage data. For each configured item (hook, skill, MCP server, CLAUDE.md instruction), determine:

1. **Is it a guardrail or a workflow tool?** Use the classification rules in [references/usage-health-analysis.md](references/usage-health-analysis.md).
2. **What does usage data show?** Check tool call counts, hook trigger patterns, and skill invocations in the session data.

**Critical rule: Never recommend removing a guardrail.** A guardrail that appears unused may be unused precisely because it is preventing the behavior it guards against. Permission deny rules, security hooks, and safety instructions in CLAUDE.md are guardrails. When in doubt, classify as guardrail and recommend keeping it.

For workflow tools only, and only with 50+ sessions of data, flag items with very low or zero usage for user review:

```markdown
| Item | Type | Classification | Usage (last N sessions) | Recommendation |
|------|------|---------------|------------------------|----------------|
| block force-push | deny rule | Guardrail | N/A | Keep (guardrail) |
| auto-lint hook | PostToolUse hook | Workflow tool | 0 triggers in 52 sessions | Review: may not be needed |
| context7 MCP | MCP server | Workflow tool | 34 calls | Active — keep |
| brainstorm skill | skill | Workflow tool | 1 use in 52 sessions | Low usage — verify still needed |
```

**Only flag workflow tools as "Review" -- never as "Remove".** The user decides whether to remove. Present the data and let them judge.

### 4g: Compile Usage Health Report

**Before assembling the report**, apply these redaction rules (the GitHub issue may be public):
- Strip absolute file paths outside the project directory
- Redact anything resembling credentials, tokens, or API keys
- Summarize friction details rather than quoting them verbatim if they contain sensitive context
- Never include raw session IDs in the report

Assemble `usage_health_report` with these sections:

```markdown
### Usage Health Summary

**Sessions analyzed**: {N} sessions from {date} to {date}
**Total interaction time**: {hours}h {minutes}m
**Overall satisfaction**: {pct}% positive
**Task success rate**: {pct}% ({n}/{total} sessions)

### Tool Usage Profile

{top 10 tools by usage}

### Friction Patterns

{friction table from 4d}

### Configuration Gaps

{unaddressed and partially-addressed friction patterns with frequency}

### Stale Configuration Review

{stale config table from 4f, or "Insufficient data (need 50+ sessions)" if < 50 sessions}

### Highest-Impact Suggestions

Based on friction patterns and gap analysis, ranked by frequency x severity:

1. {suggestion} -- addresses {pattern} ({N} occurrences, {severity})
2. {suggestion} -- addresses {pattern} ({N} occurrences, {severity})
...
```

Store this as `usage_health_report` for the combined report.

<!-- PHASE_B_MARKER: Friction-to-Fix Pipeline

When Phase B is activated, add step 4h here:

### 4h: Friction-to-Fix Pipeline

For each suggestion in the "Highest-Impact Suggestions" list, generate a concrete, ready-to-apply fix:

**For CLAUDE.md gaps**: Write the exact markdown to add, including the section header. Specify where it should be inserted (after which existing section).

**For hook gaps**: Write the exact JSON to add to `.claude/settings.local.json` or the hook file content. Include hook type, trigger, and action.

**For skill gaps**: Write a SKILL.md skeleton with name, description, trigger phrases, and key steps.

**For MCP server gaps**: Write the `.mcp.json` entry with server name, command, and configuration.

Present each fix as a fenced code block with:
- File path
- Action (add/modify)
- The exact content to insert
- Priority score (frequency x severity_weight: high=3, medium=2, low=1)

Rank all fixes by priority score. Store as `friction_fixes` for inclusion in the report.

Also add a "Ready-to-Apply Fixes" section to the issue body template after Usage Health Analysis.

END_PHASE_B_MARKER -->

## Step 5: Delta Summary

Search GitHub issue history for previous audit reports (including usage health findings from previous audits if present):

```bash
gh issue list --label "audit-report" --state all --limit 5 --json number,title,createdAt,body
```

If previous audit issues exist:

1. Read the most recent one
2. Compare its findings against the current audit
3. Categorize changes into three buckets:
   - **Fixed since last audit** -- issues that were present before but are now resolved
   - **New findings** -- issues appearing for the first time
   - **Regressions** -- issues that were previously fixed but have returned
   - **Unchanged** -- persistent issues that remain open

If no previous audit exists, note that this is the baseline audit and skip the delta comparison.

Store this as `delta_summary` for the combined report.

## Step 6: File or Update a GitHub Issue

First, check whether an open audit issue already exists:

```bash
gh issue list --label "audit-report" --state open --limit 1 --json number,title,createdAt
```

**If an open audit issue exists**: Do NOT create a new issue. Instead, add a comment to the existing issue with the new audit results. Use a comment header like:

```markdown
## Re-audit: YYYY-MM-DD

*Previous audit issue still open -- appending new findings instead of creating a duplicate.*
```

Then include the full report sections below, plus the delta summary comparing against the original issue body.

**If no open audit issue exists**: Create a new GitHub issue using `gh` with the following structure:

**Title**: `Periodic audit: CLAUDE.md + automation review (YYYY-MM-DD)` (use today's date)

**Label**: `audit-report` (create the label first if it doesn't exist)

**Body** -- use this template, filling in each section from the stored reports:

```markdown
# Periodic Audit: CLAUDE.md + Automation Review

**Date**: YYYY-MM-DD
**Repo**: owner/repo-name

---

## 1. CLAUDE.md Quality Report

{claude_md_report}

---

## 2. Automation Recommendations

{automation_report}

---

## 3. AI-First Development Readiness

{ai_first_review}

---

## 4. Usage Health Analysis

{usage_health_report}

<!-- PHASE_B_TEMPLATE_MARKER
---

## 4a. Ready-to-Apply Fixes

{friction_fixes}

END_PHASE_B_TEMPLATE_MARKER -->

---

## 5. Changes Since Last Audit

{delta_summary}

---

## 6. Recommended: Automate This Audit

This audit can run automatically on a schedule using GitHub Actions.
See the [GitHub Action setup guide](link-to-action-setup) or ask Claude:
`/audit-claude --setup-action`

---

*Generated by audit-claude skill*
```

After creating the issue:

1. Search for open issues that relate to the findings (e.g., issues about CLAUDE.md, CI/CD, testing setup)
2. If related issues exist, add a comment on the new audit issue referencing them:
   ```
   Related open issues: #12, #34, #56
   ```

Print the issue URL so the user can review it.

## Step 7: GitHub Action Recommendation

After filing the issue, recommend that the user set up automated auditing. Reference [references/github-action-setup.md](references/github-action-setup.md) for the full setup guide and sample workflow.

Summarize the recommendation:

> **Automate this audit**: You can run audit-claude on a weekly schedule using GitHub Actions.
> The action will invoke Claude Code headless, run this audit, and file a new issue with findings.
> See `references/github-action-setup.md` for a ready-to-use workflow, or I can set it up for you.

A sample workflow YAML is also available at [scripts/audit-claude-action.yml](scripts/audit-claude-action.yml).

## Output Contract

The final output shown to the user should include:
1. The full combined report (all sections above)
2. The GitHub issue URL
3. The usage health analysis (or note that no usage data was available)
4. The delta summary (or note that this is the first audit)
5. The GitHub Action recommendation

## What This Skill Does NOT Do

- It does not edit CLAUDE.md or any other file
- It does not install plugins or configure hooks
- It does not push code or create PRs
- It does not transmit usage data anywhere -- all analysis is local
- It does not modify usage data files
- It only reads, analyzes, and reports via a GitHub issue
