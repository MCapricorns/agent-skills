# Debugging

Capture the failing command, input/configuration, relevant error/stack, and expected result. Find the smallest reliable repro and compare the last good revision, dependencies, and environment. An obvious local defect needs no elaborate investigation; an unreliable repro needs evidence, not a guessed patch.

Trace to the first violated contract and state a falsifiable hypothesis. Change one variable, run the discriminating check, and discard refuted experiments. Prove the symptom on unfixed code and the fix with regression coverage. After three failed fixes, revisit assumptions/design rather than stacking patches. A retry or timeout may mitigate a symptom; label it as mitigation, not a proven root-cause fix.

## Match the tool to the missing fact

- **Bad value or deep stack:** trace the failing operation's inputs/callers backward; if reading is insufficient, capture values and stack immediately before failure. Keep validation at actual ownership/trust boundaries, not every hop.
- **Unknown layer:** instrument inputs/outputs, sizes, parsed configuration, working directory, and ordering at component boundaries. Use stderr when test logging is suppressed. Never dump credentials, tokens, connection strings, or environment values; record names/presence only.
- **Unknown revision or test pollution:** use `git bisect run <check>`, test-order bisection, or configuration halving. Observe each result, skip untestable revisions, and protect worktree changes.
- **Timing:** use barriers/hooks or controllable clocks to force the failing ordering. Bound external polling; sleeps and stress runs cannot prove race freedom. Exercise early cancellation, late completion, and teardown with work in flight rather than widening delays.

Remove investigative debris, retain intentional diagnostics, and report unresolved uncertainty. Never weaken a meaningful check to go green; a wrong check needs an explained contract correction separate from the implementation fix.
