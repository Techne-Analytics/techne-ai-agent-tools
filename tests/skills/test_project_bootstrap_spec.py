from __future__ import annotations

import pathlib

import yaml


SKILL_PATH = pathlib.Path("plugins/project-bootstrap/skills/project-bootstrap/SKILL.md")
REF_DIR = pathlib.Path("plugins/project-bootstrap/skills/project-bootstrap/references")
CMD_PATH = pathlib.Path("plugins/project-bootstrap/commands/project-bootstrap.md")


def _frontmatter(text: str) -> dict:
    parts = text.split("---")
    assert len(parts) >= 3, "file must contain YAML frontmatter"
    return yaml.safe_load(parts[1])


def test_skill_frontmatter() -> None:
    text = SKILL_PATH.read_text(encoding="utf-8")
    fm = _frontmatter(text)
    assert fm["name"] == "project-bootstrap"
    assert "description" in fm and fm["description"]


def test_skill_core_sections() -> None:
    text = SKILL_PATH.read_text(encoding="utf-8")
    required = [
        "## Prerequisites",
        "## Step 1:",
        "## Step 2:",
        "## Step 3:",
        "## Step 4:",
        "## Step 5:",
        "## Step 6:",
        "## Output Contract",
        "## What This Skill Does NOT Do",
    ]
    for section in required:
        assert section in text, f"SKILL.md missing required section: {section}"


def test_skill_has_required_references() -> None:
    expected = {
        "claude-md-template.md",
        "recommended-hooks.md",
        "recommended-mcp.md",
    }
    existing = {p.name for p in REF_DIR.glob("*.md")}
    assert expected.issubset(existing), f"missing references: {expected - existing}"


def test_command_frontmatter() -> None:
    text = CMD_PATH.read_text(encoding="utf-8")
    fm = _frontmatter(text)
    assert fm["name"] == "project-bootstrap"
    assert "description" in fm
    assert "allowed-tools" in fm
    tools = fm["allowed-tools"]
    # project-bootstrap DOES write files, so Write and Edit should be present
    assert "Write" in tools
    assert "Edit" in tools
    assert "Read" in tools
