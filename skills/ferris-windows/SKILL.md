---
name: ferris-windows
description: Windows platform, shell, and system-interface discipline for code and builds targeting Windows. Use for Windows-targeted code even with no system call in sight; PowerShell or batch scripts; path, filesystem, console, DLL, or elevation behavior; Win32, COM, P/Invoke, or FFI integration; and Windows-specific build failures. C++ and Rust language design and style belong to ferris-cpp and ferris-rust.
---

# Windows Development Discipline

The platform rules apply with no system call in sight; the shell rules apply to scripts that drive a build or a tool; the system-call rules apply the moment code touches Windows. Rationale, edge cases, and Rust/FFI detail: [references/rules.md](./references/rules.md).

## Platform rules (no system call required)

1. **Deep absolute paths get the `\\?\` prefix** — the 260-char `MAX_PATH` ceiling applies unless long paths are enabled.
2. **Names are case-insensitive but case-preserving** — `Foo.rs` and `foo.rs` collide; case-only renames take a two-step move. Reserved device names (`CON`, `PRN`, `AUX`, `NUL`, `COM1`–`COM9`, `LPT1`–`LPT9`) are never valid filenames.
3. **Open handles control delete and replace sharing** — the operation succeeds only when existing handles' share modes permit it, notably `FILE_SHARE_DELETE`; a sharing violation means a holder denies the requested operation. Closing that holder is one remedy; blind retry is not a fix.
4. **Load non-system DLLs by explicit absolute path**, never by bare name — the search order will load the wrong one.
5. **Console text is not UTF-8 by default** — the OEM code page (936 on Chinese-locale systems) renders UTF-8 bytes as mojibake: set `SetConsoleOutputCP(CP_UTF8)` at startup (or `chcp 65001` interactively) and state the encoding at every process and pipe boundary — a redirected pipe carries raw bytes with no code page. Full encoding decision table: references/rules.md.
6. **New CLI output uses virtual terminal sequences** — enable `ENABLE_VIRTUAL_TERMINAL_PROCESSING` once at startup; classic Console API stays only for the bootstrap calls (`GetStdHandle`/`SetConsoleMode`). Keyboard input reads `ReadConsoleW` — cooked-mode UTF-8 input is still incomplete.
7. **Treat symlink creation as fallible** — Developer Mode or privilege may be required; junctions are directory-only and copies lose link/update semantics. Use only an explicitly accepted behavior-preserving fallback, or fail clearly.
8. **Run unelevated by default** — elevation only for documented admin operations.

## System-call rules

1. **Unicode `W` entry points only, never `A`**; never `CP_ACP` or ANSI encodings for durable or protocol text.
2. **Bytes are not UTF-16 code units** — honor exact length contracts and terminators; never assume null termination when a length is supplied.
3. **Check documented failure values** — `FAILED`/`SUCCEEDED` for `HRESULT`, `ERROR_SUCCESS` for `LSTATUS`; capture `GetLastError()` only where documented (many calls invalidate it).
4. **RAII ownership with matching release** for handles, buffers, and COM allocations; never release borrowed or pseudo-handles. Initialize size/version fields (`cbSize`); use pointer-sized types (`DWORD_PTR`, `INT_PTR`) without truncation.

## Shell and scripting rules

1. **Native exit codes live in `$LASTEXITCODE`** — `$?` is a Boolean derived from native exit status; in PowerShell 7.4+, `$ErrorActionPreference` can act on native nonzero exits when `$PSNativeCommandUseErrorActionPreference` is enabled. For cross-version scripts, check numeric `$LASTEXITCODE` after each native tool and stop on failure.
2. **`&&` and `||` require PowerShell 7+** — Windows PowerShell 5.1 chains with `;` plus an explicit code check, and no POSIX shell assumptions (globbing, quoting, `2>&1` semantics) carry over.
3. **Declare the encoding before emitting non-ASCII** — `[Console]::OutputEncoding` decides how a native tool's output is decoded, `$OutputEncoding` what PowerShell pipes into one; `Out-File`/`Set-Content` defaults differ between 5.1 and 7, so pass `-Encoding utf8` explicitly.

When a rule here conflicts with a documented contract, the documented contract wins — say so in the code comment and in the reply. Rust `windows`-crate wrapper discipline lives in ferris-rust; for languages with no house skill (C#, PowerShell), these rules plus the documented signature are the whole contract.
