---
name: ferris-rust
description: House Rust style and design discipline. Use when creating, modifying, reviewing, or refactoring any Rust code — .rs, Cargo.toml or workspace changes, cargo build/test/clippy/fmt, proc macros — including one-line fixes and small helpers, and for Rust API-design questions. Also triggers on Rust, cargo, crate, clippy, rustc errors, unsafe, lifetimes, traits, borrow-checker fights, async, tokio, await, spawn_blocking, cancellation safety, Bytes, zero-copy, allocation, or hot-path performance work. Owns naming, panic and error discipline, documentation, lints, API design, and async/zero-copy rules. Win32 FFI correctness belongs to ferris-windows.
---

# Rust Development

House style for every Rust change, however small. A codebase with its own established conventions wins over this file — match the surrounding code there.

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
6. **Windows platform rules follow the ferris-windows skill** (W entry points, UTF-16, paths, locking, failure values) — load it alongside; the Rust-side FFI specifics live in references "Unsafe, FFI, and Windows APIs".
7. **Zero-copy by default; async never blocks.** Parsed structures borrow the input buffer, network frames move as `Bytes` views of one buffer, lock guards never cross `.await`, and blocking or CPU-heavy work goes to `spawn_blocking` (see references "Async and zero-copy").
