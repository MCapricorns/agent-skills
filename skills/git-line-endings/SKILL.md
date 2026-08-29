---
name: git-line-endings
description: Repository line-ending contract — .gitattributes, CRLF vs LF, core.autocrlf. Use when git warns 'LF will be replaced by CRLF' or 'CRLF will be replaced by LF', when a diff or PR shows every line of a file changed or ^M carriage returns, when files appear modified right after clone or checkout with no edits, when .bat, .cmd, .sln, or .vcxproj files misbehave from LF endings, when adding or editing .gitattributes or core.autocrlf, or when creating a repository that Windows and non-Windows machines will share.
---

# Git Line Endings

Invoke whenever git prints an LF/CRLF warning, a diff churns whole files or shows `^M`, files sit modified right after a fresh clone, or before creating a repository that will be cloned on both Windows and non-Windows machines. Diagnose the current state with `git ls-files --eol` — it prints index vs worktree endings per file.

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
