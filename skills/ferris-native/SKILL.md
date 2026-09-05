---
name: ferris-native
description: C++ and Rust ownership, unsafe/FFI, async cancellation, and build contracts. Use when a change hinges on those surfaces or on a compiler, linker, Cargo, or MSBuild failure.
---

# Native Engineering

| Change | Read |
|--------|------|
| C++ | [references/cpp.md](./references/cpp.md) |
| Rust | [references/rust.md](./references/rust.md) |
| Mixed-language boundary | Both, especially ABI, allocation/release, errors, and lifetimes |

Repository compiler/MSRV, standard/edition, build system, dependency policy, and conventions win. House defaults apply only to unconstrained projects. Check the installed toolchain and current vendor docs when adopting a feature.

Preserve public ownership, threading, allocation, and failure contracts. Do not hide failures behind defaults or ignored results.

For Windows APIs or scripts, also apply ferris-windows. Use ferris-workflow for diagnosis, tests, and cleanup; load only the references the task needs.
