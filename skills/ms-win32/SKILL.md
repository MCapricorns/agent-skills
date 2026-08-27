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
