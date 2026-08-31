---
name: ferris-line-endings
description: Repository line-ending contract — .gitattributes, CRLF vs LF, core.autocrlf. Use when git warns 'LF will be replaced by CRLF' or 'CRLF will be replaced by LF', when that warning keeps coming back after renormalization, when a diff or PR shows every line of a file changed or ^M carriage returns, when files appear modified right after clone or checkout with no edits, when .bat, .cmd, .sln, or .vcxproj files misbehave from LF endings, when adding or editing .gitattributes or core.autocrlf, or when creating a repository that Windows and non-Windows machines will share.
---

# Git Line Endings

Invoke whenever git prints an LF/CRLF warning, a diff churns whole files or shows `^M`, files sit modified right after a fresh clone, or before creating a repository that will be cloned on both Windows and non-Windows machines. Diagnose the current state with `git ls-files --eol` — it prints index vs worktree endings per file.

`warning: in the working copy of '<file>', LF will be replaced by CRLF the next time Git touches it` means the file is LF on disk but the checkout policy (`core.autocrlf=true` with no `eol` attribute) would write CRLF the next time Git touches it. `* text=auto` alone does NOT silence it — it only normalizes the index, so the warning returns on every `git add` of an LF-edited file. Never "fix" this by re-saving files or suppressing warnings. Give the repo an explicit contract:

1. **Commit a `.gitattributes`** so the repo, not each clone, owns the contract, and text sources are pinned to LF in the worktree:
   ```
   * text=auto eol=lf
   *.bat   text eol=crlf
   *.cmd   text eol=crlf
   *.ps1   text eol=crlf
   *.sln   text eol=crlf
   *.vcxproj text eol=crlf
   *.png binary
   *.ico binary
   ```
   Windows-tooling files MUST be CRLF — cmd.exe, older Visual Studio, and some `.sln`/`.vcxproj` parsers break on LF. Everything else checks out LF, so an LF-edited worktree file is clean instead of perpetually warning. Mark real binaries explicitly.
2. **Renormalize the index once**: `git add --renormalize . && git commit -m "chore: normalize line endings"`. Warn everyone to commit or stash first — renormalization rewrites the index.
3. **Rewrite the worktree once** so files match the contract: `git rm --cached -r . && git reset --hard` (commit or stash first — uncommitted tracked changes are lost). Until every tracked file has been rewritten under the new attributes, the warning keeps firing.
4. **Leave `core.autocrlf` alone afterwards** — for covered paths the `.gitattributes` is authoritative, so flipping it per machine is not the fix and cannot silence the warning.

Verify with `git ls-files --eol`: text sources show `i/lf w/lf` (`w/crlf` only for declared CRLF types) and the warning no longer fires. The contract is the `.gitattributes`; individual tool warnings are symptoms, not targets.
