---
name: ms-win32
description: ALWAYS use this skill BEFORE writing or modifying ANY Windows/Win32, COM, or native interop code — any language calling Windows APIs (C/C++, Rust FFI, C#/P-Invoke, PowerShell). Enforces Unicode W-suffix APIs only, UTF-16/UTF-8 text discipline, documented failure-value checks (HRESULT, LSTATUS, GetLastError), and RAII ownership for handles, buffers, and COM allocations. MANDATORY even for trivial snippets.
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
