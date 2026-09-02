---
name: ferris-windows
description: Windows platform rules and system-call correctness, in any language. Use when writing, modifying, or reviewing anything that runs on Windows, even with no system call in sight — MAX_PATH and \\?\ long paths, case-insensitive filenames, files locked by running processes (sharing violations, LNK1168), DLL search order, console code pages and UTF-8, symlinks, UAC elevation — and when calling into Windows via windows.h, the Rust windows/windows-sys crates, raw extern FFI, C# P/Invoke, or PowerShell. Also triggers on HANDLE, HWND, HRESULT, GetLastError, CreateFileW, UTF-16, W- or A-suffixed functions, DLL boundary design. C++ and Rust naming or style belong to ferris-cpp and ferris-rust.
---

# Windows Development Discipline

Invoke for ANY code that runs on Windows. The platform rules apply with no system call in sight; the system-call rules apply the moment code touches Windows. Rationale, edge cases, and Rust/FFI detail: [references/rules.md](./references/rules.md).

## Platform rules (no system call required)

1. **Deep absolute paths get the `\\?\` prefix** — the 260-char `MAX_PATH` ceiling applies unless long paths are enabled.
2. **Names are case-insensitive but case-preserving** — `Foo.rs` and `foo.rs` collide; case-only renames take a two-step move. Reserved device names (`CON`, `PRN`, `AUX`, `NUL`, `COM1`–`COM9`, `LPT1`–`LPT9`) are never valid filenames.
3. **An open file is a locked file** — sharing violations and linker `LNK1168` mean stop or close the holder first; a retry loop that never closes the holder is not a fix.
4. **Load non-system DLLs by explicit absolute path**, never by bare name — the search order will load the wrong one.
5. **Console text is not UTF-8 by default** — the OEM code page (936 on Chinese-locale systems) renders UTF-8 bytes as mojibake: set `SetConsoleOutputCP(CP_UTF8)` at startup (or `chcp 65001` interactively) and state the encoding at every process and pipe boundary — a redirected pipe carries raw bytes with no code page. Full encoding decision table: references/rules.md.
6. **New CLI output uses virtual terminal sequences** — enable `ENABLE_VIRTUAL_TERMINAL_PROCESSING` once at startup; classic Console API stays only for the bootstrap calls (`GetStdHandle`/`SetConsoleMode`). Keyboard input reads `ReadConsoleW` — cooked-mode UTF-8 input is still incomplete.
7. **Symlinks need Developer Mode or admin; junctions (`mklink /J`) don't** — prefer junctions unprivileged; a failed symlink creation degrades gracefully (copy, junction), never crashes.
8. **Run unelevated by default** — elevation only for documented admin operations.

## System-call rules

1. **Unicode `W` entry points only, never `A`**; never `CP_ACP` or ANSI encodings for durable or protocol text.
2. **Bytes are not UTF-16 code units** — honor exact length contracts and terminators; never assume null termination when a length is supplied.
3. **Check documented failure values** — `FAILED`/`SUCCEEDED` for `HRESULT`, `ERROR_SUCCESS` for `LSTATUS`; capture `GetLastError()` only where documented (many calls invalidate it).
4. **RAII ownership with matching release** for handles, buffers, and COM allocations; never release borrowed or pseudo-handles. Initialize size/version fields (`cbSize`); use pointer-sized types (`DWORD_PTR`, `INT_PTR`) without truncation.

When a rule here conflicts with a documented contract, the documented contract wins — note the deviation. Language-specific wrapper discipline (Rust `windows`-crate usage, C# P/Invoke shapes) lives in the language skills; the platform rules here apply to every language.
