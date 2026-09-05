# Tests That Catch Breaks

## Contract, not implementation

Name the production break and exercise the smallest real boundary that owns it. Derive expectations independently, not through production helpers. Source-text/private-structure assertions are change detectors unless that representation is the public contract; exact bytes/messages are valid when promised.

Keep helpers test-only. Use tables for cases of one contract, not forced splits of cohesive scenarios.

## Sensitivity

- Run each new test against missing/broken behavior: it must fail for the intended reason, not setup or compilation. For already-working behavior, inject a realistic temporary fault.
- Probe changed branches, boundaries, side effects, and empty-input behavior using the project's mutation tool or manual mutations. The same fault run can prove sensitivity; do not repeat equivalent mutations as ritual. Distinguish equivalent survivors from genuine coverage gaps.
- Restore the implementation and all mutations, then run affected checks green. Never weaken meaningful assertions to pass; explain and separately correct genuinely wrong expectations. Report sensitivity checks that could not run.

## Doubles and properties

Mock below the behavior under test, at the external/slow boundary. Model consumed fields and failure behavior faithfully; configured mock output alone proves nothing. Interactions are valid assertions when they are the contract, such as one correctly addressed request. Use integration coverage where a double cannot establish compatibility.

Combine generated properties with known valid/invalid examples or an independent oracle. Round trips can hide matching encoder/decoder bugs. Control time, randomness, and resources; wait for observable conditions with bounded timeouts instead of sleeps or retrying flaky tests away.
