---
name: ms-win32
description: Correct-usage rules for Windows APIs called from any language. Use when writing, modifying, or reviewing code that calls Win32, COM, or NT APIs — C/C++ including windows.h, Rust using the windows or windows-sys crates or raw extern system FFI, C# P/Invoke or DllImport, PowerShell or scripts touching the registry, services, or shell — even for a one-line snippet. Also triggers on HANDLE, HWND, HRESULT, GetLastError, CreateFileW, RegOpenKeyExW, CoInitializeEx, WinMain, message loops, wide strings and UTF-16, any W- or A-suffixed API, and DLL boundary design. Owns cross-language FFI, text-encoding, failure-value, and handle-ownership rules. C++ and Rust naming or style belong to ms-cpp and ms-rust; LF/CRLF churn belongs to git-line-endings.
---

# Win32 Discipline

Invoke for ANY code touching Windows APIs: `*W`/`*A` functions from kernel32/user32/advapi32/ole32/shell32 and friends, COM interfaces, handles (`HANDLE`, `HWND`, `HDC`), registry, services, or shell — in any language, however trivial the snippet.

## Non-negotiables

1. **Unicode `W` APIs only, never `A`.** Text is UTF-16 or UTF-8 only; never `CP_ACP` or any ANSI/narrow encoding for durable or protocol text.
2. **Bytes are not UTF-16 code units.** Honor exact length contracts and terminators; never assume null termination when a length is supplied.
3. **Check documented failure values.** `FAILED`/`SUCCEEDED` for `HRESULT`; `ERROR_SUCCESS` for `LSTATUS`; capture `GetLastError()` only where documented — many calls invalidate it.
4. **RAII ownership with matching release** for handles, buffers, and COM allocations; never release borrowed or pseudo-handles. Initialize structure size/version fields (`cbSize` etc.) as documented; use pointer-sized types (`DWORD_PTR`, `INT_PTR`) without truncation.

When a rule here conflicts with an API's documented contract, the documented contract wins — note the deviation.

## Cross-language general (Rust FFI and friends)

These rules apply to ANY language calling Windows APIs; each language skill defers here instead of restating them.

- **Declare Win32 imports through the official `windows`/`windows-sys` crates** rather than hand-written `extern "system"` blocks when a declaration exists there; only write raw FFI for APIs the crates don't cover.
- **`W` functions only from Rust too** — the `windows` crate exposes `*W` entry points; never reach for ANSI aliases.
- **`PCWSTR`/`PWSTR` discipline**: a `&str` becomes UTF-16 via `HSTRING::from` or `to_vec_with_nul`; never `as_ptr()` a non-nul-terminated buffer, and keep the owning allocation alive for the call.
- **Failure values are not optional in Rust either**: check `windows::core::Result` / `HRESULT` with `?` or explicit `ok_or`; a `BOOL` that is `FALSE` means call `GetLastError()` immediately, before any other call.
- **Handle RAII in Rust**: wrap owned `HANDLE`s in a newtype with `Drop` calling `CloseHandle`; never `mem::forget` or hand a raw handle to multiple owners. Borrowed/pseudo-handles (`GetCurrentProcess`) are never dropped.
- **DLL boundary portability**: only "portable" data crosses a DLL boundary — `#[repr(C)]`, no interaction with statics or `TypeId`, no non-portable values inside. Rust-owned `String`/`Vec`/`Box` and any `#[repr(Rust)]` type must not be transferred between separately compiled DLLs; each DLL has its own statics, layouts, and type IDs.
