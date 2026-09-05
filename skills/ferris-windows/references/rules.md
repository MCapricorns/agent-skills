# Windows Platform Details

Read only the sections the change needs. Confirm behavior against the actual API/runtime and supported Windows versions.

## Paths, names, and loading

- Many Win32 file APIs remove `MAX_PATH` limits when both system policy and the application manifest opt in; this does not cover every API, shell, or third-party tool. Where supported, extended paths use `\\?\C:\...` or `\\?\UNC\server\share\...`, not a blindly prefixed UNC path. They must be absolute and use backslashes without `.`/`..`; the prefix disables normal path normalization.
- Windows normally preserves case but compares names case-insensitively; NTFS directories can opt into case sensitivity. Keep portable source trees free of case-only collisions. Use a two-step Git move for case-only renames, not a delete/recreate sequence that risks data loss.
- Avoid reserved device names (`CON`, `PRN`, `AUX`, `NUL`, `COM1`–`COM9`, `LPT1`–`LPT9`, including extensions), trailing spaces/dots, and invalid filename characters. Do not lowercase paths as a universal identity check.
- Deletion/replacement of open files depends on share modes and the specific operation. Identify the process/handle denying sharing, including stale processes causing linker LNK1168; do not hide a persistent holder with blind retries.
- Use trusted absolute paths for non-system DLLs and documented `LoadLibraryExW` `LOAD_LIBRARY_SEARCH_*` flags for their dependencies, choosing only required trusted directories. The top-level DLL's path does not control all transitive loads. Avoid current-directory/PATH searching and process-wide search-path mutation around individual calls.
- Symlinks may require Developer Mode or privilege. Junctions only cover directories; copies lose link/update semantics. Request elevation only for the specific documented administrative operation.

## Encoding and terminal I/O

There are separate contracts for source literals, internal strings, and external bytes. Do not infer them from the user's locale.

| Boundary | Rule |
|----------|------|
| MSVC source and narrow literals | `/utf-8` sets source and execution encoding; a UTF-8 BOM only identifies source encoding |
| Native console output | Prefer the runtime's Unicode terminal support or `WriteConsoleW`; when emitting UTF-8 bytes to the console, set `SetConsoleOutputCP(CP_UTF8)` |
| Native console input | `ReadConsoleW` handles Unicode console input; redirected stdin is a byte stream requiring explicit decoding |
| Files and pipes | State the encoding on both ends; code-page changes do not transcode redirected bytes |
| Win32 conversion | Use an explicit code page such as `CP_UTF8`, honor error/length contracts, and do not use `CP_ACP` for durable/protocol text |
| Legacy narrow code | An `activeCodePage` manifest can select UTF-8 on supported Windows; it is not a substitute for checking API-specific behavior, and GDI is an exception |
| PowerShell/native boundary | `[Console]::OutputEncoding` controls native-output decoding where PowerShell decodes it; `$OutputEncoding` controls text piped to native stdin |
| PowerShell files | Windows PowerShell 5.1 has inconsistent cmdlet defaults and emits a BOM with `-Encoding utf8`; PowerShell 7 defaults to UTF-8 without BOM. Select the writer/encoding the consumer requires |

For cmd scripts with non-ASCII text, save as UTF-8 and switch to `chcp 65001` from an ASCII line before non-ASCII commands are parsed. In PowerShell 5.1, UTF-8 scripts containing non-ASCII generally need a BOM. Do not blindly apply one file-encoding recipe to both shells.

For new CLI styling, use virtual terminal sequences after detecting a terminal and enabling `ENABLE_VIRTUAL_TERMINAL_PROCESSING` where required. Handle non-console/redirected handles separately; do not emit styling into machine-readable output. Encoding changes are not a replacement for a correct terminal/pipe boundary.

## API and GUI details

Check `HRESULT` with `FAILED`/`SUCCEEDED`, `LSTATUS` against `ERROR_SUCCESS`, and each handle/pointer/Boolean against its documented failure value. Use `GetLastError()` only when that API promises meaningful details; another call can overwrite it. Match resource-specific release functions, initialize fields such as `cbSize`, and use pointer-sized types without truncation.

Desktop GUI apps should declare DPI awareness in the manifest, typically `PerMonitorV2` when supported, and use per-window DPI rather than a process-wide assumption. Respect the framework's DPI setup instead of racing it with late runtime configuration.

Platform references: [long paths](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation), [case sensitivity](https://learn.microsoft.com/en-us/windows/wsl/case-sensitivity), and [DLL dependency search](https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order).
