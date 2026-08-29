# C++ Style and Design

Conventions distilled from the fluxlog codebase (lib/demo/tests layout, MSBuild matrix). Read once per session before writing C++.

## Naming

| Element | Convention | Example |
|---------|-----------|---------|
| Types, classes, enums | PascalCase | `ScopeExit`, `FullPolicy` |
| Functions, methods | snake_case | `source_basename`, `log_at` |
| Namespaces | lowercase single word | `fluxlog`, `fluxlog::detail` |
| Compile-time constants | `k_` prefix + snake_case | `k_obj`, `k_storage_tag` |
| Member variables | trailing underscore | `callback_`, `active_` |
| Type aliases | PascalCase | `UniqueHandle`, `ResidentVector` |
| Macros | SCREAMING_CASE (avoid if a constant works) | `_KERNEL_MODE` guards only |

## Syntax rules

- **Trailing return types** on all new functions: `auto f(int) noexcept -> bool`.
- **`using char_t = wchar_t;`-style aliases** in public headers so the character type is swappable; never hardcode `wchar_t`/`char` ad hoc in library code.
- **`inline constexpr`** for named constants at namespace scope, not `#define` or `static const`.
- **Deleters as small structs with `static operator()`**: `struct ZwHandleDeleter { static auto operator()(void* h) noexcept -> void { ZwClose(h); } };` then `using UniqueHandle = std::unique_ptr<void, ZwHandleDeleter>;` — one close path per resource type.
- **Scope guards** for non-resource cleanup: `auto exit = make_scope_exit([&]() noexcept { /* cleanup */ });`. Guards are non-copyable and non-movable; factory functions return by value (guaranteed copy elision).
- **`static_assert`** for template constraints when `requires`/concepts are overkill.
- **Designated intent with enums**: `enum class` with explicit underlying type (`std::uint32_t`, `std::uint8_t`); comment every enumerator that has non-obvious behavior.
- **Struct options pattern**: one `Options` struct with commented fields and sensible in-class initializers (`std::uint64_t max_bytes{8ull << 20};`) instead of long parameter lists.

## Documentation (contract comments)

- File header: one-paragraph purpose, architecture notes, quick-start snippet, and an explicit **Contracts** block listing failure policy, allocation guarantees, and threading/IRQL constraints.
- Every public declaration gets a comment stating what it does and — when non-obvious — ownership, failure behavior, and preconditions. Example: "Runs `callback` on destruction unless release() disarmed the guard."
- Enumerator comments explain behavior differences, not paraphrase the name.

## Design playbook

- **Layer the public header pure.** Public header is C++/STL only — no Windows headers, no include-order contracts; all OS plumbing lives in exactly one library TU (or an internal contract header included only by library TUs). The static library propagates linker comments so consumers link one lib.
- **Fail fast at init, never degrade.** `init()` fails instead of silently falling back; after init, no path allocates — overflow policies are explicit (`Block` parks, `DropNewest` truncates and counts).
- **Hot paths are EH-free by construction** (compile-time checked format strings, preallocated storage); cold lifecycle allocations convert failure into `false`/empty returns at the `noexcept` boundary. No try/catch to mask caller bugs.
- **Single worker, ordered tickets**: producers claim an ordered ticket and publish; one worker drains in order and batches I/O. Latency-sensitive I/O is async; flush acknowledges only after completion is confirmed.
- **Same-source UM/KM sharing** where applicable: `#if defined(_KERNEL_MODE)` islands inside `detail`, with KM selecting non-paged, tag-allocating STL adapters.

## Build and project layout

- Layout: `lib/` (library + vcxproj), `demo/` (usage demo + bench), `tests/`, `build.bat` (deliverable matrix staging), solution at root.
- vcxproj: `WarningLevel=Level4`, `SDLCheck=true`, `LanguageStandard=stdcpplatest`. Prefer warnings-as-errors for library projects.
- Runtime/toolset flavors are switched per MSBuild pass with a property (`/p:FluxRuntime=MD|MT`) instead of duplicating configurations.
- Build through `build.bat` invoking MSBuild via vswhere (see ms-win32 skill "Building with MSBuild"); always exercise the full Debug/Release × MD/MT × platform matrix when a change can affect it.
