# C++ Style and Design

House standards for writing and reviewing C++. Read the sections that govern the change before writing C++.

## Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Types, classes, enums | PascalCase | `ScopeExit`, `FullPolicy` |
| Functions, methods | snake_case | `source_basename`, `try_acquire` |
| Namespaces | lowercase, short | `logging::detail` |
| Compile-time constants | `k_` prefix + snake_case | `k_max_files`, `k_storage_tag` |
| Member variables | trailing underscore | `callback_`, `active_` |
| Type aliases | PascalCase | `UniqueHandle`, `ResidentVector` |
| Macros | SCREAMING_CASE (avoid if a constant works) | config guards only |

## Modern syntax requirements

For new or unconstrained house projects, target the latest standard the toolset supports (`/std:c++latest`, C++23). Existing repositories retain their supported toolchain and language standard unless a migration is requested; use the modern spelling available within those constraints:

- **`concepts` over SFINAE.** `template <std::integral T>` or `requires` clauses; no `std::enable_if_t` towers in new code.
- **`<format>` over printf/ostringstream.** `std::format("pid={} n={}", pid, n)` gives compile-time-checked format strings. Prefer `std::print`/`std::println` for terminal output; their Unicode-aware native terminal handling requires UTF-8 ordinary literal encoding and a terminal destination. Redirected streams receive bytes, so define their encoding contract explicitly.
- **`std::span`/`std::string_view` over pointer+size pairs.** Views borrow — never own; state it in the contract comment.
- **`std::expected` (C++23) for fallible returns** in API surfaces that avoid exceptions; exceptions only at cold boundaries. `std::optional` for "may not have a value".
- **Structured bindings**: `for (auto&& [key, value] : map)`.
- **Designated initializers** for aggregate options: `Options{.path = p, .console = true}`.
- **CTAD and `auto` by default.** Local variables are `auto` wherever the initializer pins the type — constructors, casts, range-for, call results; spell the type out only when `auto` would hide a conversion, bind a proxy (`std::vector<bool>::front()`), or deduce something needlessly general. CTAD (`std::lock_guard lock{m}`) over written-out template arguments.
- **`if constexpr`** over tag-dispatch/`enable_if` for compile-time branching; `constexpr`/`consteval`/`constinit` wherever evaluation can move to compile time; `inline constexpr` at namespace scope (never `#define`).
- **`enum class` with explicit underlying type** (`std::uint8_t`, `std::uint32_t`); comment enumerators whose behavior is non-obvious.
- **`[[nodiscard]]`, `[[likely]]`/`[[unlikely]]`, `[[maybe_unused]]`** where meaningful; no raw `__attribute__`/`__declspec` when a standard attribute exists.
- **`auto&&` + perfect forwarding only when the callee truly forwards**; otherwise take concrete types, `std::span`, or `std::string_view`.
- **Range adapters/views** for pipelines (`std::views::filter | transform`) instead of hand-rolled index loops; a classic loop is fine when it is clearer.

## House idioms

- **Trailing return types** on all new functions: `auto f(int) noexcept -> bool`.
- **Character-type aliases** (`using char_t = wchar_t;`) in library headers so the type is swappable; never hardcode `wchar_t`/`char` ad hoc in library code.
- **Deleters as small structs with `static operator()`**: `struct HandleDeleter { static auto operator()(void* h) noexcept -> void { CloseHandle(h); } };` then `using UniqueHandle = std::unique_ptr<void, HandleDeleter>;` — one close path per resource type.
- **Scope guards** for non-resource cleanup: `auto exit = make_scope_exit([&]() noexcept { /* cleanup */ });`. Guards are non-copyable and non-movable; factory functions return by value (guaranteed copy elision).
- **`static_assert`** for constraints when a full `concept` is overkill.
- **Struct options pattern**: one `Options` struct with commented fields and sensible in-class initializers (`std::uint64_t max_bytes{8ull << 20};`) instead of long parameter lists.

## Documentation (contract comments)

- File header: one-paragraph purpose, architecture notes, quick-start snippet, and an explicit **Contracts** block listing failure policy, allocation guarantees, and threading constraints.
- Every public declaration gets a comment stating what it does and — when non-obvious — ownership, failure behavior, and preconditions. Example: "Runs `callback` on destruction unless release() disarmed the guard."
- Enumerator comments explain behavior differences, not paraphrase the name.

## Design playbook

- **Toolset-first dependencies are the unconstrained-project default.** New or unconstrained house projects check the standard library and Windows SDK first, never hand-roll what they provide, and use vcpkg manifest mode for third-party libraries only when a concrete misfit is stated (missing capability, weight, license). Existing repositories retain their established dependency policy unless a migration is requested.
- **Layer the public header pure.** Public header is C++/STL only — no Windows headers, no include-order contracts; all OS plumbing lives in exactly one library TU (or an internal contract header included only by library TUs), so consumers link one static lib.
- **Fail fast at init, never degrade.** `init()` fails instead of silently falling back; after init, no path allocates — overflow/full policies are explicit and counted.
- **Hot paths are EH-free by construction** (compile-time checked format strings, preallocated storage); cold lifecycle allocations convert failure into `false`/empty returns at the `noexcept` boundary. No try/catch to mask caller bugs.
- **Ordered single-consumer pipelines**: producers claim an ordered ticket and publish; one worker drains in order and batches I/O. Latency-sensitive I/O is async; completion is acknowledged only after it is confirmed.

