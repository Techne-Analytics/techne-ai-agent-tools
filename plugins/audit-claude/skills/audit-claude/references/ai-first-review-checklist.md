# AI-First Development Readiness Checklist

Use this checklist to assess how well a repository is set up for productive AI-agent-assisted development. Rate each area as: **strong**, **adequate**, **needs-work**, or **missing**.

## 1. CLAUDE.md Coverage

| Check | What to look for |
|-------|-----------------|
| Root CLAUDE.md exists | A CLAUDE.md at the repo root with project-level context |
| Substantive content | Not just a placeholder -- includes build commands, architecture, conventions |
| Subdirectory CLAUDE.md files | Key directories (src, tests, docs, infra) have their own CLAUDE.md where useful |
| Kept current | Content reflects the actual state of the codebase (not stale references) |
| Coding conventions documented | Style, naming, patterns, and anti-patterns the agent should follow |
| Build/test commands | Clear instructions for how to build, test, and lint |

## 2. Hook Configuration & Safety

| Check | What to look for |
|-------|-----------------|
| PreToolUse hooks | Guardrails before destructive operations (e.g., block force-push, prevent secret commits) |
| PostToolUse hooks | Automated follow-up actions (e.g., lint after edit, test after write) |
| UserPromptSubmit hooks | Input validation or context injection |
| Stop hooks | Post-completion actions (e.g., auto-review, summary generation) |
| Hooks are documented | CLAUDE.md or a hooks config file explains what hooks are active and why |
| Permission deny rules | Deny rules block force-push, writing sensitive files (.env, .pem, .key, credentials) |
| Agent safety rules documented | CLAUDE.md or AGENTS.md explicitly states: no merge without user ask, no deploy without user ask, no force-push to main |

## 3. MCP Server Integration

| Check | What to look for |
|-------|-----------------|
| Relevant MCP servers configured | Servers matching the project's domain (e.g., database, API docs, Slack) |
| .mcp.json present | Project-level MCP configuration exists |
| Servers accessible | Configured servers are reachable and authenticated |
| Usage documented | CLAUDE.md mentions which MCP servers are available and when to use them |

## 4. Skill Availability

| Check | What to look for |
|-------|-----------------|
| Tech-stack skills installed | Skills matching the project's languages/frameworks |
| Workflow skills present | Skills for common workflows (commit, PR, review, deploy) |
| Custom skills for project patterns | Project-specific skills for repeated complex tasks |
| Skills documented in CLAUDE.md | Available skills are listed so the agent knows what's available |
| Skills-driven dev lifecycle | A documented workflow using skills end-to-end (e.g., brainstorming → plan → code → PR → review → merge) |

## 5. Subagent Setup

| Check | What to look for |
|-------|-----------------|
| Review agents configured | Code review, PR review, or similar quality-check agents |
| Specialized agents for domains | Agents for areas like security, testing, documentation |
| Agent descriptions are clear | "When to use" descriptions are specific enough for reliable triggering |
| Agent tools are scoped | Each agent has only the tools it needs, not blanket access |

## 6. Git Workflow

| Check | What to look for |
|-------|-----------------|
| Branching model documented | CLAUDE.md describes the branch naming and merge strategy |
| No direct commits to main | Explicitly documented that all changes require a feature branch and PR |
| PR conventions specified | Template, review requirements, label conventions |
| PR testing plan required | Every PR body must include a manual testing plan with exact verification steps |
| Commit message format | Conventional commits or similar standard is documented |
| Protected branches noted | Agent knows which branches require PRs vs. direct push |
| Pre-commit checklist documented | Exact lint/test/validation commands to run before every commit are listed |

## 7. Testing Integration

| Check | What to look for |
|-------|-----------------|
| Test commands documented | CLAUDE.md has the exact commands to run tests |
| Test output is parseable | Agent can run tests and determine pass/fail from output |
| Test patterns documented | Where to put new tests, naming conventions, fixtures |
| Coverage expectations noted | Minimum coverage thresholds or expectations |

## 8. CI/CD Awareness

| Check | What to look for |
|-------|-----------------|
| CI pipeline documented | CLAUDE.md references CI system and key workflows |
| How to check CI status | Agent knows how to verify if CI passes (e.g., `gh run list`) |
| Deploy process documented | How deploys work, who/what can trigger them |
| Environment awareness | Staging, production, and other environments are described |

## Scoring Guide

- **Strong** (3): Fully configured, documented, and actively maintained
- **Adequate** (2): Present and functional but could be more thorough
- **Needs work** (1): Partially set up or significantly outdated
- **Missing** (0): Not present at all

**Total possible**: 24 points (8 areas x 3 max)

| Score Range | Overall Rating |
|-------------|---------------|
| 20-24 | Excellent -- repo is well-optimized for AI-first development |
| 14-19 | Good -- solid foundation with room for improvement |
| 8-13 | Fair -- basic setup exists but significant gaps remain |
| 0-7 | Early stage -- major setup work needed |
