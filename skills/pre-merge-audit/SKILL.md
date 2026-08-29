---
name: pre-merge-audit
description: Pre-commit hygiene pass and dead-code cleanup. Use before any git commit, push, merge, or PR submission — the staged diff gets cleaned even when nobody asks, including trivial or single-file commits — and when the user asks to clean up, simplify, dedupe, or strip dead code ('clean this up before we commit', 'remove what is unused', 'dedupe and simplify, then submit'), or wants a read-only audit ('what can we delete here', 'audit this module for dead code'). Also triggers on commit, push, merge, PR, ship it, land it, submit, dead code, leftover debug logging, unused imports. Not for diagnosing broken behavior (systematic-debugging), test-quality rules (writing-tests), or proving success claims (verification-before-completion). Formatting-only changes may skip.
---

# Pre-Merge Audit

Three tiers by authority:

1. **Pre-commit pass (automatic, every commit)** — clean the staged diff. May edit, but only within code the current change adds or modifies.
2. **Deep cleanup (explicit edit intent)** — proven cuts anywhere in scope, applied end to end per `references/cleanup.md`, with structural targets from `references/structure.md` and concurrency/lifecycle protections from `references/lifecycle-and-races.md`.
3. **Survey (read-only)** — investigate, rank, report; never edit. Same proof standards, and a report with zero safe candidates is a valid outcome.

Measure twice, cut once — and never force a deletion to look productive. Zero cuts is a valid outcome in every tier.

## Pre-commit pass

Mandatory before EVERY commit, push, merge, or PR submission — even when nobody asks, and even for trivial or single-file changes. Only formatting-only changes may skip.

1. Tidy the staged diff: remove dead code the diff introduces, obvious duplication within it, leftover debris (commented-out code, unused imports/variables, debug output), and structural bloat the diff adds (thin wrappers, needless indirection, one-off flags tangling existing flow). House compliance markers (`// ... guideline compliant ...`) are contracts, not debris.
2. Cut only what the diff itself added or modified, and only with proof: no production consumers, unreachable, no behavior contract touched. Anything reaching beyond the diff is deep cleanup, not this pass.
3. Run the smallest targeted checks covering the change (typecheck, lint, touched tests).
4. Report what was cleaned — files/contracts removed, net reduction, check failures; the user still owns the commit itself.

## Deep cleanup

Only on explicit user intent; never escalate into edits on your own. Survey the scope first, then apply every safe, proven, in-scope cut end to end per `references/cleanup.md` (deletion proof, protected surfaces, design records, external findings) and `references/structure.md` (red lines, simplification targets), without per-item approval, then re-verify the cleanup diff. When a candidate touches concurrency, cancellation, resource cleanup, defensive copies, or state crossing a process or lifetime boundary, apply `references/lifecycle-and-races.md` before cutting.

## Survey

Read-only investigations — simplification audits, "what can be removed here" — never edit, no matter how obvious the cut. Split the scope along ownership or responsibility lines; for any part you did not cover, say why. Grade every lead by the proof ladder in `references/cleanup.md` — search hits and analyzer output are leads, not authority. Rank the report so that how sure you are stays a separate question from how much a cut is worth, and have each candidate name the behavior it gives up, the one check that catches a mistaken cut, and the exact missing fact for anything left unresolved. Then stop.

## Honesty rules

- A candidate is not a deletion; never cut without proof.
- Never force a deletion to look productive, or equate deletion volume with value.
- Never equate green tests with proof.
- Classify every reference (production, support-only, unresolved) — a search hit says nothing about whether code runs.
