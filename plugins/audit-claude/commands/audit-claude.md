---
name: audit-claude
description: Run a read-only CLAUDE.md quality audit, automation recommendations scan, and usage health analysis, then file a GitHub issue with the combined report.
allowed-tools: ["Read", "Bash", "Grep", "Glob", "Skill", "Agent", "WebFetch"]
---

Run the `audit-claude` skill on this repository. Follow the skill instructions exactly:

1. Run CLAUDE.md quality audit (audit-only, no changes) [SKILL.md Step 1]
2. Run automation recommendations scan [Step 2]
3. Perform AI-first development readiness review [Step 3]
4. Analyze Claude Code usage data for friction patterns, configuration gaps, and stale configuration (skip gracefully if no usage data exists) [Step 4]
5. Compare against previous audits (search for audit-report label) [Step 5]
6. File or update a GitHub issue with the combined report [Step 6]
7. Recommend GitHub Action setup for automated auditing [Step 7]

Prerequisites: claude-md-management:claude-md-improver and claude-code-setup:claude-automation-recommender must be available. See SKILL.md Prerequisites section.

Do NOT modify any repository files or usage data. Report only.
