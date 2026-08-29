---
name: ms-rust
description: ALWAYS use this skill BEFORE writing or modifying ANY Rust code (.rs files), even for small snippets. Enforces the house Rust style (no weasel words, documented magic values, #[expect] lint overrides), panic/error discipline, M-CANONICAL-DOCS documentation with compliance comments, unsafe/FFI restraint, and API design rules. This skill is MANDATORY for all Rust development.
---

# Rust Development

This skill enforces the house Rust coding standards when creating or modifying Rust code.

## Instructions

**CRITICAL**: This skill MUST be invoked for ANY Rust code operation, including:

- Creating new .rs files (even small helpers)
- Modifying existing .rs files (any change, no matter how small)
- Reviewing or refactoring Rust code

**Process**:

1. Read [references/style-and-design.md](./references/style-and-design.md)
2. Before writing/modifying ANY Rust code, ensure edits are conformant
3. Document every public item with M-CANONICAL-DOCS sections (`Examples`/`Errors`/`Panics`/`Safety`/`Abort` when applicable)
4. Comments must ALWAYS be written in American English, unless the user explicitly requests a different language
5. If the file is fully compliant, add a comment: `// Rust guideline compliant {date}` where {date} is the guideline date/version

**No exceptions**: Even for trivial code, guidelines must be followed.

## Non-negotiables (see references for detail)

1. **Panics mean "stop the program".** Panic only on programming errors and poisoned locks; return `Result` for situational failures. Never introduce an `Error` type for contract violations.
2. **`unsafe` implies UB.** Mark a function `unsafe` only when misuse can cause undefined behavior; every `unsafe` block carries a `Safety` doc section listing caller obligations. Prefer safe APIs (e.g., `windows` crate wrappers) over raw FFI.
3. **No weasel words.** No `Manager`/`Service`/`Factory` types; name by what the type does (`Bookings`, `BookingDispatcher`); `Builder` is the canonical factory.
4. **Windows API calls follow the ms-win32 skill** — Unicode `W` APIs, documented failure values, handle RAII. Do not restate those rules here.
