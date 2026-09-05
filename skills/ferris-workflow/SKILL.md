---
name: ferris-workflow
description: Debugging, regression tests, cleanup and read-only audits, lifecycle/race analysis, and completion evidence before commit, push, merge, or PR.
---

# Engineering Workflow

Use only the phase needed. Check `git status` and preserve unrelated work; a read-only request allows no edits, and this skill grants no commit, push, release, or broader-cleanup authorization.

| Task | Read |
|------|------|
| Failure, regression, crash, failing build/test, hang, or race | [references/debugging.md](./references/debugging.md) |
| Test design/review, doubles, properties, or mutation coverage | [references/tests.md](./references/tests.md) |
| Explicit cleanup or deletion audit | [references/cleanup.md](./references/cleanup.md) |
| Simplifying cancellation, resource cleanup, defensive copies, or cross-lifetime state | [references/lifecycle-and-races.md](./references/lifecycle-and-races.md) |

## Completion evidence

- Run the smallest decisive check, then relevant repository gates. Read exit codes, failures, and warnings; report checked scope and blocked/unrun checks. Lint is not a build, execution coverage is not regression sensitivity, and a green check is not proof of every requirement.
- A fix needs the original repro failing before and passing after, with regression coverage. Compare performance/size on the same workload and environment; repeat performance measurements.
- Inspect the integrated diff against the request and actual check artifacts, including delegated work. Reuse evidence that covers the current state; rerun affected checks after edits/integration, not unchanged checks as ceremony. Never weaken a meaningful check to pass.

## Diff-local hygiene

Before commit, push, merge, or PR, remove proven dead additions, unused imports, debug debris, commented-out code, duplication, and unnecessary wrappers. Preserve intentional diagnostics and explicitly requested public APIs, even without in-repo consumers. Keep unrelated renames/reformatting out; broader cuts need the cleanup reference and explicit scope. One pass covers an unchanged diff; formatting-only changes may skip it. Recheck affected behavior after cleanup; zero safe cuts is valid.
