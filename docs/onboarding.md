# Adding Techne Plugins to Your Project

## Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed
- A project with a git repository

## Install Plugins

Add the Techne marketplace and install any plugins you need:

```bash
claude plugins marketplace add Techne-Analytics/techne-ai-agent-tools
claude plugins install project-bootstrap@techne-ai-agent-tools
claude plugins install audit-claude@techne-ai-agent-tools
```

## Recommended First Steps

1. **Run project-bootstrap** to set up Claude Code for your project:
   ```
   /project-bootstrap
   ```
   This analyzes your project and generates a CLAUDE.md, safety hooks, and MCP server recommendations.

2. **Run audit-claude** to check your setup:
   ```
   /audit-claude
   ```
   This produces a quality report and files a GitHub issue with findings.

## Available Plugins

| Plugin | Description | Command |
|--------|-------------|---------|
| project-bootstrap | Set up Claude Code config for a new project | `/project-bootstrap` |
| audit-claude | Read-only audit of CLAUDE.md quality and automation setup | `/audit-claude` |

## Updating Plugins

To get the latest versions:

```bash
claude plugins update
```

## Troubleshooting

**Plugin not found after marketplace add:**
- Verify the marketplace was added: `claude plugins marketplace list`
- Check that the plugin name matches exactly (case-sensitive)

**Permission errors during plugin commands:**
- `project-bootstrap` needs write access (creates files). Approve tool permissions when prompted.
- `audit-claude` is read-only. It only needs `Read`, `Bash`, `Grep`, `Glob` permissions.
