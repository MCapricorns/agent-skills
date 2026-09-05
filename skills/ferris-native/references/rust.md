# Rust Design and Build Details

Read the sections relevant to the change; repository MSRV, edition, layout, and dependency policy take precedence over house defaults.

## API and error discipline

- New unconstrained crates use edition 2024 and `foo.rs` with submodules under `foo/`; this layout is not an edition requirement. Name types by their domain role rather than vague `Manager`/`Service` labels. Add builders or newtypes when they encode real construction or semantic constraints.
- Return `Result` for situational failures and validate untrusted inputs at the boundary. Reserve panics for programming errors or an explicit caller contract; use types to make invalid states unrepresentable where practical. A panic may unwind a task/thread or abort the process according to the build/runtime policy; it does not universally mean process shutdown. Respect the chosen poisoned-lock policy rather than ignoring poison.
- Propagate actionable errors with `?` or handle them explicitly. Do not use `.ok()`, `.ok()?`, `let _ =`, `unwrap_or*`, or a bare `if let Ok` to conceal an unexpected failure. Intentional absence or fallback must be part of the API contract, not accidental loss of an error the caller needs.
- Applications may use `anyhow`; libraries expose concrete errors callers can inspect. Avoid redundant logging at every propagation layer and do not stringify away error structure prematurely.
- Prefer `#[expect(lint, reason = "...")]` when supported by the MSRV. Keep overrides narrow; use `#[allow]` only where an expectation is unsuitable, such as generated code or configurations where the lint may not fire.
- Document public items with a summary and applicable `Examples`, `Errors`, `Panics`, `Safety`, and `Abort` sections. Explain parameters in prose, not boilerplate tables; document module purpose and contracts. Use inherent methods for essential functionality, additive features, and deliberate public re-exports/dependency types.

## Unsafe and FFI

- Prefer safe APIs. `unsafe fn`, unsafe extern statics, and `unsafe trait` define caller/access/implementor obligations relevant to undefined behavior, documented in `# Safety`; destructive behavior alone does not make an API unsafe.
- Keep unsafe operations small and give each block a nearby `// SAFETY:` proof. An `unsafe impl` explains why implementor invariants hold; `unsafe extern` establishes correct ABI/signatures; unsafe attributes need their own symbol/linkage proof. An enclosing `unsafe fn` is not a blanket proof for its body.
- Use ABI-compatible signatures and layouts at foreign or independently compiled DLL boundaries. `#[repr(C)]` alone does not make fields FFI-safe. Do not transfer Rust-layout `String`/`Vec`/`Box` as an ABI contract; expose opaque handles with explicit allocation/release ownership instead. Do not unwind through an ABI that forbids it.
- For Windows, prefer official bindings: `windows-sys` for C-style calls, `windows`/`windows-core` for COM/WinRT, or a focused crate already covering the need. Inspect the generated signature: wrappers may already convert failure sentinels to `Result`.
- Keep UTF-16 owners alive through calls and supply terminators only where required. Rust paths may contain unpaired surrogates; use `OsStr`/`Path` platform conversions rather than forcing them through UTF-8 `str`. Wrap owned handles with the matching release operation; never drop borrowed/pseudo-handles or duplicate raw ownership. Other platform contracts belong to ferris-windows.

## Async and cancellation

Use the existing runtime; Tokio is the house default when an async runtime is actually needed.

- Release blocking mutex guards before `.await`. A Tokio async mutex guard may deliberately span `.await` when the resource protocol requires it; keep that scope minimal and consider a dedicated owner task for complex shared I/O. Use ordinary mutexes for short, non-awaiting data access.
- Move blocking work off executor workers. Bound CPU-heavy concurrency or use the existing CPU pool; sending unlimited CPU jobs to `spawn_blocking` can oversubscribe the machine. Once started, a blocking task cannot be stopped by `abort`; shutdown needs cooperative termination or explicit waiting.
- Dropping a losing `select!` future does not roll back its side effects. Check the operation's cancellation contract, including partial progress and lock/queue fairness, before retrying. Do not replace a mutex with a notification merely to silence a cancellation concern.
- Run independent work concurrently only with explicit bounds, ordering, error, and cancellation semantics. Do not turn every loop into unbounded spawning. A dropped join handle is not proof that a task stopped.
- Borrow across awaits when the owner remains valid; spawned work may require owned or shared state. Use `Arc`/`Bytes` where sharing is real, not to conceal unclear ownership. A deliberate small copy can be simpler than retaining a large shared buffer.
- Native `async fn` in traits suits generic dispatch when supported. For dynamic dispatch, check the supported language capabilities and existing project's adapter before introducing a macro crate.

## Dependencies, performance, and checks

- Prefer the standard library or established crates over hand-rolling, following the repository's dependency policy. Use compatible Cargo requirements; pre-1.0 minor releases can break compatibility. Do not exact-pin or add a runtime merely by habit.
- Profile before changing storage, hashing, or crate boundaries. Borrow parsed input where lifetimes stay simple; use `Cow` when some fields need ownership. For network buffers, `BytesMut`/`Bytes`, reuse, and vectored I/O can avoid copies, but shared slices can retain a much larger allocation.
- Keep arenas/buffers and their consumers in a clear lifetime. `Box::leak` is for intentional process-lifetime storage, not recurring work. Do not use ad-hoc transmutes for binary parsing.
- Keep collision-resistant hashing for attacker-controlled keys; alternate hashers need a measured workload and a trusted-input boundary. Prefer `LazyLock`/`OnceLock` when the MSRV supports them instead of adding redundant dependencies.
- Use narrow test seams at real external boundaries, not a trait for every system call. Split modules/crates by ownership and reuse, not "when in doubt".
- Run the smallest relevant test first, then `cargo fmt --check`, `cargo clippy -- -D warnings`, and `cargo test` with the repository's supported targets/features. Do not assume `--all-features` is meaningful for every crate or lower existing gates.

API details when needed: [Tokio mutex](https://docs.rs/tokio/latest/tokio/sync/struct.Mutex.html), [cancellation in select](https://docs.rs/tokio/latest/tokio/macro.select.html), and [blocking tasks](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html).
