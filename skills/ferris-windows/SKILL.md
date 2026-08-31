---
name: ferris-windows
description: Windows development discipline — platform rules and system-call correctness, in any language. Use when writing, modifying, or reviewing anything that runs on Windows — even with no system call in sight — for MAX_PATH and \\?\ long paths, case-insensitive filenames and reserved device names, files locked by a running process (sharing violations, linker LNK1168), DLL search order, console code pages and UTF-8 output, symlinks needing Developer Mode, or UAC elevation; and when calling into Windows — windows.h, the Rust windows or windows-sys crates, raw extern system FFI, C# P/Invoke, or PowerShell touching registry, services, or shell. Also triggers on HANDLE, HWND, HRESULT, GetLastError, CreateFileW, UTF-16, W- or A-suffixed functions, DLL boundary design. C++ and Rust naming or style belong to ferris-cpp and ferris-rust.
---

# Windows Development Discipline

Invoke for ANY code that runs on Windows. The platform rules apply with no system call in sight; the system-call rules apply the moment code touches Windows.

## Platform rules (no system call required)

1. **Paths hit the 260-char `MAX_PATH` ceiling** unless long paths are enabled or the path is `\\?\`-prefixed — prefix absolute paths in deep trees. The filesystem is case-insensitive but case-preserving: `Foo.rs` and `foo.rs` collide, and case-only renames need a two-step move. Reserved device names (`CON`, `PRN`, `AUX`, `NUL`, `COM1`–`COM9`, `LPT1`–`LPT9`) are never valid filenames.
2. **An open file is a locked file.** Windows denies deleting or replacing any file a process holds open — a running exe, a loaded DLL, an open log. Sharing violations and linker `LNK1168` mean stop or close the holder first; a retry loop that never closes the holder is not a fix.
3. **DLLs load by search order, not by magic.** Application dir, system dirs, then PATH (and the working directory in legacy modes) — load non-system DLLs by explicit absolute path, never by bare name, or you will load the wrong one.
4. **Console text is not UTF-8 by default.** The console code page is OEM (437/936/…), so pick the encoding deliberately — `chcp 65001` or `SetConsoleOutputCP(CP_UTF8)` for UTF-8, or UTF-16 APIs — and state the encoding at every process and pipe boundary.
5. **Symlinks need Developer Mode or admin.** Directory junctions (`mklink /J`) work unprivileged; prefer them when elevation is not available.
6. **Run unelevated by default.** Request elevation only for documented admin operations (HKLM writes, services, protected files); "run everything as administrator" is not a design.

## System-call rules

1. **Unicode `W` entry points only, never `A`.** Text is UTF-16 or UTF-8 only; never `CP_ACP` or any ANSI/narrow encoding for durable or protocol text.
2. **Bytes are not UTF-16 code units.** Honor exact length contracts and terminators; never assume null termination when a length is supplied.
3. **Check documented failure values.** `FAILED`/`SUCCEEDED` for `HRESULT`; `ERROR_SUCCESS` for `LSTATUS`; capture `GetLastError()` only where documented — many calls invalidate it.
4. **RAII ownership with matching release** for handles, buffers, and COM allocations; never release borrowed or pseudo-handles. Initialize structure size/version fields (`cbSize` etc.) as documented; use pointer-sized types (`DWORD_PTR`, `INT_PTR`) without truncation.

When a rule here conflicts with a documented contract, the documented contract wins — note the deviation.

## Cross-language FFI (Rust and friends)

These rules apply to ANY language calling into Windows; each language skill defers here instead of restating them.

- **Declare Windows imports through the official `windows`/`windows-sys` crates** rather than hand-written `extern "system"` blocks when a declaration exists there; only write raw FFI for what the crates don't cover.
- **`W` functions only from Rust too** — the `windows` crate exposes `*W` entry points; never reach for ANSI aliases.
- **`PCWSTR`/`PWSTR` discipline**: a `&str` becomes UTF-16 via `HSTRING::from` or `to_vec_with_nul`; never `as_ptr()` a non-nul-terminated buffer, and keep the owning allocation alive for the call.
- **Failure values are not optional in Rust either**: check `windows::core::Result` / `HRESULT` with `?` or explicit `ok_or`; a `BOOL` that is `FALSE` means call `GetLastError()` immediately, before any other call.
- **Handle RAII in Rust**: wrap owned `HANDLE`s in a newtype with `Drop` calling `CloseHandle`; never `mem::forget` or hand a raw handle to multiple owners. Borrowed/pseudo-handles (`GetCurrentProcess`) are never dropped.
- **DLL boundary portability**: only "portable" data crosses a DLL boundary — `#[repr(C)]`, no interaction with statics or `TypeId`, no non-portable values inside. Rust-owned `String`/`Vec`/`Box` and any `#[repr(Rust)]` type must not be transferred between separately compiled DLLs; each DLL has its own statics, layouts, and type IDs.
