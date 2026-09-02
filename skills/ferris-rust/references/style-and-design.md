# Rust Style and Design

House standards distilled from the Microsoft Rust guidelines. Read once per session before writing Rust.

## Naming and idioms

- **No weasel words.** Types are named by what they do, not `Service`/`Manager`/`Factory`. An item handling many bookings is `Bookings`; one that submits them is `BookingDispatcher`. Repeatable instantiation asks for `impl Fn() -> Foo`, not a factory parameter; the canonical factory type is `Builder`.
- **Magic values are documented.** Prefer named constants; a comment must state why the value was chosen and what changing it affects.
- **Lint overrides use `#[expect]`, not `#[allow]`**, with a `reason = "..."` — stale expectations warn instead of accumulating. `#[allow]` is only for generated code and macros.
- **Prefer regular functions over associated functions** when no namespace or name collision is gained (`foo.is_valid()` beats `Foo::is_valid(foo)`).
- **Strong types over primitive obsession.** Newtypes with strict, documented semantics instead of bare `String`/`u64` parameters; accept `impl AsRef<str>` (etc.) where feasible so callers pass anything.

## Panic and error discipline

- **Panic = stop the program.** Valid panics: programming errors (`expect("must never happen")`), const contexts, caller-requested `unwrap`, poisoned locks. Anything else must return `Result`.
- **Contract violations panic; situational failures return `Result`.** `divide_by(x, y)` panics on `y == 0`; `parse_uri(s)` returns `Result` because parsing can legitimately fail.
- **Correct by construction beats panicking**: use the type system so invalid inputs cannot be expressed.
- Applications may use `anyhow`; libraries return concrete, canonical error structs. Never log or stringify an error away where a caller could act on it.
- **Never swallow an error.** `.ok()?`, `let _ = fallible()`, `.unwrap_or_default()`, and a bare `if let Ok(..)` with no else all erase the failure path — execution continues as if nothing failed. Propagate with `?` on `Result`, or handle and record the error. Demoting `Result` to `Option` (`.ok()?`) to dodge error handling is banned.

## Documentation (M-CANONICAL-DOCS)

```rust
/// Summary sentence < 15 words.
///
/// Extended documentation in free form.
///
/// # Examples   — one or more usage examples
/// # Errors     — for `Result` returns: known error conditions
/// # Panics     — when this may panic
/// # Safety     — for `unsafe`: all conditions the caller must uphold
/// # Abort      — when this may abort the process
pub fn foo() {}
```

- Summary sentence is mandatory; other sections appear when applicable.
- Parameters are explained in the prose (`/// Copies a file from `src` to `dst`.`), never as a `# Parameters` table.
- Modules carry module-level docs stating purpose and contracts.

## Unsafe, FFI, and Windows APIs

- **`unsafe fn` only when misuse implies UB.** `unsafe fn delete_database()` is a misuse of the marker — use another signal.
- Every `unsafe` block has a `// SAFETY:` comment or `# Safety` doc proving each invariant; prefer `unsafe`-free designs and safe wrapper crates.
- Win32 calls, FFI declarations, and DLL-boundary portability follow the ferris-windows skill; those rules are not restated here.

## Performance and structure

- Profile and optimize the hot path early; optimize for throughput (batch work) rather than micro empty cycles; long-running loops expose yield points.
- Libraries avoid global statics; system calls sit behind traits so they can be mocked.
- Split the crate when in doubt; features are additive and libraries work out of the box (no required config).
- **Edition 2024 module layout.** Manifests set `edition = "2024"`; module `foo` lives in `foo.rs` with its submodules under `foo/` — `foo/mod.rs` never appears, including when migrating older crates.
- Don't glob re-export; don't leak external types through public signatures. Complex construction goes through builders; essential functionality lives on inherent methods. Public APIs follow the Rust API Guidelines checklist.
- Static verification before hand-off: `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test` (smallest targeted subset first).
