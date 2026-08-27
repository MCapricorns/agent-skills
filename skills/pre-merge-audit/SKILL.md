---
name: pre-merge-audit
description: ALWAYS use this skill BEFORE ANY git commit, push, merge, or PR submission — a MANDATORY pre-commit pass that cleans the staged diff (dead code, duplication, leftover debris), even when the user does not ask for it. Also use for explicit cleanup requests beyond the current diff — "clean this up before we commit", "remove the dead code", "dedupe and simplify, then submit" — and for read-only simplification surveys — "what can we delete here", "audit this module for dead code" — even when phrased casually. Surveys report ranked evidence only and never edit. No exception for trivial or single-file commits; only formatting-only changes may skip.
---

# Pre-Commit Clean

Three tiers by authority:

1. **Pre-commit pass (automatic, every commit)** — clean the staged diff. May edit, but only within code the current change adds or modifies.
2. **Deep cleanup (explicit edit intent)** — proven cuts anywhere in scope, applied end to end per `references/cleanup.md`, with structural targets from `references/structure.md` and concurrency/lifecycle protections from `references/lifecycle-and-races.md`.
3. **Survey (read-only)** — investigate, rank, report; never edit. Same proof standards, and a report with zero safe candidates is a valid outcome.

Measure twice, cut once — and never force a deletion to look productive. Zero cuts is a valid outcome in every tier.

## Pre-commit pass

Mandatory before EVERY commit, push, merge, or PR submission — even when nobody asks, and even for trivial or single-file changes. Only formatting-only changes may skip.

1. Tidy the staged diff: remove dead code the diff introduces, obvious duplication within it, leftover debris (commented-out code, unused imports/variables, debug output), and structural bloat the diff adds (thin wrappers, needless indirection, one-off flags tangling existing flow).
2. Cut only what the diff itself added or modified, and only with proof: no production consumers, unreachable, no behavior contract touched. Anything reaching beyond the diff is deep cleanup, not this pass.
3. Run the smallest targeted checks covering the change (typecheck, lint, touched tests).
4. Report what was cleaned — files/contracts removed, net reduction, check failures; the user still owns the commit itself.

## Deep cleanup

Only on explicit user intent; never escalate into edits on your own. Survey the scope first, then apply every safe, proven, in-scope cut end to end per `references/cleanup.md` (deletion proof, protected surfaces, design records, external findings) and `references/structure.md` (red lines, simplification targets), without per-item approval, then re-verify the cleanup diff. When a candidate touches concurrency, cancellation, resource cleanup, defensive copies, or state crossing a process or lifetime boundary, apply `references/lifecycle-and-races.md` before cutting.

## Survey

Read-only investigations — simplification audits, "what can be removed here" — never edit, no matter how obvious the cut. Partition the scope by responsibility, cover each part or exclude it with a reason, and grade every lead by the proof ladder in `references/cleanup.md` — search hits and analyzer output are leads, not authority. Report candidates ranked with confidence held apart from benefit, each naming the behavior it would surrender, the smallest check that would expose a wrong cut, and the exact missing fact for anything left unresolved. Then stop.

## Honesty rules

- A candidate is not a deletion; never cut without proof.
- Never force a deletion to look productive, or equate deletion volume with value.
- Never equate green tests with proof.
- Classify every reference (production, support-only, unresolved) — hit counts are not semantics.
