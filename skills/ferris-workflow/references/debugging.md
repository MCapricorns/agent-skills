# Debugging

Prove the cause before patching. For an obvious local defect, the evidence and repro may be a single failing command; do not manufacture a larger investigation.

## Investigation loop

1. **Capture:** read the full relevant error and stack trace; record the command, input, configuration, and expected behavior.
2. **Reproduce:** find the smallest reliable repro. Compare the last good state, including dependency/configuration/environment changes. Unreliable reproduction calls for more evidence, not a guessed fix.
3. **Locate:** follow bad values or ordering backward to the first violated contract. Read actual call sites. State one falsifiable hypothesis and the observation that distinguishes it from alternatives.
4. **Test:** change one variable, run the decisive check, and discard refuted experiments before trying another. Fix at the origin, not by masking the symptom.
5. **Regress:** prove the reported symptom on unfixed code, then the fix. Use the test reference linked from SKILL.md for test design; run affected checks and remove temporary instrumentation after verification.

Never weaken, skip, or delete a meaningful check to go green. If the check is genuinely wrong, explain its contract error and correct it separately from the implementation fix. After three failed fixes, stop patching and revisit the assumptions/design with the evidence. Label external/timing mitigations honestly; a retry or timeout is not a proven root-cause fix.

## Choose the missing-evidence tool

- **Deep stack:** trace the failing operation, its input, and callers until the first bad value or missing ordering guarantee. If reading cannot establish the chain, capture the relevant value and stack immediately before the operation. Keep validation at real ownership/trust boundaries, not every intermediate hop by reflex.
- **Unknown component:** instrument relevant inputs/outputs, sizes, parsed configuration, working directory, and ordering at boundaries, then narrow to the failing layer. Prefer stderr for test diagnostics when normal logging is suppressed. Never dump credentials, tokens, connection strings, or environment values; record names and presence only.
- **Unknown revision or shared-state pollution:** use `git bisect run <check>`, bisect test order, or halve suspected configuration groups. Each step needs an observed result; skip untestable revisions rather than guessing. Protect worktree changes when changing revisions.
- **Timing failure:** prefer explicit synchronization or controllable clocks to sleeps. Poll external conditions only with a hard timeout. Force the relevant ordering with barriers/hooks and capture the sequence that fails; stress runs may expose a race but cannot prove race freedom. Exercise early cancellation, late completion, and teardown with work in flight instead of widening delays.

Use only the technique needed to resolve the missing fact. Preserve intentional diagnostics, remove investigative debris, and report remaining uncertainty rather than overstating a diagnosis.
