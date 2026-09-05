# ferris-skills

Three cross-agent engineering skills focused on house choices and easily missed contracts, not language tutorials or generic coding advice. Compatible with the [Agent Skills format](https://agentskills.io/specification), including Pi and Claude Code.

Primary development environment: **Windows with PowerShell 7 (`pwsh`)**. Command examples use PowerShell; other hosts and legacy shells are compatibility targets, not defaults.

## Skills

| Skill | Use for | On-demand references |
|-------|---------|----------------------|
| [ferris-workflow](skills/ferris-workflow/SKILL.md) | Diagnosing a failure, writing a sensitive test, proving a deletion, or simplifying lifecycle/races | Debugging, test sensitivity, deletion proof, lifecycle/races |
| [ferris-native](skills/ferris-native/SKILL.md) | C++/Rust ownership, unsafe/FFI, async cancellation, or compiler/linker and Cargo/MSBuild failures | C++ or Rust; both for mixed-language boundaries |
| [ferris-windows](skills/ferris-windows/SKILL.md) | Windows paths, encoding, DLL loading, elevation, or Win32/COM/PInvoke | Paths, share modes, DLL search, encoding, privilege, GUI |

Load by task, not by chain: a Python regression needs workflow, not native; Linux Rust needs no Windows rules. References link directly from their entry point.

## Design rules

- **Keep the delta over model knowledge.** House preferences and consequential traps stay; syntax tutorials, investigation itineraries, and generic caution do not.
- **Descriptions only say when.** A short trigger for the concrete action, not the whole domain, and not "before every commit." The body is a router; read only the reference the task needs.
- **One concern, one owner.** Workflow owns diagnosis/tests/cleanup, native owns language contracts, Windows owns platform behavior.
- **Finish requested work.** Do not require a review stop after a first draft. Ask only at decisions the user would actually want to make. Repository conventions win; check current vendor docs when adopting a feature.
- **Preserve guarantees.** Shorter text must keep regression sensitivity, deletion proof, security/compatibility boundaries, and meaningful checks.

See the official [skill-authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) for concision and progressive disclosure.

Run `python scripts/validate_skills.py`. CI uses the same validator for frontmatter/YAML safety, naming/description limits, local references, orphan references, and README coverage. It checks packaging, not model effectiveness.

## Install and update

Interactive installation selects skills, agents, and scope:

```powershell
npx skills add github:MCapricorns/ferris-skills
```

List, install all globally, or update global installations:

```powershell
npx skills add github:MCapricorns/ferris-skills -l
npx skills add github:MCapricorns/ferris-skills -s '*' -g
npx skills update -g
```

Use `-s ferris-workflow` to select one skill. Add `--copy` if symlinks are unsuitable. Manual installation: copy desired `skills/<name>/` directories into `~/.agents/skills/` or the agent's own skill directory. Reload skills or restart the agent after updating.

### Migrating from six skills

`ferris-audit`, `ferris-debug`, and `ferris-tests` become `ferris-workflow`; `ferris-cpp` and `ferris-rust` become `ferris-native`; `ferris-windows` keeps its name. Updating existing names may not install replacements or remove retired names. Install replacements for the same agents/scope before removing old names:

```powershell
npx skills add github:MCapricorns/ferris-skills -s ferris-workflow ferris-native ferris-windows -g
npx skills remove ferris-audit ferris-debug ferris-tests ferris-cpp ferris-rust -g
```

Update explicit references in agent/project instructions and reload. No compatibility stubs keep retired triggers active.
