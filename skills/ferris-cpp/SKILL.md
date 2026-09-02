---
name: ferris-cpp
description: House C++ style, design, performance, and MSBuild discipline. Use when creating, modifying, reviewing, or refactoring any C++ code — .cpp/.h/.hpp/.cc/.cxx, templates, vcxproj/sln/MSBuild projects, MSVC builds — including one-line fixes and small helpers, and for C++ design or API questions. Also triggers on C++, MSVC, Visual Studio, STL, vcpkg, compiler or linker errors ending in C++ edits, hot-path, allocation, coroutine, async I/O, span, string_view, pmr, expected, move_only_function, or flat_map questions. Owns naming, modern syntax, contract comments, performance/async/zero-copy rules, dependency policy, and build layout. Win32, COM, and interop correctness belongs to ferris-windows.
---

# C++ Development

House style for every C++ change, however small. A codebase with its own established conventions wins on style — match the surrounding code there. Correctness rules do not bend to local habit: platform rules (ferris-windows), RAII ownership, and failure handling apply even where the surrounding code violates them.

**Process**:

1. Before the first C++ edit, read the sections of [references/style-and-design.md](./references/style-and-design.md) that govern the change — naming and modern syntax always; documentation, design playbook, performance, or build sections when the change touches them
2. Make every new or modified line conformant
3. Write comments in American English unless the user explicitly requests another language

## Non-negotiables (see references for detail)

1. **Latest-standard syntax.** Target the newest toolset standard (`/std:c++latest` / C++23); use the modern spelling of every construct — `concepts` over SFINAE, `<format>` over printf, `std::span` over pointer+size, structured bindings, designated initializers. Legacy spellings are review-blocking.
2. **Contracts in comments.** Every public declaration gets a comment stating what it does and — when non-obvious — ownership and failure behavior (returns false/empty, never throws from hot paths).
3. **`noexcept` on every function that cannot throw**, `[[nodiscard]]` on every function whose result is meaningful, `constexpr` wherever compile-time evaluation works.
4. **RAII for every OS resource**; raw new/delete and bare HANDLE storage are review-blocking. Scope guards (`make_scope_exit`) for non-RAII cleanup.
5. **No allocation on hot paths.** Preallocate at init; fail fast at `init()` instead of degrading silently. Build-then-free phases use `std::pmr` arenas (see references "Performance, async, and zero-copy").
6. **Zero-copy by default.** Borrowed views (`std::span`, `std::string_view`) are parameter types only, never members or returns that dangle; hot-path fallibility returns `std::expected`, not throws; async I/O is C++20 coroutines over IOCP — `std::execution` is C++26 and not in the MSVC STL yet.
7. **What the toolset ships wins.** The standard library and the Windows SDK come first; reach for a third-party library only when nothing shipped covers the need, and state the misfit where the code lands. Third-party code enters through vcpkg in manifest mode (`vcpkg.json` in the repo, restored by the build), never a vendored copy or a manual download.
8. **MSBuild is the build system.** Locate MSBuild via vswhere, check `if errorlevel 1`, exercise the configuration matrix a change can affect; keep `/W4` + `/sdl` + `stdcpplatest` (see references "Build and project layout").
