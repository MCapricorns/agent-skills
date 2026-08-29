---
name: writing-tests
description: Standards for tests that catch real breaks. Use when writing or modifying tests, adding a regression test for a bug fix, reviewing a test-heavy diff, deciding what to mock or fake, or when a suite looks tautological, over-mocked, or stays green while production breaks. Also triggers on unit test, integration test, spec, mock, stub, fixture, assertion, coverage, TDD, red-green, and flaky-test cleanup. Diagnosing why a test fails belongs to systematic-debugging; commit-time diff hygiene belongs to pre-merge-audit.
---

# Writing Tests

A test earns its place by naming the break it catches and exercising the real thing. Coverage that cannot fail on a real bug is maintenance debt, not safety.

## Non-negotiables

1. **Name the break first.** Before writing the body, state the production change that would make this test fail — a wrong branch, missing side effect, wrong argument, boundary case, broken contract. If no such change exists, the test guards nothing: pick an observable behavior that does.
2. **Watch every new test fail.** Run it before the feature exists or with the fix reverted, confirm it fails for the expected reason (missing behavior, not a typo), then watch it pass. A test never seen red proves nothing — this red-green rule applies to regression tests and new behavior alike.
3. **Hand-derive expectations.** Literals and hand-checked fixtures; never compute the expected value with the code under test or its helpers — such a test passes no matter what the code does. Table-driven cases with literal want values are the preferred shape.
4. **No change detectors.** A test that fails only on intentional decisions — a constant's value, exact message wording, private structure, source text — fires on every redesign and sleeps through every bug. Assert the behavior that depends on the decision instead.
5. **Assert real behavior, never mock behavior.** A mock earns no assertions: a check that the mock was called says the mock is present, not that the component works. Mock only the slow or external layer below what the test observes, keep the side effects the test depends on real, and mirror the complete real data structure — partial mocks pass while integration breaks.
6. **Test your contract, not the framework's.** Cover the route you register, the query you emit, the payload you produce; upstream mechanics belong to their maintainers. Constructors, getters, and trivial forwarding earn tests only when they validate, normalize, default, derive, or cause side effects.
7. **Test-only code lives in test utilities.** A method called only from tests never ships on a production class.
8. **Finish with the mutation check.** Mentally mutate the production code — wrong constant, swapped branch, dropped side effect, empty return, missing validation of zero/empty/nil/unauthorized input. At least one test must fail per realistic mutation; a mutation nothing catches marks unprotected behavior or a tautological test.

## Warning signs

Setup and assertion share the same object (equality guaranteed); expected values hidden behind loops, builders, or helpers; mock setup dwarfs the test logic; assertions on a `*-mock` test id; a test that greps source text; a sleep that makes it pass (that is a race — see systematic-debugging); tests that exist for coverage with no observable outcome; a name with "and" in it (split it); mocking "just to be safe".

When mock setup outgrows the test logic or breaks whenever the mock changes, switch to an integration test with real components — the design is telling you the seam is wrong.