## Performance, async, and zero-copy

- **Views are parameter types, never stored.** `std::span`/`std::string_view`/ranges views borrow: passing one into a call is safe, storing one past the full expression (`std::string_view s = get_name();`) is silent dangling. Bind rvalue containers to a named variable before taking a view (`borrowed_range` diagnoses the ranges case).
- **`std::pmr` arenas for build-then-free phases.** Allocation-dense parse/batch stages run `std::pmr` containers over a `monotonic_buffer_resource` that outlives every container using it. Swapping containers with unequal resources is UB when allocators do not propagate; move assignment instead performs element-wise moves and may allocate or throw. Cross-thread arenas use `synchronized_pool_resource`.
- **`std::move_only_function` for stored callbacks** holding move-only state or needing qualified invocation (`void() const noexcept`); `std::function` stays only where callers must copy. Neither guarantees allocation-free storage — hot paths still preallocate.
- **`return name;`, never `return std::move(name);`** for locals — the explicit move suppresses copy elision (NRVO); C++17 already guarantees prvalue elision and applies implicit move on return.
- **Hot-path failures return `std::expected<T, E>`** chained with `and_then`/`or_else`/`transform` — value and error inline, no allocation, no unwinding. Exceptions stay enabled for cold boundaries (MSVC STL assumes `/EHsc`); never turn exceptions off globally.
- **Optimizer hints**: exhaustive-switch `default:` holds `std::unreachable()`; compile-time branching is `if consteval` — never `if constexpr (std::is_constant_evaluated())`, which is always true at compile time. `[[assume]]` only with a measured before/after win on record.
- **Async is C++20 coroutines over IOCP today** — `co_await`-style tasks over a house IOCP awaitable; in new or unconstrained house projects, a third-party async runtime enters through vcpkg only when its portability or algorithms are actually needed. Existing repositories retain their dependency policy unless a migration is requested. `std::execution` is C++26 with no MSVC STL implementation, pilot projects only. Overlapped I/O: the `OVERLAPPED` and its buffer live until completion; release only on the completion path. High-IOPS file work may evaluate IoRing (Windows 11 22H2+, file I/O only) against IOCP with a benchmark — it is an option, not a default.
- **Container shape follows access pattern**: lookup/iteration-heavy small maps use `std::flat_map` (MSVC STL ships `<flat_map>`/`<flat_set>` in the VS 2026 18.6 toolset; on older toolsets keep a sorted `std::vector` of pairs). The standard library has no small_vector — many short vectors reserve up front, and only a measured win justifies a vcpkg dependency for one.

## Build and project layout

- Typical layout: `include/` + `src|lib/` (library + vcxproj), `tests/`, one `build.bat` that stages the deliverable matrix; solution at repo root. Keep build outputs (`obj/`, `out/`) out of version control.
- vcxproj: `WarningLevel=Level4`, `SDLCheck=true`, `LanguageStandard=stdcpplatest`; warnings-as-errors for library projects.
- Control-flow hardening on every new binary: `/guard:cf` compile plus `/GUARD:CF` link. `/CETCOMPAT` marks shadow-stack compatibility and applies to x86 and x64 only — it does nothing on ARM64; skip it for ROP-incompatible techniques such as detours-style hooking.
- Keep the source tree and build outputs on a Dev Drive (ReFS) with Defender performance mode — not antivirus folder exclusions — for build throughput.
- Runtime/toolset flavors (MD/MT) are switched per MSBuild pass with a property instead of duplicating solution configurations.
- **vcpkg manifest mode is the third-party dependency default for new or unconstrained house projects**: keep `vcpkg.json` above the project file with a `builtin-baseline`, run `vcpkg integrate install` once per machine, set `VcpkgEnableManifest=true` so restore runs with the build, and keep `vcpkg_installed/` out of version control. Multi-triplet solutions set `VcpkgManifestInstalledBaseDir`; shared and CI builds use binary caching. Existing repositories retain their established dependency policy unless a migration is requested.
- **MSBuild is the default for new or unconstrained Windows C++ projects.** Existing repositories retain their established build system unless a migration is requested. Where `.sln`/`.vcxproj` is used, invoke MSBuild rather than ad-hoc `cl.exe`/`nmake`:
  - Locate MSBuild through **vswhere**, never a hardcoded VS version path:
    ```bat
    set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
    "%VSWHERE%" -latest -products * -requires Microsoft.Component.MSBuild -find "MSBuild\**\Bin\MSBuild.exe"
    ```
    (`vswhere.exe`'s path contains `(x86)`, which breaks a `for /f` backquote — capture its output through a temp file inside batch scripts.)
  - `msbuild app.sln /t:Restore` first when NuGet packages are involved; build with `/p:Configuration=... /p:Platform=... /m /nologo /v:m`.
  - Check `if errorlevel 1` after every MSBuild invocation.
  - Exercise the full matrix when a change can affect it: Debug/Release × MD/MT × x64/Win32/ARM64.
