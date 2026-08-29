---
name: verification-before-completion
description: Evidence gate for success claims. Use when about to say done, fixed, passing, working, complete, resolved, or ready for review — in a reply, summary, commit message, or PR description — or about to tick off a plan item, report that tests pass, the build succeeds, a bug is gone, or a feature works. Also triggers when accepting a subagent's success report, when satisfaction is about to be expressed ('great, everything works'), and when the only proof at hand is a stale, partial, or remembered run. Cleaning the diff itself belongs to pre-merge-audit.
---

# Verification Before Completion

Success is claimed after running the proof, never before. Fresh evidence against the current state of the code — not confidence, memory, extrapolation, or a subagent's word. This covers paraphrases too: any wording that implies things work is a claim.

## The gate

Before any statement implying success:

1. Name the command that would prove the claim.
2. Run it fresh, complete for the claimed scope, against the current state.
3. Read the output — exit code, failure count, warnings — not just its tail.
4. Output confirms: make the claim, citing the evidence. Output refutes: report the actual state with the output, no softening.

## Claims and their proof

| Claim | Proof required | Not proof |
|-------|----------------|-----------|
| Tests pass | fresh run of the claimed scope, zero failures | yesterday's run, "should pass", a subset extrapolated |
| Build succeeds | build exits 0 | linter green, logs "look fine" |
| Bug fixed | original repro now passes, regression test seen red then green | "the code changed", plausible-looking diff |
| Requirements met | line-by-line check against the original request | tests green |
| Subagent finished X | its diff and artifacts inspected directly | its success message |

## Red flags

"Should work", "probably fixed", "seems to", celebration before the run, committing or pushing with a check still unread, trusting an agent's report, counting a partial run as the whole, being tired and wanting the task over. Each one means: stop and run the proof.

Green checks prove the checks pass, not that the work is right or complete — requirements still get compared line by line, and the diff still gets its pre-merge-audit pass.
