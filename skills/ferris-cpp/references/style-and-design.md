# C++ Style and Design

House standards for writing and reviewing C++. Read once per session before writing C++.

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

Target the latest standard the toolset supports (`/std:c++latest`, C++23); new code uses the modern spelling of every construct:

- **`concepts` over SFINAE.** `template <std::integral T>` or `requires` clauses; no `std::enable_if_t` towers in new code.
- **`<format>` over printf/ostringstream.** `std::format("pid={} n={}", pid, n)`; compile-time-checked format strings; `std::print` where available.
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

- **Prefer proven libraries over hand-rolled code.** Standard library first, then established libraries — Asio for async I/O and networking, `boost::container::small_vector` for short vectors, `boost::flat_map` where `std::flat_map` is not yet available. Write in-house code only when nothing fits, and state why in the contract comment; never hand-roll what the toolset already ships.
- **Layer the public header pure.** Public header is C++/STL only — no Windows headers, no include-order contracts; all OS plumbing lives in exactly one library TU (or an internal contract header included only by library TUs), so consumers link one static lib.
- **Fail fast at init, never degrade.** `init()` fails instead of silently falling back; after init, no path allocates — overflow/full policies are explicit and counted.
- **Hot paths are EH-free by construction** (compile-time checked format strings, preallocated storage); cold lifecycle allocations convert failure into `false`/empty returns at the `noexcept` boundary. No try/catch to mask caller bugs.
- **Ordered single-consumer pipelines**: producers claim an ordered ticket and publish; one worker drains in order and batches I/O. Latency-sensitive I/O is async; completion is acknowledged only after it is confirmed.

## Performance, async, and zero-copy

- **Views are parameter types, never stored.** `std::span`/`std::string_view`/ranges views borrow: passing one into a call is safe, storing one past the full expression (`std::string_view s = get_name();`) is silent dangling. Bind rvalue containers to a named variable before taking a view (`borrowed_range` diagnoses the ranges case).
- **`std::pmr` arenas for build-then-free phases.** Allocation-dense parse/batch stages run `std::pmr` containers over a `monotonic_buffer_resource` that outlives every container using it; never swap or move-assign pmr containers wired to different resources (UB — the allocator does not propagate). Cross-thread arenas use `synchronized_pool_resource`.
- **`std::move_only_function` for stored callbacks** holding move-only state or needing qualified invocation (`void() const noexcept`); `std::function` stays only where callers must copy. Neither guarantees allocation-free storage — hot paths still preallocate.
- **`return name;`, never `return std::move(name);`** for locals — the explicit move suppresses copy elision (NRVO); C++17 already guarantees prvalue elision and applies implicit move on return.
- **Hot-path failures return `std::expected<T, E>`** chained with `and_then`/`or_else`/`transform` — value and error inline, no allocation, no unwinding. Exceptions stay enabled for cold boundaries (MSVC STL assumes `/EHsc`); never turn exceptions off globally.
- **Optimizer hints**: exhaustive-switch `default:` holds `std::unreachable()`; compile-time branching is `if consteval` — never `if constexpr (std::is_constant_evaluated())`, which is always true at compile time. `[[assume]]` only with a measured win on record (needs VS 2026 toolset).
- **Async is C++20 coroutines over IOCP today** — `co_await`-style tasks (Asio `use_awaitable` or a house IOCP awaitable); `std::execution` is C++26 with no shipping STL implementation, pilot projects only. Overlapped I/O: the `OVERLAPPED` and its buffer live until completion; release only on the completion path. High-IOPS file work may evaluate IoRing (Windows 11 22H2+, file I/O only) against IOCP with a benchmark — it is an option, not a default.
- **Container shape follows access pattern**: lookup/iteration-heavy small maps use `std::flat_map` (needs the VS 2026 toolset; until then a sorted vector of pairs), many short vectors use `boost::container::small_vector` — the standard library has no small_vector.

## Build and project layout

- Typical layout: `include/` + `src|lib/` (library + vcxproj), `tests/`, one `build.bat` that stages the deliverable matrix; solution at repo root. Keep build outputs (`obj/`, `out/`) out of version control.
- vcxproj: `WarningLevel=Level4`, `SDLCheck=true`, `LanguageStandard=stdcpplatest`; warnings-as-errors for library projects.
- New x64/ARM64 binaries link with `/CETCOMPAT` (plus `/guard:cf` compile, `/GUARD:CF` link) — skip only for ROP-incompatible techniques such as detours-style hooking.
- Keep the source tree and build outputs on a Dev Drive (ReFS) with Defender performance mode — not antivirus folder exclusions — for build throughput.
- Runtime/toolset flavors (MD/MT) are switched per MSBuild pass with a property instead of duplicating solution configurations.
- **MSBuild is the build system** for anything with `.sln`/`.vcxproj` — never ad-hoc `cl.exe`/`nmake`:
  - Locate MSBuild through **vswhere**, never a hardcoded VS version path:
    ```bat
    set "VSWHERE=%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe"
    "%VSWHERE%" -latest -products * -requires Microsoft.Component.MSBuild -find "MSBuild\**\Bin\MSBuild.exe"
    ```
    (`vswhere.exe`'s path contains `(x86)`, which breaks a `for /f` backquote — capture its output through a temp file inside batch scripts.)
  - `msbuild app.sln /t:Restore` first when NuGet packages are involved; build with `/p:Configuration=... /p:Platform=... /m /nologo /v:m`.
  - Check `if errorlevel 1` after every MSBuild invocation.
  - Exercise the full matrix when a change can affect it: Debug/Release × MD/MT × x64/Win32/ARM64.
