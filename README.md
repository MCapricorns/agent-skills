# agent-skills

Personal cross-agent skill collection. Works with ZCode, Claude Code, Cursor, and any agent that discovers `~/.agents/skills/`.

## Design rules

Every skill here follows the same contract, tuned for reliable triggering:

- **The description is the trigger.** It states what the skill is in one clause, then the concrete situations that should fire it — file types, tool names, quoted error text, and the phrasings people actually use. It never summarizes the skill's rules: agents that see a summary follow the summary and skip the body.
- **One owner per rule.** Each concern lives in exactly one skill; neighbors point to it by name instead of restating it, and descriptions carry negative triggers ("X belongs to skill-y") so skills never fight over the same task.
- **Lean bodies, progressive depth.** SKILL.md carries the load-bearing rules; the full standards live in `references/` and load only when needed.

| Concern | Owner |
|---------|-------|
| Diff hygiene at commit time, dead-code cleanup, simplification audits | pre-merge-audit |
| Proof behind "done / fixed / passing" claims | verification-before-completion |
| Root-cause process when anything is broken | systematic-debugging |
| Test quality, mocks, regression tests | writing-tests |
| Windows API correctness from any language | ms-win32 |
| C++ style, design, MSBuild | ms-cpp |
| Rust style, design, lints | ms-rust |
| Line endings, .gitattributes | git-line-endings |

CI enforces the contract mechanically — `python3 scripts/validate_skills.py` checks frontmatter shape and YAML safety, name/directory match, description length within loader limits, resolvable links and reference mentions, orphan reference files, and README coverage.

## Skills

### Discipline

- **pre-merge-audit** — mandatory pre-commit pass that cleans the staged diff (dead code, duplication, leftover debris) before any commit, push, merge, or PR; explicit-intent deep cleanup with a proof ladder for every deletion; read-only simplification surveys that rank evidence and never edit.
- **verification-before-completion** — no success claim without running the proving command fresh and reading its output; claims-to-proof table for tests, builds, bug fixes, requirements, and subagent reports.

### Process

- **systematic-debugging** — root cause before any fix: read the evidence, reproduce reliably, diff against last-good, instrument boundaries, trace bad values to their origin, test one hypothesis at a time, fix with a regression test; three failed fixes escalate to questioning the design.
- **writing-tests** — tests that catch real breaks: name the break first, watch every new test fail then pass, hand-derived expectations, no change detectors, mocks earn no assertions, mutation check before finishing.

### House style

- **ms-win32** — Windows/Win32/COM correctness in any language: Unicode `W` APIs only, bytes vs UTF-16 code units, documented failure values (`HRESULT`, `LSTATUS`, `GetLastError`), RAII handle ownership, and the cross-language FFI rules (Rust `windows`-crate discipline, DLL boundary portability) that language skills defer to.
- **ms-cpp** — house C++ discipline: latest-standard syntax (concepts, `<format>`, `std::span`, `std::expected`), PascalCase/snake_case naming, trailing return types, `noexcept`/`[[nodiscard]]` contracts, contract comments, fail-fast init with EH-free hot paths, and vswhere/MSBuild build discipline.
- **ms-rust** — house Rust discipline: panic = programming bug vs `Result` = situational failure, errors never swallowed (`.ok()?`, `let _ =`, `unwrap_or*` are all banned), `unsafe` restraint with mandatory `Safety` sections, no weasel-word names, `#[expect]` lint overrides, edition 2024 with the `foo.rs` + `foo/` layout (`mod.rs` banned), M-CANONICAL-DOCS documentation, and API design rules. Win32 FFI defers to ms-win32.

### Repo hygiene

- **git-line-endings** — the repository owns its line-ending contract: `.gitattributes` with explicit CRLF for Windows-tooling files, one-shot `git add --renormalize .`, `core.autocrlf` as belt-and-suspenders; triggered by LF/CRLF warnings, whole-file diffs, and `^M` churn.

## Install

One line — every skill, every detected agent, global:

```bash
npx skills add github:MCapricorns/agent-skills --all -g
```

Single skill:

```bash
npx skills add github:MCapricorns/agent-skills --skill pre-merge-audit -g
```

Add `--copy` to copy files instead of symlinking. Update later:

```bash
npx skills update -g
```

Manual: copy `skills/<name>/` into `~/.agents/skills/` (or your agent's skills directory).
