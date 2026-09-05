---
name: ferris-native
description: C++ and Rust source, API, ownership, unsafe/FFI, async, performance, dependencies, and build work, including Cargo, compiler/linker fixes, and MSBuild. Windows platform and shell rules belong to ferris-windows.
---

# C++ and Rust Development

## Load the applicable language

- **C++ edits or review:** read the applicable sections of [references/cpp.md](./references/cpp.md).
- **Rust edits or review:** read the applicable sections of [references/rust.md](./references/rust.md).
- **Mixed-language boundary:** read both, concentrating on ABI, allocation/release ownership, errors, and lifetimes.
- **Windows targets or build scripts:** also apply ferris-windows. Do not load Windows details for a non-Windows-only task.

## Shared discipline

1. Respect the repository's supported compiler/MSRV, standard/edition, build/dependency policy, and conventions. House defaults are for new or unconstrained projects, not permission to migrate existing code.
2. Make ownership and lifetime explicit. Prefer RAII/safe wrappers; do not duplicate owners, retain dangling views, or release asynchronous resources before completion. Document public contracts and non-obvious failure, threading, allocation, and unsafe obligations.
3. Propagate actionable errors or handle them explicitly. Do not hide failure behind a default, an ignored result, or an incorrect `noexcept`/panic policy. Preserve existing safety and compatibility guarantees.
4. Reuse the canonical helper, standard library, or established dependency before hand-rolling. Do not force a new wrapper, runtime, builder, or crate split without a concrete need.
5. Measure the actual workload before specializing. Zero-copy, arenas, concurrency, and batching must respect ownership, backpressure, ordering, and cancellation; they are not universal defaults. Preserve promised allocation/latency contracts.

Use ferris-workflow for debugging, test design, final checks, and cleanup. Consult current vendor documentation when a change depends on API or toolchain availability; reusable guidance should not predict release support.
