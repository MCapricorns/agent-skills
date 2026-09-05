# C++ Contracts and Build Traps

## House defaults

For unconstrained code: PascalCase types/aliases, snake_case functions, lowercase namespaces, trailing-underscore members, `k_` snake_case constants, and trailing returns. Prefer typed constants to macros. Keep public headers self-contained and Windows implementation details out of portable APIs; avoid aliases implying interchangeable encodings.

## Ownership and failure

- Adopt owned resources immediately into the canonical RAII wrapper. Match the invalid sentinel and release operation; borrowed/pseudo-handles are not owners. A `unique_ptr<void>` deleter is not a universal handle wrapper. Reuse the existing scope guard for exactly-once cleanup.
- Stored/returned views require an owner that survives every use and no invalidating mutation. Name temporary owners before borrowing; recheck captures and buffers across async boundaries. Return locals without `std::move` to retain NRVO.
- `std::expected` is not an allocation-free or non-throwing guarantee. Keep `noexcept` truthful, handle callees' exceptions at non-throwing boundaries without hiding programming errors, and report fallible initialization. Preserve allocation/overflow policy; mark must-consider results `[[nodiscard]]`.
- `std::unreachable()` and `[[assume]]` cause undefined behavior when wrong. Require a proven invariant and measured benefit. For evaluation-mode branching use `if consteval` when supported, not `if constexpr (std::is_constant_evaluated())`.

## Allocation and async

- `std::pmr` resources must outlive their containers. Unequal-resource swaps can be undefined with non-propagating allocators.
- Neither `std::function` nor `std::move_only_function` guarantees allocation-free storage. Select the wrapper by copyability and invocation contract.
- Coroutines supply neither a scheduler nor cancellation semantics; use the existing runtime. For Windows overlapped I/O, keep `OVERLAPPED` and buffers alive until completion is observed; a cancellation request is not completion.
- `std::print`/`std::println` Unicode behavior depends on literal encoding and destination. See ferris-windows for console/pipe boundaries.

## Windows builds

For new unconstrained Windows projects, use MSBuild and prefer the standard library/Windows SDK, then vcpkg manifest mode for a concrete capability, weight, and license fit. Existing build/dependency policies win.

- Locate MSBuild rather than hardcoding a Visual Studio version:

  ```powershell
  $vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio/Installer/vswhere.exe'
  & $vswhere -latest -products '*' -requires Microsoft.Component.MSBuild -find 'MSBuild\**\Bin\MSBuild.exe'
  ```

  Invoke the returned path, restore NuGet when applicable, and build the affected configuration/platform. Shell quoting and exit handling belong to ferris-windows.
- Preserve manifest restore, triplet, installed-directory, and binary-cache settings; keep outputs and `vcpkg_installed/` out of Git. No unsolicited machine-wide integration changes.
- Preserve `/W4`, `/sdl`, library warnings-as-errors, selected standard, and UTF-8 source/execution encoding. New binaries use `/guard:cf` at compile time and `/GUARD:CF` at link time; `/CETCOMPAT` requires compatible x86/x64 binaries, not ARM64 or incompatible hooking. Never drop existing hardening for convenience.

Feature adoption: [MSVC standard modes](https://learn.microsoft.com/en-us/cpp/build/reference/std-specify-language-standard-version). `/std:c++latest` includes experimental features; verify compiler **and** STL support instead of equating the switch or publication year with availability.
