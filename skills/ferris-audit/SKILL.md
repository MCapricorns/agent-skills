---
name: ferris-audit
description: Evidence gate and hygiene pass for finishing work. Use when about to claim done, fixed, passing, or ready for review in any reply, summary, commit message, or PR, when ticking off a plan item or accepting a subagent's success report, and before any commit, push, merge, or PR — the staged diff gets cleaned even when nobody asks. Also when the user asks to clean up, simplify, dedupe, or strip dead code, or wants a read-only audit of what can be deleted. Triggers on ship it, land it, dead code, unused imports, leftover debug logging, 'should work', 'probably fixed', stale proof. Not for diagnosing broken behavior (ferris-debug) or test-quality rules (ferris-tests). Formatting-only changes may skip.
---

# Audit and Verification

Two gates guard the finish line: no success claim without fresh proof against the current state of the code — never confidence, memory, extrapolation, or a subagent's word — and no commit that still ships its own debris.

## The verification gate

Before any statement implying success — done, fixed, passing, working, resolved, ready for review; paraphrases count, in replies, summaries, commit messages, and PR descriptions alike:

1. Name the command that would prove the claim.
2. Run it fresh, complete for the claimed scope, against the current state.
3. Read the output — exit code, failure count, warnings — not just its tail.
4. Output confirms: make the claim, citing the evidence. Output refutes: report the actual state with the output, no softening.

| Claim | Proof required | Not proof |
|-------|----------------|-----------|
| Tests pass | fresh run of the claimed scope, zero failures | yesterday's run, "should pass", a subset extrapolated |
| Build succeeds | build exits 0 | linter green, logs "look fine" |
| Bug fixed | original repro now passes, regression test seen red then green | "the code changed", a plausible-looking diff |
| Requirements met | line-by-line check against the original request | tests green |
| Faster or smaller | before/after measurement of the same workload on one machine, repeated | a reasoned argument, a micro-benchmark never run |
| Subagent finished X | its diff and artifacts inspected directly | its success message |

Red flags: "should work", "seems to", celebration before the run, counting a partial run as the whole, trusting an agent's report. Green checks prove the checks pass, not that the work is right or complete.

## The hygiene pass — three tiers by authority

Measure twice, cut once — and never force a deletion to look productive. Zero cuts is a valid outcome in every tier.

### Pre-commit pass (automatic, every commit)

Mandatory before EVERY commit, push, merge, or PR — even when nobody asks, even for trivial single-file changes. Formatting-only changes may skip.

1. Tidy the staged diff: remove dead code the diff introduces, duplication within it, leftover debris (commented-out code, unused imports/variables, temporary debug output), and structural bloat the diff adds (thin wrappers, needless indirection, one-off flags). Durable logging the change is meant to ship is not debris — only instrumentation added to investigate goes.
2. Cut only what the diff itself added or modified, and only with proof: no production consumers, unreachable, no behavior contract touched. Anything reaching beyond the diff is deep cleanup, not this pass.
3. Every new function or API the diff introduces has a consumer in the same diff — unconsumed additions are deleted, not parked for later.
4. Structural churn rides separately: renames, moves, and reformats do not mix with behavior changes in one commit.
5. Run the smallest targeted checks covering the change (typecheck, lint, touched tests), then report what was cleaned; the user still owns the commit itself.

### Deep cleanup (explicit user intent)

Survey the scope first, then apply every safe, proven, in-scope cut end to end per [references/cleanup.md](./references/cleanup.md) (deletion proof, protected surfaces, design records, external findings) and [references/structure.md](./references/structure.md) (red lines, simplification targets), without per-item approval, then re-verify the cleanup diff. When a candidate touches concurrency, cancellation, resource cleanup, defensive copies, or state crossing a process or lifetime boundary, apply [references/lifecycle-and-races.md](./references/lifecycle-and-races.md) before cutting.

### Survey (read-only)

Read-only investigations — simplification audits, "what can be removed here" — never edit, no matter how obvious the cut. Split the scope along ownership lines; for any part not covered, say why. Grade every lead by the proof ladder in [references/cleanup.md](./references/cleanup.md) — search hits and analyzer output are leads, not authority. Rank the report so that how sure you are stays separate from how much a cut is worth; each candidate names the behavior it gives up, the one check that catches a mistaken cut, and the exact missing fact for anything unresolved. Then stop.
