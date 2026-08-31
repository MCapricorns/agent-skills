---
name: ferris-rust
description: House Rust style and design discipline. Use when creating, modifying, reviewing, or refactoring any Rust code — .rs files, Cargo.toml or workspace changes, cargo build, test, clippy, or fmt work, proc macros — including one-line fixes and small helpers, and when answering Rust API-design questions. Also triggers on Rust, cargo, crate, clippy, rustc errors, unsafe, lifetimes, traits, borrow-checker fights, and new crate setup. Owns naming, panic and error discipline, documentation, lints, and API design. Win32 FFI correctness belongs to ferris-windows.
---

# Rust Development

House style for every Rust change, however small.

**Process**:

1. Read [references/style-and-design.md](./references/style-and-design.md) once per session before the first Rust edit
2. Make every new or modified line conformant
3. Document every public item with M-CANONICAL-DOCS sections (`Examples`/`Errors`/`Panics`/`Safety`/`Abort` when applicable)
4. Write comments in American English unless the user explicitly requests another language
5. When the file is fully compliant, add a comment: `// Rust guideline compliant {date}` where {date} is the guideline date/version

## Non-negotiables (see references for detail)

1. **Panics mean "stop the program".** Panic only on programming errors and poisoned locks; return `Result` for situational failures. Never introduce an `Error` type for contract violations.
2. **`unsafe` implies UB.** Mark a function `unsafe` only when misuse can cause undefined behavior; every `unsafe` block carries a `Safety` doc section listing caller obligations. Prefer safe APIs (e.g., `windows` crate wrappers) over raw FFI.
3. **No weasel words.** No `Manager`/`Service`/`Factory` types; name by what the type does (`Bookings`, `BookingDispatcher`); `Builder` is the canonical factory.
4. **Errors are never swallowed.** No `.ok()?` (a `Result` demoted to `Option` erases the error), no `let _ =` on fallible calls, no `.ok()`/`.unwrap_or*`/bare `if let Ok` used to make failure invisible. Propagate with `?` or handle and record the error.
5. **Edition 2024, no `mod.rs`.** Crates target `edition = "2024"`; a module lives in `foo.rs` beside its `foo/` directory — `mod.rs` files must not exist.
6. **Windows API and FFI work follows the ferris-windows skill** — it owns the Win32 correctness, FFI declaration, and DLL-boundary rules. Load it alongside this one; its rules are deliberately not restated here.
