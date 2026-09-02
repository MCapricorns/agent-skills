# Tests and Mocks — Detail

Read when a non-negotiable in SKILL.md needs unpacking: why a rule exists, how far to take it, and the warning signs that a suite is decorative.

## Why each rule exists

- **Name the break first** forces the test to observe behavior. If the only failure you can describe is "the code changed", the test is a change detector; pick an observable behavior instead.
- **Seen red** is the only proof a test can fail. Tests written after the fix, or never run against the bug, routinely assert the buggy behavior by accident.
- **Hand-derived expectations** close the classic tautology: expected values computed by the code under test (or its helpers) make the test pass for every possible implementation, including the broken one.
- **Mocks earn no assertions**: a check that the mock was called says the mock is present, not that the component works. Partial mocks pass while integration breaks — mirror the complete real data structure.

## Mock or real?

Mock only the slow or external layer *below* the seam the test observes (network, clock, filesystem, third-party API). Keep everything above the seam real. When mock setup outgrows the test logic, or tests break whenever the mock changes, the design is telling you the seam is wrong — switch to an integration test with real components instead of mocking "just to be safe".

## Warning signs

Setup and assertion share the same object (equality guaranteed); expected values hidden behind loops, builders, or helpers; assertions on a `*-mock` test id; a test that greps source text; a sleep that makes it pass (that is a race — see ferris-debug); tests that exist for coverage with no observable outcome; a name with "and" in it (split it).

## Property-based testing

When the expected output is hard to write down but an invariant is easy (round-trip parse/print, serialize/deserialize, monotonic ids, ordering), state the invariant and let a generator (Hypothesis, proptest, fast-check) supply inputs. Properties are immune to the copy-the-output tautology because the expectation is a relation, not a value. Keep a few concrete literal examples alongside the properties for readability and debuggability.

## Mutation testing

Mutation testing is the mechanized form of the mutation check: the tool flips constants, negates branches, and deletes side effects, and reports mutants no test killed. Treat a surviving realistic mutant as unprotected behavior or a tautological test. It is the strongest signal available on whether a suite catches real breaks — coverage only measures execution.
