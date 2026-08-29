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
- **CTAD** (`std::lock_guard lock{m}`) and `auto` where the type is obvious from the initializer; no `auto` that hides a non-obvious conversion.
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

- **Layer the public header pure.** Public header is C++/STL only — no Windows headers, no include-order contracts; all OS plumbing lives in exactly one library TU (or an internal contract header included only by library TUs), so consumers link one static lib.
- **Fail fast at init, never degrade.** `init()` fails instead of silently falling back; after init, no path allocates — overflow/full policies are explicit and counted.
- **Hot paths are EH-free by construction** (compile-time checked format strings, preallocated storage); cold lifecycle allocations convert failure into `false`/empty returns at the `noexcept` boundary. No try/catch to mask caller bugs.
- **Ordered single-consumer pipelines**: producers claim an ordered ticket and publish; one worker drains in order and batches I/O. Latency-sensitive I/O is async; completion is acknowledged only after it is confirmed.

## Build and project layout

- Typical layout: `include/` + `src|lib/` (library + vcxproj), `tests/`, one `build.bat` that stages the deliverable matrix; solution at repo root. Keep build outputs (`obj/`, `out/`) out of version control.
- vcxproj: `WarningLevel=Level4`, `SDLCheck=true`, `LanguageStandard=stdcpplatest`; warnings-as-errors for library projects.
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
