# ferris-skills

A compact, cross-agent engineering skill collection. Three entry points share no mandatory loading chain: workflow, native languages, and Windows. Each loads only the references needed for the current task. Compatible with agents supporting the [Agent Skills format](https://agentskills.io/specification), including Pi and Claude Code.

## Skills

| Skill | Responsibility | Load only when needed |
|-------|----------------|-----------------------|
| [ferris-workflow](skills/ferris-workflow/SKILL.md) | Debugging, test design, completion evidence, diff hygiene, and cleanup | Debugging, tests, deletion proof, lifecycle/race analysis |
| [ferris-native](skills/ferris-native/SKILL.md) | C++ and Rust ownership, APIs, unsafe/FFI, performance, dependencies, and builds | C++ or Rust details; both for mixed-language boundaries |
| [ferris-windows](skills/ferris-windows/SKILL.md) | Windows paths, filesystem, encoding, DLLs, privileges, system APIs, and PowerShell/batch | Platform and encoding edge cases |

Examples: a Python regression uses workflow, not native or Windows rules. A Linux Rust change adds native's Rust reference, not C++ details. Windows C++ work uses all three entry points but only the relevant references.

## Design rules

- **Short descriptions route tasks.** They are always in context; implementation detail belongs in the body or a reference.
- **One owner per concern.** Workflow owns verification; native owns language details; Windows owns platform contracts. References link directly from their skill entry point.
- **No ritual loading.** A small fix does not require a deep-cleanup investigation. Current-state evidence can serve multiple claims without rerunning unchanged checks.
- **Prefer contracts over blanket prescriptions.** Keep repository conventions and safety guarantees. Specialize ownership, concurrency, allocation, and dependencies only for a concrete requirement; check installed toolchain/API support instead of embedding release predictions.
- **Keep verification real.** Preserve regression sensitivity, deletion proof, security/compatibility boundaries, and meaningful checks. Less instruction text is not evidence of better task success.

This structure follows the official [skill-authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) on concise instructions and progressive disclosure.

Validate locally with `python scripts/validate_skills.py`. CI runs the same validator: frontmatter/YAML safety, name/directory agreement, loader description limits, local links/reference mentions, orphan references, and README coverage. These checks validate packaging, not model behavior.

## Install and update

Interactive installation selects skills, agents, and scope:

```bash
npx skills add github:MCapricorns/ferris-skills
```

List or select global skills:

```bash
npx skills add github:MCapricorns/ferris-skills -l
npx skills add github:MCapricorns/ferris-skills -s ferris-workflow -g
npx skills add github:MCapricorns/ferris-skills -s '*' -g
npx skills update -g
```

Add `--copy` when symlinks are unsuitable. Manual installation: copy the desired `skills/<name>/` directories into `~/.agents/skills/` or the agent's own skill directory.

### Migrating from six skills

- `ferris-audit`, `ferris-debug`, and `ferris-tests` become `ferris-workflow`.
- `ferris-cpp` and `ferris-rust` become `ferris-native`.
- `ferris-windows` keeps its name.

An update may refresh existing names without installing replacements or removing retired names. Install the three current skills for the same agents/scope, then remove the five retired names to prevent duplicate instructions:

```bash
npx skills add github:MCapricorns/ferris-skills -s ferris-workflow ferris-native ferris-windows -g
npx skills remove ferris-audit ferris-debug ferris-tests ferris-cpp ferris-rust -g
```

Update explicit skill references in your own agent/project instructions, and reload skills or restart the agent after migration. No compatibility stubs remain to keep obsolete triggers active.
