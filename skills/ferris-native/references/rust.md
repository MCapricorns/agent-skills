# Rust Contracts and Runtime Traps

## API and edition

New unconstrained crates use edition 2024 and `foo.rs` with children under `foo/`; the layout is a house preference, not an edition rule.

- Validate untrusted inputs at the boundary. Use `Result` for situational errors, panics only for programming errors or a stated contract. Keep inspectable library errors; applications may use `anyhow`. Do not erase needed failures with `.ok()`, ignored results, or fallbacks. Panic unwind/abort and poisoned-lock behavior follow the existing build/runtime policy.
- Use narrow `#[expect(lint, reason = "...")]` where the MSRV supports it; `#[allow]` remains appropriate when an expectation cannot reliably fire. Keep essential operations inherent and features additive.
- Edition 2024 return-position `impl Trait` captures all in-scope generic parameters unless constrained with `use<..>`; tail-expression temporaries have narrower scopes. Inspect these contracts before adding clones, `'static`, or lifetime workarounds copied from another edition.

## Unsafe and FFI

- `unsafe fn`/traits/extern statics specify obligations needed to avoid undefined behavior. Document them in `# Safety` with local `// SAFETY:` proofs. An enclosing `unsafe fn` is no blanket proof.
- Across foreign or independently compiled DLL boundaries, use compatible signatures/layouts and explicit allocation/release ownership. `#[repr(C)]` does not make arbitrary fields FFI-safe; do not expose Rust-layout `String`/`Vec`/`Box` as the ABI. Use opaque handles and never unwind through a non-unwinding ABI.
- On Windows, prefer `windows-sys` for C-style calls and `windows`/`windows-core` for COM/WinRT, or the existing focused crate. Inspect generated signatures: failure sentinels may already become `Result`. Keep UTF-16 owners alive with required terminators; `OsStr`/`Path` conversions preserve unpaired surrogates that UTF-8 `str` cannot. Owned handles need matching release; borrowed/pseudo-handles must not be dropped or duplicated as owners.

## Async and cancellation

Use the existing runtime; Tokio is the house default only when a runtime is needed.

- Release blocking mutex guards before `.await`. An async mutex may span `.await` for a resource protocol; keep the scope small or use an owner task for complex I/O.
- Move blocking work off executor workers, but bound CPU-heavy `spawn_blocking` work or use the CPU pool. Started blocking tasks cannot be aborted. A dropped join handle does not prove termination.
- A losing `select!` future can leave side effects or partial progress. Check the operation's cancellation contract, not just its return type.
- Bound spawned work and retain error, ordering, and cancellation semantics. `Arc`/`Bytes` are for real sharing; a small copy can avoid retaining a large buffer.

## Storage and dependencies

- Preserve collision-resistant hashing for attacker-controlled keys. Shared slices can retain large allocations; `Box::leak` is for intentional process-lifetime storage, not recurring work. No ad-hoc transmutes for binary parsing.
- Follow Cargo dependency policy: pre-1.0 minor releases can break compatibility. Do not exact-pin, add a runtime, or replace MSRV-supported `LazyLock`/`OnceLock` with a dependency by habit. `--all-features` is not valid for every crate; preserve existing gates.

Consult when relevant: [2024 capture rules](https://doc.rust-lang.org/edition-guide/rust-2024/rpit-lifetime-capture.html), [temporary scopes](https://doc.rust-lang.org/edition-guide/rust-2024/temporary-tail-expr-scope.html), [Tokio mutex](https://docs.rs/tokio/latest/tokio/sync/struct.Mutex.html), [select cancellation](https://docs.rs/tokio/latest/tokio/macro.select.html), [blocking tasks](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html).
