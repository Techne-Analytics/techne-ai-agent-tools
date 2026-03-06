from __future__ import annotations

import pathlib

import yaml


SKILL_PATH = pathlib.Path("plugins/audit-claude/skills/audit-claude/SKILL.md")
REF_DIR = pathlib.Path("plugins/audit-claude/skills/audit-claude/references")
CMD_PATH = pathlib.Path("plugins/audit-claude/commands/audit-claude.md")


def _frontmatter(text: str) -> dict:
    parts = text.split("---")
    assert len(parts) >= 3, "file must contain YAML frontmatter"
    return yaml.safe_load(parts[1])


def test_skill_frontmatter() -> None:
    text = SKILL_PATH.read_text(encoding="utf-8")
    fm = _frontmatter(text)
    assert fm["name"] == "audit-claude"
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
        "## Step 7:",
        "## Output Contract",
        "## What This Skill Does NOT Do",
    ]
    for section in required:
        assert section in text, f"SKILL.md missing required section: {section}"


def test_skill_has_required_references() -> None:
    expected = {
        "ai-first-review-checklist.md",
        "github-action-setup.md",
        "usage-health-analysis.md",
    }
    existing = {p.name for p in REF_DIR.glob("*.md")}
    assert expected.issubset(existing), f"missing references: {expected - existing}"


def test_command_frontmatter() -> None:
    text = CMD_PATH.read_text(encoding="utf-8")
    fm = _frontmatter(text)
    assert fm["name"] == "audit-claude"
    assert "description" in fm
    assert "allowed-tools" in fm
    # Verify read-only: no write tools
    tools = fm["allowed-tools"]
    for forbidden in ["Write", "Edit", "NotebookEdit"]:
        assert forbidden not in tools, f"read-only command must not allow {forbidden}"


def test_skill_references_read_only_contract() -> None:
    text = SKILL_PATH.read_text(encoding="utf-8")
    assert "## What This Skill Does NOT Do" in text
    not_do_section = text.split("## What This Skill Does NOT Do")[1]
    assert "not edit" in not_do_section.lower() or "not modify" in not_do_section.lower()
