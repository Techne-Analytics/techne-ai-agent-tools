# Techne AI Agent Tools

Open-source Claude Code plugins for AI-agent-assisted development.

[![CI](https://github.com/Techne-Analytics/techne-ai-agent-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/Techne-Analytics/techne-ai-agent-tools/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Quick Start

Add this marketplace to your Claude Code setup:

```bash
claude plugins marketplace add Techne-Analytics/techne-ai-agent-tools
claude plugins install project-bootstrap@techne-ai-agent-tools
claude plugins install audit-claude@techne-ai-agent-tools
```

## Available Plugins

### project-bootstrap

Set up Claude Code configuration for any project in minutes.

```
/project-bootstrap
```

Analyzes your project's tech stack, structure, and conventions, then configures:
- **CLAUDE.md** tailored to your project (build commands, architecture, code style)
- **Safety hooks** (block force-push, block secret commits)
- **MCP servers** based on your stack (Context7, database, GitHub)
- **Settings** with recommended marketplace connections

### audit-claude

Periodic health check for your Claude Code setup.

```
/audit-claude
```

Runs a read-only audit that checks:
- **CLAUDE.md quality** and completeness
- **Automation gaps** (missing hooks, skills, MCP servers)
- **AI-first development readiness** across 8 dimensions
- **Usage friction patterns** from session data
- **Delta tracking** against previous audits

Files a GitHub issue with the full report. Can be automated via GitHub Actions on a weekly schedule.

## Why These Tools?

AI-agent-assisted development works best when the agent has good context. Most teams skip the setup -- no CLAUDE.md, no hooks, no safety guardrails -- and wonder why Claude makes mistakes.

These plugins encode the patterns we've refined across dozens of client engagements at [Techne Analytics](https://techneanalytics.com). They're opinionated, practical, and free.

## Contributing

We welcome contributions. Please:

1. Fork the repo
2. Create a feature branch (`feat/your-feature`)
3. Follow [conventional commits](https://www.conventionalcommits.org/)
4. Include tests for new plugins
5. Open a PR with a testing plan

See `CLAUDE.md` for development setup and guidelines.

## Compliance

This repository follows SOC 2-ready development practices: branch protection, required reviews, CI validation, no secrets in code. It was configured using our own compliance toolkit -- run our [compliance auditor](https://github.com/Techne-Analytics/agentic-ai-tooling) against it to see the results.

## Built by Techne Analytics

[Techne Analytics](https://techneanalytics.com) helps teams build reliable AI agents. We offer:

- **AI agent development** -- custom agents for your workflows
- **Compliance auditing** -- SOC 2, ISO 27001, HIPAA readiness for AI systems
- **Claude Code optimization** -- get more out of AI-assisted development

[Get in touch](https://techneanalytics.com/contact) to learn more.

---

MIT License. See [LICENSE](LICENSE) for details.
