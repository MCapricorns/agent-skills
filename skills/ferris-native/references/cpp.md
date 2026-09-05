# C++ Design and Build Details

Read only the sections relevant to the change. Use repository conventions where they differ from house style.

## House defaults

- PascalCase types/aliases, snake_case functions, lowercase namespaces, trailing-underscore members, `k_` snake_case constants, and trailing return types. Use uppercase macros only when a typed constant cannot do the job.
- Select a supported language standard deliberately. `/std:c++latest` includes experimental features, not just C++23; confirm compiler/STL availability rather than relying on a release prediction.
- Use RAII for owned memory and OS resources; no owning raw `new`/`delete` or unwrapped handles. Use truthful `noexcept`, `[[nodiscard]]` for results callers must consider, and `constexpr` where useful.

## API and syntax

- Prefer concepts over SFINAE towers, `std::span` over pointer+size, scoped enums, and standard attributes. Use CTAD and `auto` when they preserve intent; spell out types when deduction hides a conversion or binds a proxy.
- Use `std::optional` for absence and `std::expected` for actionable failures when available under the selected standard. The value/error types can allocate or throw; `expected` itself does not make a path allocation-free or `noexcept`.
- Prefer standard formatting over printf-style varargs. `std::print`/`std::println` terminal Unicode handling depends on literal encoding and destination; redirected output still needs an explicit byte encoding.
- Keep public headers self-contained and avoid leaking Windows headers or include-order requirements into portable APIs. Put platform implementation in internal headers/translation units; do not force a whole subsystem into one file.
- Use an options struct when it clarifies a genuinely complex call, not for every parameter list. Avoid character-type aliases that suggest unsupported encoding interchangeability.
- Public comments describe behavior and non-obvious preconditions, ownership, errors, and threading. Explain enumerator differences and magic values; do not duplicate a full architecture/quick-start template in every source file.

## Ownership and failure

- Reuse the canonical resource wrapper and scope guard. Adopt raw resources immediately; preserve borrowed/pseudo-handle distinctions and the API's actual invalid sentinel. A generic `unique_ptr<void>` deleter is not a universal Windows handle wrapper.
- A guard must execute cleanup exactly once. Do not add another scope-exit abstraction when the project already supplies one.
- Views can be stored or returned when the owner outlives every use and mutation cannot invalidate them. Name temporary owners before borrowing. Recheck captures and buffers across asynchronous boundaries.
- Return a local as `return value;`, not `return std::move(value);`, to permit NRVO and implicit move.
- Fallible initialization reports failure rather than silently degrading. Preserve promised allocation/overflow policies and explicit overflow accounting. A `noexcept` boundary must handle any exception its callees can produce without hiding programming errors.
- `std::unreachable()` and `[[assume]]` introduce undefined behavior when wrong; they are not validation or a generic default branch. Require a proven invariant; optimizer hints also need a measured benefit. Use `if consteval` for evaluation-mode branching when supported, not `if constexpr (std::is_constant_evaluated())`.

## Performance and asynchronous I/O

- Profile the actual workload before adding specialized storage or scheduling. Preserve established latency/allocation guarantees; prefer batching and buffer reuse to speculative micro-optimization.
- A `std::pmr` resource must outlive every container using it. Monotonic resources suit build-then-free lifetimes. Unequal-resource swaps can be undefined when allocators do not propagate; move assignment may allocate or throw. Thread-shared allocation needs a resource with the required synchronization.
- Choose callback wrappers by copyability and invocation contract. `std::move_only_function` and `std::function` do not guarantee allocation-free storage.
- Use the existing async runtime. Native Windows overlapped I/O can use IOCP with coroutine adapters, but coroutines alone supply no scheduler or cancellation policy. Keep `OVERLAPPED` and buffers alive until completion is observed, including after cancellation; preserve ordering and acknowledge completion only after confirmation.
- Check compiler/library feature support before adopting sender/receiver facilities, flat containers, or newer call wrappers. Do not encode a release-number prediction in reusable guidance.

## Dependencies and builds

For new Windows house projects, prefer the standard library and Windows SDK, then vcpkg manifest mode for a concrete capability/weight/license fit; MSBuild is the default. Existing projects retain their build system, dependency/versioning policy, and supported configuration matrix.

- Keep outputs and `vcpkg_installed/` out of Git. Preserve the repository's manifest restore, triplet, installed-directory, and binary-cache settings; avoid unrequested machine-wide integration changes.
- For `.sln`/`.vcxproj`, locate MSBuild via vswhere rather than a hardcoded Visual Studio version path:

  ```bat
  "%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -requires Microsoft.Component.MSBuild -find "MSBuild\**\Bin\MSBuild.exe"
  ```

  Invoke the returned path. Quote batch paths carefully; use a temporary output file if command substitution becomes fragile. Restore NuGet when applicable, then build the affected configuration/platform. Check `if errorlevel 1` after native build commands; PowerShell exit handling belongs to ferris-windows.
- Preserve `/W4`, `/sdl`, library warnings-as-errors, the selected language standard, and UTF-8 source/execution encoding. For new binaries, use `/guard:cf` at compile time and `/GUARD:CF` at link time; `/CETCOMPAT` is for compatible x86/x64 binaries, not ARM64 or incompatible hooking techniques. Do not remove existing hardening for convenience.
- Exercise the supported Debug/Release, MD/MT, and architecture combinations the change can affect; do not invent unsupported matrix entries. Switch runtime flavors through build properties rather than duplicated projects.
- If build I/O is the measured bottleneck, consider Dev Drive with Defender performance mode, not antivirus exclusions.

Feature availability: [MSVC standard modes](https://learn.microsoft.com/en-us/cpp/build/reference/std-specify-language-standard-version). Consult the installed toolset and current vendor documentation when adopting a feature, not on every ordinary edit.
