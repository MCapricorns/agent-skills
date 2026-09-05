---
name: ferris-windows
description: Windows-first development with PowerShell 7, paths, encoding, DLL loading, elevation, and Win32/COM/PInvoke contracts; legacy shells when required.
---

# Windows Engineering

Default to Windows and PowerShell 7 (`pwsh`) for house development and command examples. Use another host, Windows PowerShell 5.1, or cmd/batch only when the task/repository requires it.

Read the relevant sections of [references/rules.md](./references/rules.md) for paths/share modes, DLL dependencies, encoding/terminal I/O, privilege, and API/GUI contracts. Runtime/API behavior wins over house defaults; do not apply every Windows rule to a shell-only task.

## Shell execution

- Check `$LASTEXITCODE` immediately after each native tool and interpret its documented codes; stop on actual failure. Cmdlet errors require PowerShell error handling, not `$LASTEXITCODE`.
- Use argument arrays and literal paths instead of constructed command strings. PowerShell is not a POSIX shell; quoting, wildcard expansion, and native argument passing follow the host's rules.

Use ferris-native for language ownership/build details and ferris-workflow for diagnosis, tests, and verification.
