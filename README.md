# agent-skills

Personal cross-agent skill collection. Every skill auto-triggers on intent (not just literal keywords), carries only standard `name` + `description` frontmatter, and loads its full standards progressively from `references/` only when needed. Works with ZCode, Claude Code, Cursor, and any agent that discovers `~/.agents/skills/`.

## Skills

### pre-merge-audit

Mandatory pre-commit hygiene, two tiers:

- **Pre-commit pass (automatic, every commit)** — before any commit, push, merge, or PR: clean the staged diff (dead code, duplication, leftover debris, structural bloat the diff adds), prove every cut, run the smallest targeted checks, report; never commit unaudited changes.
- **Deep cleanup (explicit intent only)** — "clean this up before we commit", "remove the dead code": apply proven cuts anywhere in scope per `references/cleanup.md`, guided by the structural red lines in `references/structure.md` (1000-line files, tangled growth, thin wrappers, canonical helpers, preferred remedies).

### ms-win32

Windows/Win32 API coding discipline — mandatory before writing or modifying any Windows API, COM, or native interop code in any language (C/C++, Rust FFI, C#/P-Invoke, PowerShell): Unicode `W` APIs only (never `A`), bytes vs UTF-16 code units, documented failure values (`HRESULT`, `LSTATUS`, `GetLastError`), RAII ownership for handles, buffers, and COM allocations. Also owns Windows repo hygiene: git LF/CRLF line-ending contracts (`.gitattributes` + renormalize) and MSBuild via vswhere.

### ms-c++

House C++ coding discipline — mandatory before writing or modifying any C++ code. Naming (PascalCase types, snake_case functions, `k_` constants), syntax contracts (trailing return types, `noexcept`/`[[nodiscard]]`/`constexpr`), contract-comment documentation, the design playbook (pure public header, fail-fast init, EH-free preallocated hot paths), and MSBuild/vcxproj discipline (`/W4`, `/sdl`, `stdcpplatest`).

### ms-rust

Microsoft Rust coding guidelines — mandatory before writing or modifying any Rust code, even Hello World. Loads progressive guideline sections from `resources/` (universal, AI-friendly, safety, FFI, performance, documentation, library UX), applies M-CANONICAL-DOCS documentation format, adds compliance comments, and validates edits against the guidelines.

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
