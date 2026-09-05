---
name: ferris-workflow
description: Engineering workflow for debugging failures/regressions, designing tests, verifying completion or delegated work, and cleanup or read-only audits. Use before commit, push, merge, or PR; language/platform details belong to ferris-native and ferris-windows.
---

# Engineering Workflow

Use the phase the task needs, not every phase as a ceremony. Preserve unrelated worktree changes. Read-only requests never authorize edits; this skill never authorizes a commit, push, release, or broader cleanup by itself.

## Route the work

| Task | Read when needed |
|------|------------------|
| Unexplained failure, regression, crash, failing build/test, hang, or race | [references/debugging.md](./references/debugging.md) — root cause before patching |
| Write/change/review tests, mocks, fixtures, properties, or mutation coverage | [references/tests.md](./references/tests.md) — observable contracts and fault sensitivity |
| Explicit cleanup or read-only deletion/simplification audit | [references/cleanup.md](./references/cleanup.md) — consumers, contracts, and deletion proof |
| Simplify concurrency, cancellation, cleanup, defensive copies, or cross-lifetime state | [references/lifecycle-and-races.md](./references/lifecycle-and-races.md) — ordering and quiescence |

A localized fix need not load deep-cleanup guidance. An ordinary implementation need not run a debugging investigation. Use only the applicable references; finish with the checks below.

## Prove the claim

Before claiming success, run the proving check against the current state and read its exit code, failures, and warnings. Start with the smallest decisive check, then the relevant repository gates. Report the actual scope and any blocked or unrun checks; confidence and another agent's summary are not evidence.

| Claim | Required evidence |
|-------|-------------------|
| Tests pass | Completed run of the claimed scope with zero failures |
| Build succeeds | Successful build, not merely lint or typecheck |
| Bug fixed | Original repro fails before the fix and passes after it, with regression coverage |
| Requirements met | Diff checked against the request, including non-testable requirements |
| Faster or smaller | Before/after measurement of the same workload and environment; repeat performance measurements |
| Delegated work complete | Integrated diff and actual check artifacts inspected directly |

A check already run in this task counts if it covers the current state. Re-run affected checks after edits or integration; do not repeat an unchanged run just to restate its result. Green checks prove their scope, not the entire request.

## Clean the intended diff once

Before commit, push, merge, or PR, remove proven diff-local dead additions, unused imports, temporary debug output, commented-out code, duplication, and unnecessary wrappers. Preserve intentional diagnostics and unrelated changes. Formatting-only changes may skip this hygiene pass.

Remove speculative APIs without consumers, but an explicitly requested published API is not dead merely because its callers live elsewhere. Keep unrelated renames, moves, and reformatting separate from behavior changes. Broader cleanup needs explicit intent and the cleanup reference; zero safe cuts is a valid result.

Run affected checks after cleanup. One pass covers the same unchanged diff; later edits need their affected scope rechecked. Never weaken a meaningful check to manufacture success.
