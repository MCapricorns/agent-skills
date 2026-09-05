---
name: ferris-native
description: C++ and Rust engineering for ownership, unsafe/FFI, async cancellation, performance, dependencies, and compiler/linker or Cargo/MSBuild changes.
---

# Native Engineering

| Change | Read |
|--------|------|
| C++ | [references/cpp.md](./references/cpp.md) |
| Rust | [references/rust.md](./references/rust.md) |
| Mixed-language boundary | Both, especially ABI, allocation/release, errors, and lifetimes |

Repository compiler/MSRV, standard/edition, build system, dependency policy, and conventions take precedence. House defaults apply only to unconstrained projects, not unsolicited migrations. Check installed toolchain and current vendor support when adopting a feature; a calendar year is not a support matrix.

- Reuse canonical helpers and resource owners rather than adding wrappers, runtimes, builders, or crate splits without a consumer.
- Preserve actionable errors, safety/compatibility guarantees, and public ownership, threading, allocation, and failure contracts. Document non-obvious obligations; do not hide failures behind defaults or ignored results.
- Measure the workload before specializing storage or scheduling. Zero-copy, arenas, batching, and concurrency must preserve lifetimes, backpressure, ordering, cancellation, and promised allocation/latency bounds.

For Windows APIs or scripts, also apply ferris-windows. Use ferris-workflow for diagnosis, tests, verification, and cleanup; load only references relevant to the task.
