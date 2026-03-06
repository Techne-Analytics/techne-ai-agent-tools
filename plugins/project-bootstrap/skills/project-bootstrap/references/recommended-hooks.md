# Recommended Hooks

## Always Configure (Deny Rules)

These should be in every project's `.claude/settings.json`:

```json
{
  "permissions": {
    "deny": [
      "Bash(git push --force*)",
      "Bash(git push -f*)",
      "Write(*.env)",
      "Write(*.pem)",
      "Write(*.key)"
    ]
  }
}
```

## Stack-Specific Recommendations

### Python Projects
- **PostToolUse (Edit/Write)**: Run `ruff check --fix` after file edits if ruff is configured
- **PostToolUse (Edit/Write)**: Run `black` or `ruff format` if configured

### Node/TypeScript Projects
- **PostToolUse (Edit/Write)**: Run `eslint --fix` if eslint is configured
- **PostToolUse (Edit/Write)**: Run `prettier --write` if prettier is configured

### Rust Projects
- **PostToolUse (Edit/Write)**: Run `cargo fmt` after edits
- **PostToolUse (Edit/Write)**: Run `cargo clippy` for lint warnings

### Go Projects
- **PostToolUse (Edit/Write)**: Run `gofmt` after edits
- **PostToolUse (Edit/Write)**: Run `go vet` for static analysis

## General Recommendations

- **UserPromptSubmit**: Inject project context or remind about conventions
- **Stop**: Auto-review or summary generation after task completion
- **SessionStart**: Display project status or recent changes
