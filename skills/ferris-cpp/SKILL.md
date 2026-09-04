---
name: ferris-cpp
description: House discipline for C++ source, project, API, build, and performance work. Use for C++ code or project changes, design and API review, compiler or linker failures that require C++ edits, performance or asynchronous I/O work, dependency decisions, and MSBuild configuration. Windows platform, Win32, COM, and interop correctness belongs to ferris-windows.
---

# C++ Development

House defaults for new or unconstrained C++ projects. In an existing repository, its supported toolchain and language standard, build and dependency policy, and established conventions take precedence; do not force a migration. Portable safety and correctness obligations — platform contracts (ferris-windows), RAII ownership, and failure handling — still apply.

**Process**:

1. Before the first C++ edit, read the sections of [references/style-and-design.md](./references/style-and-design.md) that govern the change — naming and modern syntax always; documentation, design playbook, performance, or build sections when the change touches them
2. Make every new or modified line conformant
3. Write comments in American English unless the user explicitly requests another language

## House defaults and portable obligations (see references for detail)

1. **Latest-standard syntax is the unconstrained-project default.** New or unconstrained house projects target the newest toolset standard (`/std:c++latest` / C++23) and use modern spellings — `concepts` over SFINAE, `<format>` over printf, `std::span` over pointer+size, structured bindings, designated initializers. Constrained repositories use the modern spelling available within their supported standard rather than forcing a migration.
2. **Contracts in comments.** Every public declaration gets a comment stating what it does and — when non-obvious — ownership and failure behavior (returns false/empty, never throws from hot paths).
3. **`noexcept` on every function that cannot throw**, `[[nodiscard]]` on every function whose result is meaningful, `constexpr` wherever compile-time evaluation works.
4. **RAII for every OS resource**; raw new/delete and bare HANDLE storage are review-blocking. Scope guards (`make_scope_exit`) for non-RAII cleanup.
5. **No allocation on hot paths.** Preallocate at init; fail fast at `init()` instead of degrading silently. Build-then-free phases use `std::pmr` arenas (see references "Performance, async, and zero-copy").
6. **Zero-copy by default.** Borrowed views (`std::span`, `std::string_view`) are parameter types only, never members or returns that dangle; hot-path fallibility returns `std::expected`, not throws; async I/O is C++20 coroutines over IOCP — `std::execution` is C++26 and not in the MSVC STL yet.
7. **Toolset-first dependencies are the unconstrained-project default.** New or unconstrained house projects use the standard library and Windows SDK first, with third-party code entering through vcpkg manifest mode only for a stated misfit. Existing repositories retain their dependency policy unless a migration is requested.
8. **MSBuild is the unconstrained Windows-project default.** Existing repositories retain their established build system unless a migration is requested. Where MSBuild applies, locate it via vswhere, check `if errorlevel 1`, exercise the affected configuration matrix, and keep `/W4` + `/sdl` + the repository's selected language standard (see references "Build and project layout").
