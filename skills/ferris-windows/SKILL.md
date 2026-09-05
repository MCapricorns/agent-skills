---
name: ferris-windows
description: Windows-targeted code/builds, PowerShell or batch scripts, paths/filesystem, console encoding, DLL loading, elevation, and Win32/COM/PInvoke contracts. C++ and Rust language details belong to ferris-native.
---

# Windows Development

Apply the relevant platform, shell, or API rules; not every Windows task needs all three. The documented API/runtime contract wins over a house default.

## Platform and API contracts

- **Paths:** long-path support depends on the API/runtime and application configuration. Use extended paths only where supported; never blindly prepend `\\?\`. Keep Unicode paths and portable filenames; assume case-insensitive defaults without assuming every directory is case-insensitive.
- **Open files:** delete/replace behavior depends on existing share modes, notably `FILE_SHARE_DELETE`. Identify the denying holder on sharing violations; retries help only if it will release the handle.
- **DLLs:** load non-system DLLs from trusted absolute paths and constrain dependency searching. An absolute path to the top-level DLL alone does not secure its dependencies.
- **Text:** use Unicode `W` APIs for new code, honor bytes versus UTF-16 code units and terminators, and specify encodings at process/file/pipe boundaries. Do not use the system ANSI code page for durable or protocol text.
- **Failure and ownership:** check documented sentinels/status values; capture `GetLastError()` immediately only where documented. Match every owned handle/buffer/COM allocation with its release operation; never release borrowed/pseudo-handles. Initialize size/version fields and preserve pointer-sized values.
- **Privilege:** run unelevated unless the operation needs elevation. Symlink creation is fallible; directory junctions and copies are not transparent fallbacks. Use only an explicitly accepted behavior-preserving alternative or fail clearly.

## Shell execution

- Check `$LASTEXITCODE` immediately after each native tool and interpret its documented codes; stop on actual failure. PowerShell cmdlet failures need PowerShell error handling, not `$LASTEXITCODE`. Batch scripts check `if errorlevel 1` for tools whose nonzero codes mean failure.
- `&&`/`||` require PowerShell 7+. Windows PowerShell 5.1 needs separate commands and explicit checks. Do not assume POSIX quoting, globbing, or redirection semantics; prefer argument arrays and literal paths over constructed command strings.
- Set text encodings deliberately. Console/native-pipe encodings and file encodings are separate; `-Encoding utf8` has different BOM behavior in Windows PowerShell 5.1 and PowerShell 7.

Read the relevant sections of [references/rules.md](./references/rules.md) for long paths, names, DLL search, encoding/terminal output, or GUI manifests. Use ferris-native for language-specific wrappers and ferris-workflow for diagnosis, tests, and verification.
