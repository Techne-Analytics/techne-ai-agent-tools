---
name: project-bootstrap
description: Analyze a project and set up Claude Code configuration (CLAUDE.md, hooks, MCP servers, settings) following Techne best practices.
allowed-tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob", "Agent", "WebFetch"]
---

Run the `project-bootstrap` skill on this repository. Follow the skill instructions exactly:

1. Analyze the project (tech stack, structure, conventions) [Step 1]
2. Generate a CLAUDE.md tailored to the project [Step 2]
3. Configure recommended hooks and deny rules [Step 3]
4. Suggest and configure MCP servers [Step 4]
5. Set up .claude/settings.json with Techne marketplace [Step 5]
6. Output a summary checklist of what was configured [Step 6]

This skill CREATES and MODIFIES files. Review all changes before committing.
