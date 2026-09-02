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
- **Declare Windows imports through the official crates, not hand-written `extern "system"` blocks**: `windows-sys` for plain C-style calls, `windows`/`windows-core` for COM/WinRT, and the focused crates (`windows-registry`, `windows-threading`, …) when one covers the need. Every 0.x minor breaks APIs — pin the version and upgrade stepwise, never float it.
- **`PCWSTR`/`PWSTR` discipline**: a `&str` becomes UTF-16 via `HSTRING::from` or `to_vec_with_nul`; never `as_ptr()` a non-nul-terminated buffer, and keep the owning allocation alive for the call.
- **Check `windows::core::Result` / `HRESULT` with `?`** or explicit `ok_or`; a `BOOL` that is `FALSE` means call `GetLastError()` immediately, before any other call.
- **Wrap owned `HANDLE`s in a newtype with `Drop`** calling `CloseHandle`; never `mem::forget` or hand a raw handle to multiple owners. Borrowed/pseudo-handles (`GetCurrentProcess`) are never dropped.
- **DLL boundary portability**: only `#[repr(C)]` data crosses a DLL boundary — Rust-owned `String`/`Vec`/`Box` and any `#[repr(Rust)]` type must not be transferred between separately compiled DLLs; each DLL has its own statics, layouts, and type IDs.
- Windows platform rules (`W` entry points only, UTF-16 discipline, paths, locking, failure values) follow the ferris-windows skill — load it alongside this one.

## Async and zero-copy

- **No lock guard crosses `.await`.** `std::sync::Mutex` for short critical sections; `tokio::sync::Mutex` only when the guard must survive an await; keep clippy's `await_holding_lock` on. Blocking or CPU-heavy calls go to `spawn_blocking` — a blocked worker starves every task on it.
- **`select!` branches must be cancellation-safe.** The losing branch is dropped mid-flight; a lock-acquire await is not cancellation-safe — acquire outside the select or switch to a channel/notify.
- **Independent awaits run concurrently**, not sequentially: `join!`, `buffered(n)`, `buffered_unordered(n)` — a `for` loop of awaits sums the latencies.
- **Native `async fn` in traits** behind generics (stable); `dyn` dispatch needs `#[async_trait]` or `dynosaur` — native dyn-async is not stable yet.
- **Across an await or a `spawn` boundary, move ownership or share via `Arc`/`Bytes`** — a defensive `.clone()` to appease the borrow checker is a design smell, not a fix.
- **Parse by borrowing.** Parsed structures carry the input buffer's lifetime (`&'a str`, `&'a [u8]`); `Cow<'a, str>` only for the few fields that must be owned; fixed binary layouts use `zerocopy`-style primitives, never ad-hoc transmutes.
- **Network pipelines read into `BytesMut` and hand off frames as `Bytes`** via `split()`/`freeze()` — views of one shared buffer, not copies; codec code is written against the `Buf`/`BufMut` traits.
- **Size and reuse buffers deliberately.** `with_capacity` when the size is known; `read_buf` into spare capacity (not zero-initialized vecs); `BufWriter::with_capacity` on sinks; `IoSlice`/`write_vectored` for header+payload instead of concatenating. Workhorse buffers live across iterations and `clear()`; `clone_from` beats `clone` when overwriting.
- **`Box::leak` only for process-lifetime singletons** allocated once — in loops or long-running services it is a leak; share with `Arc` instead.
- **Hot-path hash maps earn their hasher**: profiling first; non-adversarial keys may move to `rustc-hash`/`ahash`/`foldhash`, but std's SipHash stays wherever keys touch untrusted input.
- **Lazy inits are std now**: `LazyLock`/`OnceLock` in new code; no new `lazy_static`/`once_cell` dependencies.

## Performance and structure

- Profile and optimize the hot path early; optimize for throughput (batch work) rather than micro empty cycles; long-running loops expose yield points.
- Libraries avoid global statics; system calls sit behind traits so they can be mocked.
- Split the crate when in doubt; features are additive and libraries work out of the box (no required config).
- **Edition 2024 module layout.** Manifests set `edition = "2024"`; module `foo` lives in `foo.rs` with its submodules under `foo/` — `foo/mod.rs` never appears, including when migrating older crates.
- Don't glob re-export; don't leak external types through public signatures. Complex construction goes through builders; essential functionality lives on inherent methods. Public APIs follow the Rust API Guidelines checklist.
- Static verification before hand-off: `cargo fmt --check`, `cargo clippy -- -D warnings`, `cargo test` (smallest targeted subset first).
