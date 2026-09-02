---
name: ferris-debug
description: Root-cause-first debugging process. Use when anything misbehaves and the cause is not yet proven — a failing or flaky test, a reported bug, a crash, wrong output, a build or CI failure, a performance regression, 'it worked before', 'why does this happen', 'doesn't work' — before proposing or applying any fix, and especially when a quick patch is tempting, a previous fix did not stick, or several components could be at fault. Also triggers on error messages, stack traces, exceptions, segfaults, hangs, races, and intermittent failures. Not for tidying a working change (ferris-audit) or for test-quality rules (ferris-tests).
---

# Systematic Debugging

No fix without a proven root cause. Guessed patches destroy the evidence and stack new failure modes on old ones; the loop below is faster than thrashing — for simple bugs and emergencies too.

## The loop

1. **Read the evidence.** The full error text, the complete stack trace, the failing assertion, exact line numbers and error codes. Errors usually name their cause; do not skim past them.
2. **Reproduce reliably.** Exact steps, smallest input that still fails. No reliable repro means gather more data — never fix blind.
3. **Diff against the last good state.** Recent commits, dependency bumps, config and environment changes; `git bisect` when the breaking change is not obvious.
4. **Locate before theorizing.** When the failing path spans components (CI, build, signing; API, service, database), instrument each boundary and let the evidence name the failing layer; when the error surfaces deep in a call stack, trace the bad value backward to its origin — both per [references/tracing.md](./references/tracing.md). The fix belongs at the source, not where the error appeared.
5. **One hypothesis, one minimal change.** State "X causes this because Y", change a single variable, verify. Refuted means a new hypothesis — never a second fix stacked on the first, and never several changes at once. Not knowing is a finding: say what is still unknown and instrument for it.
6. **Fix with a regression test.** Write the failing repro test first (test quality per ferris-tests), apply the single root-cause fix, watch the test pass, confirm the suite stays green. No "while I'm here" changes riding along.

## Escalation

Count failed fix attempts. At three, stop treating it as a code bug and question the design: symptoms recurring in different places mean the pattern is wrong, not the patch. Lay out the structural options instead of attempting fix number four.

## Red flags — back to step 1

- "Quick fix for now, investigate later" / "just try changing X and see"
- Fixing where the error appears without tracing where the value came from
- "Probably X" with no verification; several changes in one attempt
- A fix that did not help but stays in anyway
- Explaining the bug without being able to reproduce it
- Skipping the regression test because the fix "obviously works"

When honest investigation lands on an external or timing cause, say so with the evidence, handle it explicitly (retry, timeout, clearer error), and leave instrumentation behind for the next occurrence. Most "no root cause" verdicts are unfinished investigations.
