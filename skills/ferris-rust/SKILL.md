---
name: ferris-rust
description: House discipline for Rust source, Cargo projects, APIs, builds, and performance-sensitive work. Use for Rust code or workspace changes, design and API review, compiler or Clippy failures that require Rust edits, unsafe or asynchronous code, and performance work. Windows platform and FFI correctness belongs to ferris-windows.
---

# Rust Development

House style for Rust changes. A codebase with its own established conventions wins on style — match the surrounding code there. Correctness rules do not bend to local habit: platform rules (ferris-windows), error discipline, and `unsafe` obligations apply even where the surrounding code violates them.

**Process**:

1. Before the first Rust edit, read the sections of [references/style-and-design.md](./references/style-and-design.md) that govern the change — naming and error discipline always; documentation, unsafe/FFI, dependency, async, or performance sections when the change touches them
2. Make every new or modified line conformant
3. Document every public item with M-CANONICAL-DOCS sections (`Examples`/`Errors`/`Panics`/`Safety`/`Abort` when applicable)
4. Write comments in American English unless the user explicitly requests another language

## Non-negotiables (see references for detail)

1. **Panics mean "stop the program".** Panic only on programming errors and poisoned locks; return `Result` for situational failures. Never introduce an `Error` type for contract violations.
2. **`unsafe` implies UB.** Mark a function `unsafe` only when misuse can cause undefined behavior; every `unsafe` block carries a `Safety` doc section listing caller obligations. Prefer safe APIs (e.g., `windows` crate wrappers) over raw FFI.
3. **No weasel words.** No `Manager`/`Service`/`Factory` types; name by what the type does (`Bookings`, `BookingDispatcher`); `Builder` is the canonical factory.
4. **Errors are never swallowed.** No `.ok()?` (a `Result` demoted to `Option` erases the error), no `let _ =` on fallible calls, no `.ok()`/`.unwrap_or*`/bare `if let Ok` used to make failure invisible. Propagate with `?` or handle and record the error.
5. **Edition 2024, no `mod.rs`.** Crates target `edition = "2024"`; a module lives in `foo.rs` beside its `foo/` directory — `mod.rs` files must not exist.
6. **Windows platform rules follow the ferris-windows skill** (W entry points, UTF-16, paths, locking, failure values) — load it alongside; the Rust-side FFI specifics live in references "Unsafe, FFI, and Windows APIs".
7. **Zero-copy by default; async never blocks.** Parsed structures borrow the input buffer, network frames move as `Bytes` views of one buffer, lock guards never cross `.await`, and blocking or CPU-heavy work goes to `spawn_blocking` (see references "Async and zero-copy").
