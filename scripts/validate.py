#!/usr/bin/env python3
"""Validate the published dont-stop skill without third-party dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skill_path = root / "SKILL.md"
    agent_path = root / "agents" / "openai.yaml"
    readme_path = root / "README.md"
    readme_zh_path = root / "README.zh-CN.md"

    for path in (skill_path, agent_path, readme_path, readme_zh_path):
        require(path.is_file(), f"missing required file: {path.relative_to(root)}", errors)

    if not skill_path.is_file():
        return errors

    skill_text = skill_path.read_text(encoding="utf-8")
    frontmatter = re.match(r"^---\n(.*?)\n---\n", skill_text, re.DOTALL)
    require(frontmatter is not None, "SKILL.md is missing YAML frontmatter", errors)

    if frontmatter is not None:
        fields: dict[str, str] = {}
        for line in frontmatter.group(1).splitlines():
            match = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
            require(match is not None, f"invalid frontmatter line: {line}", errors)
            if match is not None:
                fields[match.group(1)] = match.group(2).strip()

        require(
            set(fields) == {"name", "description"},
            "frontmatter must contain only name and description",
            errors,
        )
        name = fields.get("name", "")
        require(name == "dont-stop", "skill name must be dont-stop", errors)
        require(
            re.fullmatch(r"[a-z0-9-]{1,64}", name) is not None,
            "skill name must use lowercase letters, digits, and hyphens",
            errors,
        )
        require(bool(fields.get("description")), "description must not be empty", errors)

    if agent_path.is_file():
        agent_text = agent_path.read_text(encoding="utf-8")
        require(
            'display_name: "Don\'t Stop"' in agent_text,
            "agents/openai.yaml has the wrong display name",
            errors,
        )
        require(
            "$dont-stop" in agent_text,
            "agents/openai.yaml default prompt must mention $dont-stop",
            errors,
        )

    if readme_path.is_file():
        readme = readme_path.read_text(encoding="utf-8")
        require(
            "README.zh-CN.md" in readme,
            "README.md is missing the Chinese-language link",
            errors,
        )

    if readme_zh_path.is_file():
        readme_zh = readme_zh_path.read_text(encoding="utf-8")
        require(
            "README.md" in readme_zh,
            "README.zh-CN.md is missing the English-language link",
            errors,
        )

    return errors


def main() -> int:
    root = (
        Path(sys.argv[1]).expanduser().resolve()
        if len(sys.argv) > 1
        else Path(__file__).resolve().parents[1]
    )
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"OK: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
