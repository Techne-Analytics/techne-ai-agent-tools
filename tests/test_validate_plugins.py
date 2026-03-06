from __future__ import annotations

import json
import pathlib
from unittest.mock import patch

import pytest

from scripts.validate_plugins import validate, main, MARKETPLACE_PATH, REPO_ROOT


def test_valid_marketplace_passes() -> None:
    """Real marketplace.json should pass validation."""
    errors = validate()
    assert errors == []


def test_main_returns_zero_on_success() -> None:
    assert main() == 0


def _write_marketplace(tmp_path: pathlib.Path, data: dict | str) -> pathlib.Path:
    """Helper to write a marketplace.json in a tmp directory."""
    plugin_dir = tmp_path / ".claude-plugin"
    plugin_dir.mkdir(parents=True, exist_ok=True)
    mp = plugin_dir / "marketplace.json"
    if isinstance(data, str):
        mp.write_text(data, encoding="utf-8")
    else:
        mp.write_text(json.dumps(data), encoding="utf-8")
    return mp


def test_missing_marketplace_file(tmp_path: pathlib.Path) -> None:
    fake_path = tmp_path / ".claude-plugin" / "marketplace.json"
    with patch("scripts.validate_plugins.MARKETPLACE_PATH", fake_path):
        errors = validate()
    assert len(errors) == 1
    assert "not found" in errors[0]


def test_invalid_json(tmp_path: pathlib.Path) -> None:
    mp = _write_marketplace(tmp_path, "not valid json {{{")
    with patch("scripts.validate_plugins.MARKETPLACE_PATH", mp):
        errors = validate()
    assert len(errors) == 1
    assert "invalid JSON" in errors[0]


def test_missing_required_top_level_fields(tmp_path: pathlib.Path) -> None:
    mp = _write_marketplace(tmp_path, {"foo": "bar"})
    with patch("scripts.validate_plugins.MARKETPLACE_PATH", mp):
        errors = validate()
    assert any("'name'" in e for e in errors)
    assert any("'owner'" in e for e in errors)
    assert any("'plugins'" in e for e in errors)


def test_plugins_wrong_type(tmp_path: pathlib.Path) -> None:
    mp = _write_marketplace(tmp_path, {"name": "x", "owner": {}, "plugins": "not-a-list"})
    with patch("scripts.validate_plugins.MARKETPLACE_PATH", mp):
        errors = validate()
    assert any("must be an array" in e for e in errors)


def test_plugins_empty_array(tmp_path: pathlib.Path) -> None:
    mp = _write_marketplace(tmp_path, {"name": "x", "owner": {}, "plugins": []})
    with patch("scripts.validate_plugins.MARKETPLACE_PATH", mp):
        errors = validate()
    assert any("at least one plugin" in e for e in errors)


def test_non_dict_plugin_entry(tmp_path: pathlib.Path) -> None:
    mp = _write_marketplace(tmp_path, {"name": "x", "owner": {}, "plugins": ["a-string"]})
    with patch("scripts.validate_plugins.MARKETPLACE_PATH", mp):
        errors = validate()
    assert any("must be an object" in e for e in errors)


def test_missing_plugin_fields(tmp_path: pathlib.Path) -> None:
    mp = _write_marketplace(tmp_path, {
        "name": "x", "owner": {}, "plugins": [{"name": "p"}]
    })
    with patch("scripts.validate_plugins.MARKETPLACE_PATH", mp):
        errors = validate()
    assert any("'source'" in e for e in errors)
    assert any("'description'" in e for e in errors)
    assert any("'version'" in e for e in errors)


def test_empty_source_field(tmp_path: pathlib.Path) -> None:
    mp = _write_marketplace(tmp_path, {
        "name": "x", "owner": {}, "plugins": [
            {"name": "p", "source": "", "description": "d", "version": "1.0.0"}
        ]
    })
    with patch("scripts.validate_plugins.MARKETPLACE_PATH", mp):
        errors = validate()
    assert any("empty" in e for e in errors)


def test_plugin_source_not_found(tmp_path: pathlib.Path) -> None:
    mp = _write_marketplace(tmp_path, {
        "name": "x", "owner": {}, "plugins": [
            {"name": "p", "source": "./nonexistent", "description": "d", "version": "1.0.0"}
        ]
    })
    with patch("scripts.validate_plugins.MARKETPLACE_PATH", mp), \
         patch("scripts.validate_plugins.REPO_ROOT", tmp_path):
        errors = validate()
    assert any("not found" in e for e in errors)


def test_version_mismatch(tmp_path: pathlib.Path) -> None:
    # Create a plugin directory with mismatched version
    plugin_dir = tmp_path / "plugins" / "myplugin"
    (plugin_dir / ".claude-plugin").mkdir(parents=True)
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"name": "myplugin", "version": "2.0.0", "description": "d"}),
        encoding="utf-8",
    )
    # Need at least one command or skill to avoid that error too
    (plugin_dir / "commands").mkdir()
    (plugin_dir / "commands" / "cmd.md").write_text("---\nname: cmd\ndescription: d\n---\n")

    mp = _write_marketplace(tmp_path, {
        "name": "x", "owner": {}, "plugins": [
            {"name": "myplugin", "source": "./plugins/myplugin", "description": "d", "version": "1.0.0"}
        ]
    })
    with patch("scripts.validate_plugins.MARKETPLACE_PATH", mp), \
         patch("scripts.validate_plugins.REPO_ROOT", tmp_path):
        errors = validate()
    assert any("version mismatch" in e for e in errors)


def test_missing_commands_and_skills(tmp_path: pathlib.Path) -> None:
    # Create a plugin directory with plugin.json but no commands or skills
    plugin_dir = tmp_path / "plugins" / "empty"
    (plugin_dir / ".claude-plugin").mkdir(parents=True)
    (plugin_dir / ".claude-plugin" / "plugin.json").write_text(
        json.dumps({"name": "empty", "version": "1.0.0", "description": "d"}),
        encoding="utf-8",
    )

    mp = _write_marketplace(tmp_path, {
        "name": "x", "owner": {}, "plugins": [
            {"name": "empty", "source": "./plugins/empty", "description": "d", "version": "1.0.0"}
        ]
    })
    with patch("scripts.validate_plugins.MARKETPLACE_PATH", mp), \
         patch("scripts.validate_plugins.REPO_ROOT", tmp_path):
        errors = validate()
    assert any("no commands or skills" in e for e in errors)


def test_main_returns_one_on_errors(tmp_path: pathlib.Path) -> None:
    fake_path = tmp_path / ".claude-plugin" / "marketplace.json"
    with patch("scripts.validate_plugins.MARKETPLACE_PATH", fake_path):
        result = main()
    assert result == 1
