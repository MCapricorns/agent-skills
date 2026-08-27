---
name: pre-merge-audit
description: ALWAYS use this skill BEFORE ANY git commit, push, merge, or PR submission — a MANDATORY pre-commit pass that cleans the staged diff (dead code, duplication, leftover debris), even when the user does not ask for it. Also use on explicit cleanup requests that go beyond the current diff — "clean this up before we commit", "remove the dead code", "dedupe and simplify, then submit" — even when phrased casually. No exception for trivial or single-file commits; only formatting-only changes may skip.
---

# Pre-Commit Clean

Two tiers by authority:

1. **Pre-commit pass (automatic, every commit)** — clean the staged diff. May edit, but only within code the current change adds or modifies.
2. **Deep cleanup (explicit intent only)** — proven cuts anywhere in scope per `references/cleanup.md` and `references/structure.md`.

Measure twice, cut once — and never force a deletion to look productive. Zero cuts is a valid outcome.

## Pre-commit pass

Mandatory before EVERY commit, push, merge, or PR submission — even when nobody asks, and even for trivial or single-file changes. Only formatting-only changes may skip.

1. Tidy the staged diff: remove dead code the diff introduces, obvious duplication within it, leftover debris (commented-out code, unused imports/variables, debug output), and structural bloat the diff adds (thin wrappers, needless indirection, one-off flags tangling existing flow).
2. Cut only what the diff itself added or modified, and only with proof: no production consumers, unreachable, no behavior contract touched. Anything reaching beyond the diff is deep cleanup, not this pass.
3. Run the smallest targeted checks covering the change (typecheck, lint, touched tests).
4. Report what was cleaned — files/contracts removed, net reduction, check failures; the user still owns the commit itself.

## Deep cleanup

Only on explicit user intent; never escalate into edits on your own. Survey the scope first, then apply every safe, proven, in-scope cut end to end per `references/cleanup.md` (deletion proof, protected surfaces) and `references/structure.md` (red lines, simplification targets), without per-item approval, then re-verify the cleanup diff.

## Honesty rules

- A candidate is not a deletion; never cut without proof.
- Never force a deletion to look productive, or equate deletion volume with value.
- Never equate green tests with proof.
