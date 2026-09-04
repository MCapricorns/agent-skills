# ferris-skills

Personal cross-agent skill collection — the **ferris** family. Every skill is prefixed `ferris-` so the family groups together in any agent's skill list and never collides with third-party skills. Works with ZCode, Claude Code, Cursor, and any agent that discovers `~/.agents/skills/`.

## Design rules

Every skill here follows the same contract, tuned for reliable triggering:

- **The description is the trigger.** It states the skill's purpose in one clause, then generalized activation categories, a few discriminative terms, and boundaries with neighboring skills. It routes rather than summarizing the body. Keep it lean — it rides in every session's context.
- **One owner per rule.** Each concern lives in exactly one skill; neighbors point to it by name instead of restating it, and descriptions carry negative triggers ("X belongs to skill-y") so skills never fight over the same task.
- **Every skill is progressive disclosure.** SKILL.md carries one screen of load-bearing rules only — imperative lines, no rationale; the why, edge cases, tooling names, and examples live in `references/` and load only when a rule needs unpacking.

| Concern | Owner |
|---------|-------|
| Proof behind "done / fixed / passing" claims, diff hygiene at commit time, dead-code cleanup, simplification audits | ferris-audit |
| Root-cause process when anything is broken | ferris-debug |
| Test quality, mocks, regression tests | ferris-tests |
| Windows platform rules, PowerShell/batch scripting, Win32 system-call correctness from any language | ferris-windows |
| C++ style, design, performance, dependencies (vcpkg), MSBuild | ferris-cpp |
| Rust style, design, async, lints | ferris-rust |

CI enforces the contract mechanically — `python3 scripts/validate_skills.py` checks frontmatter shape and YAML safety, name/directory match, description length within loader limits, resolvable links and reference mentions, orphan reference files, and README coverage.

## Skills

### Discipline

- **ferris-audit** — the finish-line gate. No success claim without running the proving command fresh and reading its output (claims-to-proof table for tests, builds, bug fixes, requirements, performance claims, and subagent reports); and a mandatory pre-commit pass that cleans the staged diff even when nobody asks — new APIs must have same-diff consumers, structural churn rides separately from behavior changes. Explicit-intent deep cleanup applies proven cuts end to end with a proof ladder for every deletion; read-only simplification surveys rank evidence and never edit.

### Process

- **ferris-debug** — root cause before any fix: read the evidence, reproduce reliably, diff against last-good, instrument boundaries, trace bad values to their origin, one hypothesis at a time, fix with a regression test seen red first; checks are never weakened to go green, and three failed fixes escalate to questioning the design.
- **ferris-tests** — tests that catch real breaks: name the break first, watch every new test fail then pass, hand-derived expectations (property tests when expectations resist hand-derivation), no change detectors, mocks earn no assertions, tests frozen while implementing, mutation check before finishing.

### House style

- **ferris-windows** — Windows platform discipline for ANY code that runs on Windows, no API call required: MAX_PATH and `\\?\` long paths, case-insensitive filenames and reserved device names, open files locked by running processes (sharing violations, linker LNK1168), DLL search order, the full mojibake cure for console/file encoding (OEM code pages, `SetConsoleOutputCP(CP_UTF8)` vs `ReadConsoleW`, MSVC `/utf-8`, `activeCodePage` manifest, pipe boundaries), virtual terminal sequences, symlinks needing Developer Mode, UAC elevation. Plus shell discipline for the scripts that drive builds (`$LASTEXITCODE` over `$?`, no `&&` on PowerShell 5.1, explicit output encoding) and Win32 system-call correctness in any language: Unicode `W` APIs only, bytes vs UTF-16 code units, documented failure values (`HRESULT`, `LSTATUS`, `GetLastError`), RAII handle ownership, `cbSize` initialization, pointer-sized types. Rust `windows`-crate wrapper discipline lives in ferris-rust; languages with no house skill (C#, PowerShell) run on these rules alone.
- **ferris-cpp** — house C++ discipline: latest-standard syntax (concepts, `<format>`, `std::span`, `std::expected`), PascalCase/snake_case naming, trailing return types with `auto` by default, `noexcept`/`[[nodiscard]]` contracts, contract comments, fail-fast init with EH-free hot paths, zero-copy borrowing (`std::pmr` arenas, view-lifetime rules), C++20-coroutine async over IOCP, what the toolset ships before any third party (and vcpkg manifest mode for the rest), and vswhere/MSBuild build discipline.
- **ferris-rust** — house Rust discipline: panic = programming bug vs `Result` = situational failure, errors never swallowed (`.ok()?`, `let _ =`, `unwrap_or*` are all banned), `unsafe` restraint with mandatory `Safety` sections, no weasel-word names, `#[expect]` lint overrides, edition 2024 with the `foo.rs` + `foo/` layout (`mod.rs` banned), M-CANONICAL-DOCS documentation, API design rules, established crates over hand-rolling, and tokio-based async/zero-copy discipline (no guards across `.await`, `spawn_blocking` for blocking work, borrowed parses, `Bytes` views). Windows FFI defers to ferris-windows for platform rules.

## Install

Interactive — the CLI asks which skills, which agents, and global or project scope:

```bash
npx skills add github:MCapricorns/ferris-skills
```

Headless picks:

```bash
npx skills add github:MCapricorns/ferris-skills -l                  # list before choosing
npx skills add github:MCapricorns/ferris-skills -s ferris-audit -g  # one skill, global
npx skills add github:MCapricorns/ferris-skills -s '*' -g           # every skill, global
```

Add `--copy` to copy files instead of symlinking. Update later:

```bash
npx skills update -g
```

Manual: copy `skills/<name>/` into `~/.agents/skills/` (or your agent's skills directory).
