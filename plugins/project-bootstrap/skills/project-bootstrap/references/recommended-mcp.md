# Recommended MCP Servers

## Universal (Any Project)

### Context7
Documentation retrieval for libraries and APIs. Useful for any project.
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/context7-mcp"]
    }
  }
}
```

## Stack-Specific

### Database Projects (PostgreSQL, MySQL, SQLite)
If the project connects to a database (detected via ORM configs, connection strings, or database drivers in dependencies).

### GitHub Integration
If the project has `.github/` directory or uses GitHub for issue tracking.

### Slack Integration
If the project has Slack webhook URLs or bot tokens in config.

## Selection Criteria

Recommend an MCP server when:
1. The project's tech stack clearly benefits from it
2. The server is maintained and well-documented
3. The user has the necessary credentials/access

Do NOT recommend:
- Servers for technologies not used in the project
- Experimental or unmaintained servers
- Servers requiring complex setup without clear benefit
