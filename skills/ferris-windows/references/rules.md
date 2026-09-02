# Windows Rules — Rationale

Read when a rule in SKILL.md needs unpacking.

## Platform-rule rationale

- **`\\?\` and MAX_PATH**: the 260-char ceiling applies to most file APIs unless long paths are enabled — which needs *both* the machine policy (`LongPathsEnabled=1`) and a `longPathAware` manifest, and Explorer plus most third-party apps still don't handle long paths. `\\?\` remains the unconditional fallback; note it disables normalization — fully-qualified backslash paths only, no relative segments, no `.`/`..`.
- **Case-insensitivity**: the filesystem preserves the first casing written; two files differing only in case cannot coexist, and a case-only rename needs create-temp → delete-old → rename-temp.
- **Locking**: Windows denies deleting or replacing any file a process holds open — a running exe, a loaded DLL, an open log. Closing the holder (or ending the process) is the fix; retrying the delete is a loop.
- **DLL search order**: application dir, system dirs, then PATH (plus the working directory in legacy modes). Bare-name loads pick whichever matches first — hijack territory; `LoadLibraryExW` with an absolute path (or `LOAD_LIBRARY_SEARCH_*` flags) pins the right one.
- **Symlinks**: the Developer-Mode/`SeCreateSymbolicLinkPrivilege` requirement is unchanged as of Windows 11 24H2; junctions need no privilege. Treat symlink creation as fallible — degrade to junction or copy.
- **Elevation**: "run everything as administrator" disables UAC's least-privilege point; request elevation per documented admin operation (HKLM writes, services, protected files).

## Console and file encoding — the mojibake cure

Chinese text corrupts when the three layers — internal strings, bytes on the wire, terminal decode — disagree. Pin every layer explicitly:

- **MSVC compiles BOM-less UTF-8 sources as the system ACP by default** — on a Chinese-locale system that is GBK/936, and string literals corrupt silently at compile time. Compile with `/utf-8` (sets both source and execution charset). A UTF-8 BOM also forces UTF-8 source parsing but does nothing for the execution charset.
- **Output**: `SetConsoleOutputCP(CP_UTF8)` at startup, then write UTF-8 bytes (or `WriteConsoleW` to send UTF-16 straight to the console). `chcp 65001` does the same for the current console session only — an interactive fix, not a shipped tool's design.
- **Input**: read keyboard input with `ReadConsoleW`; the cooked-read path does not decode UTF-8 completely on current Windows.
- **The `activeCodePage` manifest key** (Windows 10 1903+) makes the process ACP UTF-8, so `-A` APIs and CRT narrow functions become UTF-8 — the sanctioned escape hatch for legacy narrow codebases. Prefer `W` + explicit encodings in new code. GDI does not follow per-process ACP; pre-1903 Windows silently falls back to the system page.
- **Pipes and files have no code page** — redirection carries raw bytes; the encoding is a contract stated on both ends. Pass `CP_UTF8` explicitly (never `CP_ACP`) in every `MultiByteToWideChar`/`WideCharToMultiByte` call.
- **Batch files**: `chcp 65001` at the top *and* save the script itself as UTF-8 — cmd parses BOM-less scripts with the OEM page.
- **Interpreters**: Python's console I/O already goes through the W APIs (set `PYTHONUTF8=1` to extend UTF-8 to files and pipes); Node and Go emit UTF-8 by default — when mojibake still appears, the cause is a legacy console still decoding at page 936, fixed by the output rules above.

## GUI manifests

- Desktop apps declare `<dpiAwareness>PerMonitorV2</dpiAwareness>` in the manifest (not a runtime `SetProcessDpiAwareness` call) and read per-window DPI with `GetDpiForWindow`; undeclared apps blur and mis-scale on mixed-DPI multi-monitor setups.
