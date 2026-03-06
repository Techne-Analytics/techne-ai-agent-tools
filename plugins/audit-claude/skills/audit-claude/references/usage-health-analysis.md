# Usage Health Analysis Methodology

How audit-claude analyzes Claude Code usage data to identify friction patterns, configuration gaps, and stale configuration.

## Data Sources

Claude Code stores per-session telemetry in `~/.claude/usage-data/`:

### Facets (`facets/*.json`)

Per-session qualitative data:

| Field | Type | Description |
|-------|------|-------------|
| `underlying_goal` | string | What the user was trying to accomplish |
| `goal_categories` | object | Categorized goal types with counts |
| `outcome` | string | `achieved`, `mostly_achieved`, `partially_achieved`, `not_achieved` |
| `user_satisfaction_counts` | object | Satisfaction signals: `satisfied`, `likely_satisfied`, `dissatisfied`, `happy` |
| `claude_helpfulness` | string | `essential`, `very_helpful`, `somewhat_helpful`, `not_helpful` |
| `session_type` | string | `single_task`, `multi_task` |
| `friction_counts` | object | Friction event counts by type |
| `friction_detail` | string | Specific friction descriptions |
| `primary_success` | string | Whether the primary goal was achieved |
| `brief_summary` | string | Short description of what happened |
| `session_id` | string | Links to session-meta |

### Session Metadata (`session-meta/*.json`)

Per-session quantitative data:

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | string | Links to facets |
| `project_path` | string | Filesystem path of the project |
| `start_time` | string | ISO timestamp |
| `duration_minutes` | number | Session length |
| Message counts | numbers | User and assistant message counts |
| Tool usage | object | Tool call counts by name (e.g., `{"Bash": 15, "Read": 8}`) |
| `languages` | array | Programming languages detected |
| Git stats | object | Commits, files changed |
| Token counts | object | Input/output token totals |
| `errors` | array | Errors encountered |

### Insights Report (`report.html`)

If the user has previously run `/insights`, the synthesized report is available at `~/.claude/usage-data/report.html`. This contains pre-computed analysis (project areas, interaction style, friction categories, suggestions) that supplements the raw data. Use it as additional context if present, but do not depend on it.

## Analysis Pipeline

### 1. Session Filtering

Filter sessions by `project_path` matching `git rev-parse --show-toplevel`. Only sessions for the audited project are analyzed. Cap at 50 most recent sessions to stay within context limits.

### 2. Metric Aggregation

Aggregate across matching sessions:
- Totals: duration, tokens, messages, tool calls
- Distributions: outcome types, satisfaction levels, session types
- Rankings: most-used tools, most common errors, most common goals

### 3. Friction Pattern Extraction

1. Collect `friction_counts` and `friction_detail` across sessions
2. Normalize similar descriptions into groups
3. Rank by frequency
4. Assess severity by correlating with session outcomes:
   - Friction in `not_achieved` sessions = **high** severity
   - Friction in `partially_achieved` / `mostly_achieved` sessions = **medium** severity
   - Friction in `achieved` sessions = **low** severity

### 4. Gap Analysis

Cross-reference each friction pattern against four configuration layers:

| Layer | Files Checked | What Would Address Friction |
|-------|--------------|---------------------------|
| CLAUDE.md | Root and subdirectory CLAUDE.md files | Missing instructions, stale guidance |
| Hooks | `.claude/settings.local.json`, `.claude/hooks/` | Missing guardrails, missing auto-actions |
| Skills | Installed skills, plugin skills | Missing workflow automation |
| MCP Servers | `.mcp.json` | Missing external integrations |

Each friction pattern is classified:
- **Addressed** — relevant configuration exists that should prevent it
- **Partially addressed** — configuration exists but is incomplete
- **Unaddressed gap** — no configuration targets this friction

### 5. Stale Configuration Detection

Cross-reference existing configuration against actual usage to find items that may no longer be needed. This analysis must be conservative — see Classification Rules below.

#### Configuration Classification

Every configured item is classified into one of two roles:

**Guardrail** — exists to prevent bad outcomes. Examples:
- Permission deny rules (block force-push, block writing .env files)
- PreToolUse hooks that block destructive operations
- CLAUDE.md rules like "never commit to main directly" or "never deploy without asking"
- Security-related MCP server restrictions

**Workflow tool** — exists to make work easier or faster. Examples:
- Skills for PR creation, code review, brainstorming
- PostToolUse hooks that auto-lint or auto-format
- MCP servers for documentation lookup or issue tracking
- Custom subagents for exploration or testing

#### Staleness Rules

| Classification | Usage Signal | Recommendation | Confidence Required |
|---------------|-------------|----------------|-------------------|
| Guardrail | Never triggered | **Keep** — absence of triggers means it may be working as intended | N/A — never recommend removal |
| Guardrail | Triggered frequently | **Keep and investigate** — frequent triggers may indicate a training/docs gap | N/A |
| Workflow tool | Never used in 50+ sessions | **Review** — may not be needed, but verify with user first | High (must have 50+ sessions of data) |
| Workflow tool | Used < 3 times in 50+ sessions | **Low usage** — flag for user review, do not recommend removal | High |
| Workflow tool | Used regularly | **Active** — keep | N/A |
| Any | Cannot determine classification | **Keep** — when in doubt, do not recommend removal | N/A |

**Critical rule**: Never recommend removing a guardrail. A guardrail that appears unused may be unused precisely because it is preventing the behavior it guards against. The only valid action for a guardrail is to keep it or investigate why it triggers frequently.

#### How to Identify Guardrails

A configuration item is a guardrail if ANY of these are true:
- It is a permission deny rule in `.claude/settings.local.json`
- It is a PreToolUse hook that blocks or rejects operations
- It is a PostToolUse hook that validates, reverts, or rejects results
- It contains keywords: `block`, `deny`, `prevent`, `never`, `forbidden`, `restrict`, `security`, `force-push`, `credential`, `secret`, `.env`, `.pem`, `.key`, `require`, `must`, `mandatory`, `production`, `deploy`, `protected`, `allowlist`, `blocklist`
- It references safety, security, or compliance concerns
- It restricts what Claude can do (as opposed to helping Claude do things)

When in doubt, classify as guardrail.

### 6. Suggestion Ranking

Suggestions for new configuration (from gap analysis) are ranked by impact score:

`impact = frequency x severity_weight`

| Severity | Weight |
|----------|--------|
| High | 3 |
| Medium | 2 |
| Low | 1 |

### 7. Privacy and Redaction

Before including usage data in the GitHub issue:
- Strip absolute file paths outside the project directory
- Redact anything resembling credentials, tokens, or API keys
- Summarize rather than quote friction details that may contain sensitive context
- Never include raw session IDs in the report

## Graceful Degradation

| Condition | Behavior |
|-----------|----------|
| `~/.claude/usage-data/` does not exist | Skip step, note in report |
| Directory exists but is empty | Skip step, note in report |
| Data exists but no sessions match project | Report "no matching sessions" |
| Facets file missing for a session | Use session-meta only, note incomplete data |
| Session-meta missing for a session | Use facets only, note incomplete data |
| Fewer than 3 sessions | Analyze but caveat: "limited data — patterns may not be representative" |
| Fewer than 50 sessions for stale config analysis | Skip stale config recommendations, note insufficient data |
| Malformed JSON in a session file | Skip that session, note incomplete data |
| `jq` not available | Fall back to `python3 -c "import json; ..."` for JSON parsing |
