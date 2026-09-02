---
name: ferris-tests
description: Standards for tests that catch real breaks. Use when writing or modifying tests, adding a regression test for a bug fix, reviewing a test-heavy diff, deciding what to mock or fake, or when a suite looks tautological, over-mocked, or stays green while production breaks. Also triggers on unit test, integration test, spec, mock, stub, fixture, assertion, coverage, TDD, red-green, property-based testing, mutation testing, and flaky-test cleanup. Diagnosing why a test fails belongs to ferris-debug; commit-time diff hygiene belongs to ferris-audit.
---

# Writing Tests

A test earns its place by naming the break it catches and exercising the real thing. Coverage that cannot fail on a real bug is maintenance debt, not safety. Rationale, mock guidance, and warning signs: [references/tests-and-mocks.md](./references/tests-and-mocks.md).

## Non-negotiables

1. **Name the break first.** Before writing the body, state the production change that would make this test fail; a test with no such change guards nothing.
2. **Watch every new test fail.** Run it before the fix exists, confirm it fails for the expected reason, then watch it pass. A test never seen red proves nothing.
3. **Hand-derive expectations.** Literals and hand-checked fixtures; computing the expected value with the code under test passes no matter what the code does. Table-driven cases with literal want values are the preferred shape.
4. **No change detectors.** Assert the behavior that depends on a decision, not the decision's surface (constant value, message wording, private structure).
5. **Mocks earn no assertions.** Mock only the slow or external layer below what the test observes; keep the side effects the test depends on real, and mirror the complete real data structure.
6. **Test your contract, not the framework's** — the route you register, the query you emit, the payload you produce.
7. **Test-only code lives in test utilities** — a method called only from tests never ships on a production class.
8. **Tests are frozen while implementing.** Never weaken, skip, or delete a test to make a run green; a genuinely wrong test is fixed in its own commit with the reason stated.
9. **Weak oracles go property-based.** When expectations are hard to hand-derive (parsers, round-trips, serialization, invariants), express the invariant as a property instead of copying observed output.
10. **Finish with the mutation check.** Run a mutation tool when the project has one (Stryker, cargo-mutants, mutmut); otherwise mutate by hand — wrong constant, swapped branch, dropped side effect, missing zero/empty case — and require at least one test to fail per realistic mutation.
