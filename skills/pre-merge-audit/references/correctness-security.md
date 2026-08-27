# Part 1 — Correctness & Security

Read this before the correctness pass of every audit run.

## Trace side effects end-to-end

This is a complex codebase with many cross-package and cross-module dependencies. Simple local edits often break distant functionality. You MUST trace every change through its possible side effects before clearing it.

Hunt specifically for:

- **Bugs and logic errors** in the new or changed paths, including edge cases and error handling.
- **Security vulnerabilities** introduced by the change.
- **Developer-experience (DX) breakage.** It is easy to silently break how developers run or build the code locally. Examples (not exhaustive):
  - changing how secrets are read, or where they are read from
  - renaming or adding environment variables
  - remapping ports or networking
  - adding scripts that must be run for existing functionality to keep working

  Adding a dependency through the normal package manager does NOT count; forcing a manual install outside the normal workflow (a website, an app store) does.
- **Feature-gate leaks.** Features are often carefully gated behind feature flags or internal-only checks, and the leaks are usually subtle. Be very careful that nothing meant to stay gated leaks out.
