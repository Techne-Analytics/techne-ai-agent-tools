from __future__ import annotations

import json
import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


class TestMarketplaceSettings:
    def test_claude_settings_exists(self) -> None:
        settings_path = REPO_ROOT / ".claude" / "settings.json"
        assert settings_path.exists(), ".claude/settings.json must exist"

    def test_claude_settings_valid_json(self) -> None:
        settings_path = REPO_ROOT / ".claude" / "settings.json"
        data = json.loads(settings_path.read_text(encoding="utf-8"))
        assert isinstance(data, dict)

    def test_claude_settings_has_deny_rules(self) -> None:
        settings_path = REPO_ROOT / ".claude" / "settings.json"
        data = json.loads(settings_path.read_text(encoding="utf-8"))
        deny = data.get("permissions", {}).get("deny", [])
        assert any("force" in rule for rule in deny), \
            "settings.json must deny force-push"
