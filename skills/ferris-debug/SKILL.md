---
name: ferris-debug
description: Root-cause-first debugging. Use when anything misbehaves and the cause is not yet proven — failing or flaky tests, reported bugs, crashes, wrong output, build or CI failures, performance regressions, hangs, races, 'it worked before', 'why does this happen' — before proposing or applying any fix, especially when a quick patch is tempting, a previous fix did not stick, or several components could be at fault. Also triggers on error messages, stack traces, exceptions, segfaults, and intermittent failures. Not for tidying a working change (ferris-audit) or test-quality rules (ferris-tests).
---

# Systematic Debugging

No fix without a proven root cause. Guessed patches destroy the evidence and stack new failure modes on old ones; the loop below is faster than thrashing — for simple bugs and emergencies too. Evidence-collection detail: [references/tracing.md](./references/tracing.md).

## The loop

1. **Read the evidence** — full error text, complete stack trace, failing assertion, error codes. Errors usually name their cause; do not skim past them.
2. **Reproduce reliably** — exact steps, smallest input that still fails. No reliable repro means gather more data; never fix blind.
3. **Diff against the last good state** — recent commits, dependency bumps, config and environment changes; `git bisect` when the breaking change is not obvious.
4. **Locate before theorizing** — trace bad values backward to their origin and instrument component boundaries (per references/tracing.md); the fix belongs at the source, not where the error appeared.
5. **One hypothesis, one minimal change** — state "X causes this because Y", change a single variable, verify. Refuted means a *new* hypothesis — never a second fix stacked on the first, never several changes at once. Stuck means instrument more, not guess differently.
6. **Fix with a regression test** — run it against the unfixed code first and require the *reported* symptom, not merely some failure; then apply the single root-cause fix and watch it pass. Test shape and quality per ferris-tests. No "while I'm here" changes riding along; leftover instrumentation goes out in the ferris-audit pre-commit pass.

## Hard rules

- **Never make a check pass by weakening it.** Modifying, skipping, or deleting tests and validators to go green attacks the messenger; if the check itself is wrong, say so and change it in its own commit.
- **Three failed fixes stop the patching.** Symptoms recurring in different places mean the pattern is wrong, not the patch: question the design and lay out structural options instead of attempting fix number four.
- **A bug you cannot reproduce is a hypothesis, not a diagnosis.** Say what is still unknown, instrument for it, and when honest investigation lands on an external or timing cause, say so with the evidence and handle it explicitly (retry, timeout, clearer error).
