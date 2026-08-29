---
name: git-line-endings
description: ALWAYS use this skill when a git LF/CRLF warning appears ("LF will be replaced by CRLF", "CRLF will be replaced by LF"), when setting up a new repository's line-ending contract, or when touching .gitattributes or core.autocrlf. Enforces declaring the contract in .gitattributes and renormalizing once, instead of per-user autocrlf luck.
---

# Git Line Endings

Invoke whenever git prints an LF/CRLF warning, or before creating a repository that will be cloned on both Windows and non-Windows machines.

`warning: in the working copy of '<file>', LF will be replaced by CRLF the next time Git touches it` means the repo relies on per-user `core.autocrlf` instead of declaring its contract. Never "fix" this by re-saving files or suppressing warnings. Do:

1. **Commit a `.gitattributes`** so the repo, not each clone, owns the contract:
   ```
   * text=auto
   *.bat   text eol=crlf
   *.cmd   text eol=crlf
   *.ps1   text eol=crlf
   *.sln   text eol=crlf
   *.vcxproj text eol=crlf
   *.png binary
   *.ico binary
   ```
   Windows-tooling files MUST be CRLF — cmd.exe, older Visual Studio, and some `.sln`/`.vcxproj` parsers break on LF. Mark real binaries explicitly; `* text=auto` covers the rest and keeps them LF in the index.
2. **Renormalize once**: `git add --renormalize . && git commit -m "chore: normalize line endings"`. Warn everyone to commit or stash first — renormalization rewrites the index.
3. **Keep `core.autocrlf=true` on Windows clones** as belt-and-suspenders; the `.gitattributes` is authoritative either way.

The contract is the `.gitattributes`; individual tool warnings are symptoms, not targets.
