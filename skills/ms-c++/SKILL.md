---
name: ms-c++
description: ALWAYS use this skill BEFORE writing or modifying ANY C++ code (.h/.cpp files), even for small snippets. Enforces the house C++ style (PascalCase types, snake_case functions, trailing return types, noexcept contracts), contract-comment documentation, MSBuild/vcxproj discipline, and the design playbook (layered public header, preallocated hot paths, EH-free core). This skill is MANDATORY for all C++ development.
---

# C++ Development

This skill enforces the house C++ coding standards when creating or modifying C++ code.

## Instructions

**CRITICAL**: This skill MUST be invoked for ANY C++ code operation, including:

- Creating new .h/.cpp files (even small helpers)
- Modifying existing C++ files (any change, no matter how small)
- Reviewing or refactoring C++ code

**Process**:

1. Read [references/style-and-design.md](./references/style-and-design.md)
2. Before writing/modifying ANY C++ code, ensure edits are conformant
3. Document every public symbol with a contract comment (what it does, ownership, failure behavior)
4. Comments must ALWAYS be written in American English, unless the user explicitly requests a different language
5. If the file is fully compliant, add a header comment: `// C++ guideline compliant {date}` where {date} is the guideline date/version

**No exceptions**: Even for trivial code, guidelines must be followed.

## Non-negotiables (see references for detail)

1. **Contracts in comments.** Every non-obvious function states its failure behavior (returns false/empty, never throws from hot paths) and ownership (who frees what) in a comment at the declaration.
2. **`noexcept` on every function that cannot throw**, `[[nodiscard]]` on every function whose result is meaningful, `constexpr` wherever compile-time evaluation works.
3. **RAII for every OS resource**; raw new/delete and bare HANDLE storage are review-blocking. Scope guards (`make_scope_exit`) for non-RAII cleanup.
4. **No allocation on hot paths.** Preallocate at init; fail fast at `init()` instead of degrading silently.
5. **MSBuild is the build system.** Locate MSBuild via vswhere (see ms-win32 skill); keep `/W4` + `/sdl` + `stdcpplatest`.
