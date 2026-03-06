#!/usr/bin/env python3
"""Validate plugin marketplace structure.

Validates core plugin marketplace structure for CI. See tests/test_plugin_structure.py
for full structural tests.
"""
from __future__ import annotations

import json
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
MARKETPLACE_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"


def validate() -> list[str]:
    errors: list[str] = []

    if not MARKETPLACE_PATH.exists():
        return [".claude-plugin/marketplace.json not found"]

    try:
        raw = MARKETPLACE_PATH.read_text(encoding="utf-8")
    except OSError as e:
        return [f"marketplace.json could not be read: {e}"]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return [f"marketplace.json is invalid JSON: {e}"]

    for field in ("name", "owner", "plugins"):
        if field not in data:
            errors.append(f"marketplace.json missing required field '{field}'")
    if errors:
        return errors

    plugins = data.get("plugins", [])
    if not isinstance(plugins, list):
        return [f"marketplace.json 'plugins' must be an array, got {type(plugins).__name__}"]
    if len(plugins) == 0:
        return ["marketplace.json 'plugins' array must contain at least one plugin"]

    for i, plugin in enumerate(plugins):
        if not isinstance(plugin, dict):
            errors.append(f"plugins[{i}] must be an object, got {type(plugin).__name__}")
            continue
        name = plugin.get("name", "<unnamed>")
        for field in ("name", "source", "description", "version"):
            if field not in plugin:
                errors.append(f"plugin '{name}' missing field '{field}'")

        source = plugin.get("source")
        if not source or not isinstance(source, str):
            if "source" in plugin:
                errors.append(f"plugin '{name}' has empty or non-string 'source' field")
            continue
        plugin_dir = (REPO_ROOT / pathlib.Path(source)).resolve()
        if not str(plugin_dir).startswith(str(REPO_ROOT.resolve())):
            errors.append(f"plugin '{name}' source path escapes repository root: {source}")
            continue
        if not plugin_dir.exists():
            errors.append(f"plugin '{name}' source directory not found: {source}")
            continue

        pj_path = plugin_dir / ".claude-plugin" / "plugin.json"
        if not pj_path.exists():
            errors.append(f"plugin '{name}' missing .claude-plugin/plugin.json")
        else:
            try:
                pj = json.loads(pj_path.read_text(encoding="utf-8"))
                if pj.get("version") != plugin.get("version"):
                    errors.append(
                        f"plugin '{name}' version mismatch: "
                        f"marketplace={plugin.get('version')}, plugin.json={pj.get('version')}"
                    )
            except (json.JSONDecodeError, OSError) as e:
                errors.append(f"plugin '{name}' plugin.json could not be read or parsed: {e}")

        commands = list((plugin_dir / "commands").glob("*.md")) if (plugin_dir / "commands").exists() else []
        skills = list((plugin_dir / "skills").glob("*/SKILL.md")) if (plugin_dir / "skills").exists() else []
        if not commands and not skills:
            errors.append(f"plugin '{name}' has no commands or skills")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1
    print("Plugin marketplace validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
