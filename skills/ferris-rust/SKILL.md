---
name: ferris-rust
description: House discipline for Rust source, Cargo projects, APIs, builds, and performance-sensitive work. Use for Rust code or workspace changes, design and API review, compiler or Clippy failures that require Rust edits, unsafe or asynchronous code, and performance work. Windows platform and FFI correctness belongs to ferris-windows.
---

# Rust Development

House defaults for new or unconstrained Rust projects. In an existing repository, its supported toolchain/MSRV, edition, build and dependency policy, and established conventions take precedence; do not force a migration. Portable safety and correctness obligations — platform contracts (ferris-windows), error discipline, and `unsafe` obligations — still apply.

**Process**:

1. Before the first Rust edit, read the sections of [references/style-and-design.md](./references/style-and-design.md) that govern the change — naming and error discipline always; documentation, unsafe/FFI, dependency, async, or performance sections when the change touches them
2. Make every new or modified line conformant
3. Document every public item with M-CANONICAL-DOCS sections (`Examples`/`Errors`/`Panics`/`Safety`/`Abort` when applicable)
4. Write comments in American English unless the user explicitly requests another language

## House defaults and portable obligations (see references for detail)

1. **Panics mean "stop the program".** Panic only on programming errors and poisoned locks; return `Result` for situational failures. Never introduce an `Error` type for contract violations.
2. **`unsafe` marks explicit UB obligations.** `unsafe fn`, `unsafe static`, and `unsafe trait` define documented caller, access, and implementor obligations respectively. `unsafe {}` uses a nearby `// SAFETY:` proof; `unsafe impl`, `unsafe extern`, and `#[unsafe(...)]` each require context-appropriate proof that their invariants, ABI/signatures, or attribute requirements are satisfied. Prefer safe APIs over raw FFI.
3. **No weasel words.** No `Manager`/`Service`/`Factory` types; name by what the type does (`Bookings`, `BookingDispatcher`); `Builder` is the canonical factory.
4. **Errors are never swallowed.** No `.ok()?` (a `Result` demoted to `Option` erases the error), no `let _ =` on fallible calls, no `.ok()`/`.unwrap_or*`/bare `if let Ok` used to make failure invisible. Propagate with `?` or handle and record the error.
5. **Edition 2024 and the `foo.rs` + `foo/` module layout are unconstrained-project defaults.** New or unconstrained house crates use them; existing repositories retain their supported edition/MSRV and established layout unless a migration is requested.
6. **Windows platform rules follow the ferris-windows skill** (W entry points, UTF-16, paths, locking, failure values) — load it alongside; the Rust-side FFI specifics live in references "Unsafe, FFI, and Windows APIs".
7. **Zero-copy by default; async never blocks.** Parsed structures borrow the input buffer, network frames move as `Bytes` views of one buffer, lock guards never cross `.await`, and blocking or CPU-heavy work goes to `spawn_blocking` (see references "Async and zero-copy").
