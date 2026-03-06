from __future__ import annotations

import json
import pathlib

import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
MARKETPLACE_PATH = REPO_ROOT / ".claude-plugin" / "marketplace.json"


def _load_marketplace() -> dict:
    return json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))


def _frontmatter(text: str) -> dict:
    parts = text.split("---")
    assert len(parts) >= 3, "file must contain YAML frontmatter"
    return yaml.safe_load(parts[1])


class TestMarketplaceJson:
    def test_marketplace_exists(self) -> None:
        assert MARKETPLACE_PATH.exists(), ".claude-plugin/marketplace.json must exist"

    def test_marketplace_has_required_fields(self) -> None:
        data = _load_marketplace()
        assert "name" in data
        assert "owner" in data
        assert "plugins" in data
        assert isinstance(data["plugins"], list)
        assert len(data["plugins"]) >= 1

    def test_marketplace_plugins_have_required_fields(self) -> None:
        data = _load_marketplace()
        for plugin in data["plugins"]:
            assert "name" in plugin, f"plugin missing 'name': {plugin}"
            assert "source" in plugin, f"plugin missing 'source': {plugin}"
            assert "description" in plugin, f"plugin missing 'description': {plugin}"
            assert "version" in plugin, f"plugin missing 'version': {plugin}"


class TestPluginDirectories:
    def test_each_listed_plugin_exists(self) -> None:
        data = _load_marketplace()
        for plugin in data["plugins"]:
            source = pathlib.Path(plugin["source"])
            plugin_dir = REPO_ROOT / source
            assert plugin_dir.exists(), f"plugin directory not found: {plugin_dir}"

    def test_each_plugin_has_plugin_json(self) -> None:
        data = _load_marketplace()
        for plugin in data["plugins"]:
            source = pathlib.Path(plugin["source"])
            pj = REPO_ROOT / source / ".claude-plugin" / "plugin.json"
            assert pj.exists(), f"plugin.json not found: {pj}"

    def test_each_plugin_has_command_or_skill(self) -> None:
        data = _load_marketplace()
        for plugin in data["plugins"]:
            source = pathlib.Path(plugin["source"])
            plugin_dir = REPO_ROOT / source
            commands = list((plugin_dir / "commands").glob("*.md")) if (plugin_dir / "commands").exists() else []
            skills = list((plugin_dir / "skills").glob("*/SKILL.md")) if (plugin_dir / "skills").exists() else []
            assert len(commands) + len(skills) >= 1, (
                f"plugin '{plugin['name']}' must have at least one command or skill"
            )


class TestPluginJsonContents:
    def test_plugin_json_has_required_fields(self) -> None:
        data = _load_marketplace()
        required = {"name", "version", "description"}
        for plugin in data["plugins"]:
            source = pathlib.Path(plugin["source"])
            pj_path = REPO_ROOT / source / ".claude-plugin" / "plugin.json"
            pj = json.loads(pj_path.read_text(encoding="utf-8"))
            missing = required - set(pj.keys())
            assert not missing, f"plugin.json for '{plugin['name']}' missing fields: {missing}"

    def test_plugin_json_version_matches_marketplace(self) -> None:
        data = _load_marketplace()
        for plugin in data["plugins"]:
            source = pathlib.Path(plugin["source"])
            pj_path = REPO_ROOT / source / ".claude-plugin" / "plugin.json"
            pj = json.loads(pj_path.read_text(encoding="utf-8"))
            assert pj["version"] == plugin["version"], (
                f"version mismatch for '{plugin['name']}': "
                f"marketplace says {plugin['version']}, plugin.json says {pj['version']}"
            )


class TestPluginJsonReferences:
    def test_plugin_json_does_not_use_bare_name_arrays(self) -> None:
        """Plugin.json skills/commands must be paths (./...) not bare names."""
        data = _load_marketplace()
        for plugin in data["plugins"]:
            source = pathlib.Path(plugin["source"])
            pj_path = REPO_ROOT / source / ".claude-plugin" / "plugin.json"
            pj = json.loads(pj_path.read_text(encoding="utf-8"))
            for field in ("skills", "commands"):
                values = pj.get(field, [])
                if isinstance(values, str):
                    values = [values]
                for val in values:
                    assert val.startswith("./"), (
                        f"plugin '{plugin['name']}' {field} entry '{val}' must be a path starting with './' "
                        f"(bare names cause validation errors)"
                    )


class TestCommandFrontmatter:
    def test_commands_have_name_and_description(self) -> None:
        data = _load_marketplace()
        for plugin in data["plugins"]:
            source = pathlib.Path(plugin["source"])
            cmd_dir = REPO_ROOT / source / "commands"
            if not cmd_dir.exists():
                continue
            for cmd_file in cmd_dir.glob("*.md"):
                text = cmd_file.read_text(encoding="utf-8")
                fm = _frontmatter(text)
                assert "name" in fm, f"{cmd_file} missing 'name' in frontmatter"
                assert "description" in fm, f"{cmd_file} missing 'description' in frontmatter"


class TestSkillStructure:
    def test_skills_have_valid_frontmatter(self) -> None:
        data = _load_marketplace()
        for plugin in data["plugins"]:
            source = pathlib.Path(plugin["source"])
            skills_dir = REPO_ROOT / source / "skills"
            if not skills_dir.exists():
                continue
            for skill_md in skills_dir.glob("*/SKILL.md"):
                text = skill_md.read_text(encoding="utf-8")
                fm = _frontmatter(text)
                assert "name" in fm, f"{skill_md} missing 'name' in frontmatter"
                assert "description" in fm, f"{skill_md} missing 'description' in frontmatter"

    def test_skills_have_output_contract(self) -> None:
        data = _load_marketplace()
        for plugin in data["plugins"]:
            source = pathlib.Path(plugin["source"])
            skills_dir = REPO_ROOT / source / "skills"
            if not skills_dir.exists():
                continue
            for skill_md in skills_dir.glob("*/SKILL.md"):
                text = skill_md.read_text(encoding="utf-8")
                assert "## Output Contract" in text or "## Output" in text, (
                    f"{skill_md} missing Output Contract section"
                )
