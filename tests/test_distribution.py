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
