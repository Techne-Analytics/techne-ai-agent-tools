from __future__ import annotations

import json
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SETTINGS_PATH = REPO_ROOT / ".claude" / "settings.json"


class TestMarketplaceSettings:
    def test_claude_settings_exists(self) -> None:
        assert SETTINGS_PATH.exists(), ".claude/settings.json must exist"

    def test_claude_settings_valid_json(self) -> None:
        data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        assert isinstance(data, dict)

    def test_claude_settings_has_deny_rules(self) -> None:
        data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        deny = data.get("permissions", {}).get("deny", [])
        assert any("force" in rule for rule in deny), \
            "settings.json must deny force-push"
        assert any("-f" in rule for rule in deny), \
            "settings.json must deny short-flag force-push (-f)"
        assert any(".env" in rule for rule in deny), \
            "settings.json must deny writing .env files"
        assert any(".pem" in rule for rule in deny), \
            "settings.json must deny writing .pem files"
        assert any(".key" in rule for rule in deny), \
            "settings.json must deny writing .key files"


class TestPluginDiscovery:
    """Test that marketplace plugins are discoverable and structurally valid."""

    def test_all_marketplace_plugins_have_commands_or_skills(self) -> None:
        mp_path = REPO_ROOT / ".claude-plugin" / "marketplace.json"
        data = json.loads(mp_path.read_text(encoding="utf-8"))
        for plugin in data["plugins"]:
            source = pathlib.Path(plugin["source"])
            plugin_dir = REPO_ROOT / source
            commands = list((plugin_dir / "commands").glob("*.md")) if (plugin_dir / "commands").exists() else []
            skills = list((plugin_dir / "skills").glob("*/SKILL.md")) if (plugin_dir / "skills").exists() else []
            assert len(commands) + len(skills) >= 1, (
                f"Plugin '{plugin['name']}' must have at least one command or skill for discovery"
            )

    def test_all_marketplace_plugins_have_consistent_versions(self) -> None:
        mp_path = REPO_ROOT / ".claude-plugin" / "marketplace.json"
        data = json.loads(mp_path.read_text(encoding="utf-8"))
        for plugin in data["plugins"]:
            source = pathlib.Path(plugin["source"])
            pj_path = REPO_ROOT / source / ".claude-plugin" / "plugin.json"
            pj = json.loads(pj_path.read_text(encoding="utf-8"))
            assert pj["version"] == plugin["version"], (
                f"Plugin '{plugin['name']}' version mismatch: "
                f"marketplace={plugin['version']}, plugin.json={pj['version']}"
            )

    def test_marketplace_owner_matches_github_org(self) -> None:
        mp_path = REPO_ROOT / ".claude-plugin" / "marketplace.json"
        data = json.loads(mp_path.read_text(encoding="utf-8"))
        owner = data.get("owner", {})
        assert owner.get("name") == "Techne Analytics" or "techne" in str(owner).lower(), \
            "Marketplace owner should reference Techne Analytics"
