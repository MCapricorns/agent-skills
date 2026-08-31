# ferris-skills

Personal cross-agent skill collection — the **ferris** family. Every skill is prefixed `ferris-` so the family groups together in any agent's skill list and never collides with third-party skills. Works with ZCode, Claude Code, Cursor, and any agent that discovers `~/.agents/skills/`.

## Design rules

Every skill here follows the same contract, tuned for reliable triggering:

- **The description is the trigger.** It states what the skill is in one clause, then the concrete situations that should fire it — file types, tool names, quoted error text, and the phrasings people actually use. It never summarizes the skill's rules: agents that see a summary follow the summary and skip the body.
- **One owner per rule.** Each concern lives in exactly one skill; neighbors point to it by name instead of restating it, and descriptions carry negative triggers ("X belongs to skill-y") so skills never fight over the same task.
- **Lean bodies, progressive depth.** SKILL.md carries the load-bearing rules; the full standards live in `references/` and load only when needed.

| Concern | Owner |
|---------|-------|
| Proof behind "done / fixed / passing" claims, diff hygiene at commit time, dead-code cleanup, simplification audits | ferris-audit |
| Root-cause process when anything is broken | ferris-debug |
| Test quality, mocks, regression tests | ferris-tests |
| Windows platform rules and Win32 API correctness from any language | ferris-windows |
| C++ style, design, MSBuild | ferris-cpp |
| Rust style, design, lints | ferris-rust |
| Line endings, .gitattributes | ferris-line-endings |

CI enforces the contract mechanically — `python3 scripts/validate_skills.py` checks frontmatter shape and YAML safety, name/directory match, description length within loader limits, resolvable links and reference mentions, orphan reference files, and README coverage.

## Skills

### Discipline

- **ferris-audit** — the finish-line gate. No success claim without running the proving command fresh and reading its output (claims-to-proof table for tests, builds, bug fixes, requirements, and subagent reports); and a mandatory pre-commit pass that cleans the staged diff even when nobody asks. Explicit-intent deep cleanup applies proven cuts end to end with a proof ladder for every deletion; read-only simplification surveys rank evidence and never edit.

### Process

- **ferris-debug** — root cause before any fix: read the evidence, reproduce reliably, diff against last-good, instrument boundaries, trace bad values to their origin, test one hypothesis at a time, fix with a regression test; three failed fixes escalate to questioning the design.
- **ferris-tests** — tests that catch real breaks: name the break first, watch every new test fail then pass, hand-derived expectations, no change detectors, mocks earn no assertions, mutation check before finishing.

### House style

- **ferris-windows** — Windows platform discipline for ANY code that runs on Windows, no API call required: MAX_PATH and `\\?\` long paths, case-insensitive filenames and reserved device names, open files locked by running processes (sharing violations, linker LNK1168), DLL search order, console code pages and UTF-8, symlinks needing Developer Mode, UAC elevation. Plus Win32/COM correctness in any language: Unicode `W` APIs only, bytes vs UTF-16 code units, documented failure values (`HRESULT`, `LSTATUS`, `GetLastError`), RAII handle ownership, and the cross-language FFI rules (Rust `windows`-crate discipline, DLL boundary portability) that language skills defer to.
- **ferris-cpp** — house C++ discipline: latest-standard syntax (concepts, `<format>`, `std::span`, `std::expected`), PascalCase/snake_case naming, trailing return types, `noexcept`/`[[nodiscard]]` contracts, contract comments, fail-fast init with EH-free hot paths, and vswhere/MSBuild build discipline.
- **ferris-rust** — house Rust discipline: panic = programming bug vs `Result` = situational failure, errors never swallowed (`.ok()?`, `let _ =`, `unwrap_or*` are all banned), `unsafe` restraint with mandatory `Safety` sections, no weasel-word names, `#[expect]` lint overrides, edition 2024 with the `foo.rs` + `foo/` layout (`mod.rs` banned), M-CANONICAL-DOCS documentation, and API design rules. Windows FFI defers to ferris-windows.

### Repo hygiene

- **ferris-line-endings** — the repository owns its line-ending contract: `.gitattributes` with `text=auto eol=lf` for text sources and explicit CRLF for Windows-tooling files, a one-shot index renormalize plus a one-shot worktree rewrite — `text=auto` alone does not stop the recurring LF/CRLF warning; triggered by LF/CRLF warnings, whole-file diffs, and `^M` churn.

## Install

One line — every skill, every detected agent, global:

```bash
npx skills add github:MCapricorns/ferris-skills --all -g
```

Single skill:

```bash
npx skills add github:MCapricorns/ferris-skills --skill ferris-audit -g
```

Add `--copy` to copy files instead of symlinking. Update later:

```bash
npx skills update -g
```

Manual: copy `skills/<name>/` into `~/.agents/skills/` (or your agent's skills directory).
