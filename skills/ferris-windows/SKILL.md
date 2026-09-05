---
name: ferris-windows
description: Windows paths, encoding, DLL loading, elevation, and Win32/COM/PInvoke contracts. Use when a task hinges on those surfaces or on PowerShell 7 argument and encoding rules.
---

# Windows Engineering

Default to Windows and PowerShell 7 (`pwsh`) for house development and command examples. Use another host, Windows PowerShell 5.1, or cmd/batch only when the task or repository requires it.

Read the relevant sections of [references/rules.md](./references/rules.md). Runtime behavior wins over house defaults; do not apply every Windows rule to a shell-only task.

## Shell execution

- Chain success-dependent native commands with `&&`. Use explicit status handling only for special exit-code contracts or recovery. Cmdlet error handling is separate.
- Use argument arrays and literal paths. PowerShell is not a POSIX shell.

Use ferris-native for language ownership and builds, ferris-workflow for diagnosis, tests, and verification.
