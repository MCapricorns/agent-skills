#!/usr/bin/env python3
"""Enforce the repository's skill contract (see README "Design rules").

Checks every skills/<name>/SKILL.md for:
  - frontmatter shape: `---`, `name:` + `description:` single-line plain
    scalars, closing `---` — the strictest form every agent loader parses
  - YAML plain-scalar safety: no `: `, no ` #`, no leading indicator char
  - name matches the directory, is lowercase kebab-case, unique, <= 64 chars
  - description non-empty and <= 1024 chars (Claude Code loader limit)
  - every relative markdown link and every `references/*.md` mention resolves
  - no orphan files under references/ (each must be cited from SKILL.md)
  - every skill directory is mentioned in the top-level README

Dependency-free on purpose: single-line plain scalars are the one frontmatter
shape that naive and full YAML parsers read identically.

Exit code 0 when clean; 1 with one line per violation otherwise.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
README = REPO_ROOT / "README.md"

NAME_RE = re.compile(r"^[a-z][a-z0-9-]{0,63}$")
MD_LINK_RE = re.compile(r"\]\(([^)\s]+)\)")
BARE_REF_RE = re.compile(r"\breferences/[A-Za-z0-9._-]+\.md\b")
# Characters that change the meaning of a plain scalar when they lead it.
YAML_INDICATORS = set("-?:,[]{}#&*!|>'\"%@`")

MAX_DESCRIPTION = 1024

errors: list[str] = []


def fail(path: Path, message: str) -> None:
    errors.append(f"{path.relative_to(REPO_ROOT)}: {message}")


def parse_frontmatter(path: Path, text: str) -> dict[str, str]:
    """Parse the strict frontmatter shape; report every deviation."""
    lines = text.split("\n")
    if not lines or lines[0] != "---":
        fail(path, "must start with a `---` frontmatter fence")
        return {}
    fields: dict[str, str] = {}
    for index, line in enumerate(lines[1:], start=1):
        if line == "---":
            break
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*): (\S.*)$", line)
        if not match:
            fail(path, f"frontmatter line {index + 1} is not a single-line `key: value` pair: {line[:60]!r}")
            continue
        key, value = match.group(1), match.group(2)
        if key in fields:
            fail(path, f"duplicate frontmatter key `{key}`")
        fields[key] = value
        if value != value.strip():
            fail(path, f"`{key}` has leading/trailing whitespace")
        if "\t" in value:
            fail(path, f"`{key}` contains a tab character")
        if value[0] in YAML_INDICATORS:
            fail(path, f"`{key}` starts with `{value[0]}`, which YAML parses as an indicator — reword or quote")
        if ": " in value:
            fail(path, f"`{key}` contains `: `, which breaks YAML plain scalars — reword it")
        if " #" in value:
            fail(path, f"`{key}` contains ` #`, which starts a YAML comment and silently truncates — reword it")
    else:
        fail(path, "frontmatter fence `---` is never closed")
    unexpected = sorted(set(fields) - {"name", "description"})
    if unexpected:
        fail(path, f"unexpected frontmatter keys: {', '.join(unexpected)}")
    return fields


def check_links(path: Path, text: str) -> None:
    """Every relative markdown link must resolve from the containing file."""
    for target in MD_LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        resolved = (path.parent / target.split("#", 1)[0]).resolve()
        if not resolved.exists():
            fail(path, f"markdown link `{target}` does not resolve")


def check_skill(skill_dir: Path, seen_names: dict[str, Path]) -> None:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        fail(skill_dir, "missing SKILL.md")
        return
    text = skill_md.read_text(encoding="utf-8")
    fields = parse_frontmatter(skill_md, text)

    name = fields.get("name")
    if name is None:
        fail(skill_md, "frontmatter is missing `name`")
    else:
        if not NAME_RE.match(name):
            fail(skill_md, f"name `{name}` is not lowercase kebab-case (max 64 chars)")
        if name != skill_dir.name:
            fail(skill_md, f"name `{name}` does not match directory `{skill_dir.name}`")
        if name in seen_names:
            fail(skill_md, f"name `{name}` already used by {seen_names[name].relative_to(REPO_ROOT)}")
        seen_names.setdefault(name, skill_md)

    description = fields.get("description")
    if description is None:
        fail(skill_md, "frontmatter is missing `description`")
    elif len(description) > MAX_DESCRIPTION:
        fail(skill_md, f"description is {len(description)} chars; loaders cap at {MAX_DESCRIPTION}")

    body = text.split("\n---\n", 1)
    if len(body) < 2 or not body[1].strip():
        fail(skill_md, "no body after the frontmatter")

    # Bare `references/foo.md` mentions resolve from the skill root.
    for mention in set(BARE_REF_RE.findall(text)):
        if not (skill_dir / mention).is_file():
            fail(skill_md, f"mentions `{mention}`, which does not exist")

    for md_file in sorted(skill_dir.rglob("*.md")):
        check_links(md_file, md_file.read_text(encoding="utf-8"))

    references_dir = skill_dir / "references"
    if references_dir.is_dir():
        for ref in sorted(references_dir.rglob("*.md")):
            rel = ref.relative_to(skill_dir).as_posix()
            if rel not in text:
                fail(ref, f"orphan reference: never mentioned in {skill_dir.name}/SKILL.md")


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"{SKILLS_DIR} not found", file=sys.stderr)
        return 1
    skill_dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir() and not d.name.startswith("."))
    if not skill_dirs:
        print("no skills found", file=sys.stderr)
        return 1

    seen_names: dict[str, Path] = {}
    for skill_dir in skill_dirs:
        check_skill(skill_dir, seen_names)

    readme_text = README.read_text(encoding="utf-8") if README.is_file() else ""
    for skill_dir in skill_dirs:
        if skill_dir.name not in readme_text:
            fail(README, f"skill `{skill_dir.name}` is not mentioned")

    if errors:
        for line in errors:
            print(f"FAIL {line}")
        print(f"\n{len(errors)} violation(s) across {len(skill_dirs)} skills")
        return 1
    print(f"OK: {len(skill_dirs)} skills pass the contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
