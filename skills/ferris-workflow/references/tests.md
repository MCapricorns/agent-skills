# Tests That Catch Breaks

## Choose an observable contract

- Name the realistic production break the test must catch, then exercise the real behavior at the smallest useful boundary. Test the route, query, payload, state change, or failure policy your code owns, not framework internals.
- Derive expectations independently: hand-checked literals/examples or an independent oracle. Never compute expected values through the implementation or its helpers.
- Avoid change detectors: private structure, source-text matching, or incidental wording. Exact bytes, messages, and constants are valid assertions when they are the public contract, not merely today's implementation.
- Keep test-only helpers in test utilities, not production APIs. Prefer table-driven cases when they express one contract clearly; do not split a cohesive scenario merely because its name contains "and".

## Prove sensitivity, then verify

1. Run each new test against the missing/broken behavior and require the intended failure, not a setup or compilation error. For already-working behavior, introduce a realistic temporary fault and confirm the test catches it.
2. Restore the intended implementation and run the test green. Never weaken, skip, or delete a meaningful check to pass; a genuinely wrong expectation needs a stated contract reason and a separate correction.
3. Check realistic mutations in the changed behavior: a swapped branch, wrong boundary, missing side effect, or empty-input bug. Use the project's mutation tool when available, otherwise mutate by hand. Earlier fault-injection runs can satisfy the same check; do not repeat equivalent mutations as a finishing ritual. Restore all mutations and run affected checks on the final state.

A surviving mutant is a lead: distinguish equivalent behavior from a real gap. Execution coverage alone does not establish sensitivity. Report any proof that could not be run rather than treating it as passed.

## Select doubles and properties deliberately

Mock only the external/slow boundary below the behavior under test. Keep the component real and model the relevant dependency contract faithfully, including consumed fields and failure behavior. An assertion that a configured mock returned its configured value proves nothing. An interaction assertion can be valid when the interaction itself is the contract, such as sending one correctly addressed request; use integration coverage where a double cannot prove compatibility.

When exact expectations are hard to derive, combine concrete examples with generated properties or an independent reference implementation. Round-trip properties alone can miss matching encoder/decoder bugs; add known valid/invalid examples and invariants not shared by both sides.

Keep time, randomness, and resources controlled. Wait for observable conditions with bounded timeouts rather than arbitrary sleeps; diagnose flaky ordering using the debugging reference linked from SKILL.md instead of retrying it away.
