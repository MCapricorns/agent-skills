# Tracing and Evidence

Read this when the error surfaces deep in a call stack, when the failing component is unknown, or when the failure is intermittent.

## Trace the bad value backward

Where an error surfaces is rarely where the mistake lives. Walk the chain upstream:

1. **Symptom** — the operation that visibly failed and the value it choked on.
2. **Immediate cause** — the code that directly performed that operation.
3. **Caller** — who invoked it, and with what arguments. Read the actual call site; do not assume.
4. **Ascend** — repeat until the first place the value went wrong (empty string, stale handle, wrong path, unset variable). That is the origin.
5. **Fix at the origin.** Then decide layer by layer whether the intermediate hops deserve validation of their own — an assert or early check at each real ownership boundary turns the next occurrence of this class of bug into an immediate, local failure instead of a deep mystery.

When the chain cannot be walked by reading, capture it at runtime: log the suspicious value plus a stack trace (`new Error().stack`, `backtrace`, `CaptureStackBackTrace`) immediately **before** the dangerous operation — after it fails is too late, the state is gone.

## Instrument component boundaries

When a path spans several components and any of them could be at fault, stop reasoning and measure. For each boundary in the failing path, log what enters and what exits: values, sizes, environment variables, config as parsed, working directory. Run the failing scenario once and read the trail — the failing layer names itself, and the investigation narrows from "somewhere in the pipeline" to one component.

Practical rules: print to stderr in test code (loggers are often suppressed or buffered); include timestamps when ordering matters; redact credentials, tokens, and connection strings before printing an environment or config dump — print the name and whether it is set, never the value; keep the instrumentation in place until the fix is verified, then strip it in the ferris-audit pre-commit pass.

## Bisect when the trigger is unknown

When something breaks and the causing change or test is unknown, bisect instead of staring: `git bisect run <check>` over history; halve the test set (or run tests one by one) when a test pollutes shared state; toggle config groups in halves when a setting is suspected. Each round must end with the harness saying pass or fail — bisection on vibes converges on nothing.

## Flaky and timing-dependent failures

A test that needs a sleep to pass documents a race. Replace every arbitrary sleep with condition polling: wait for the observable state change (file exists, port accepts, element rendered, promise settled, queue drained) with a hard timeout, then assert. When flakiness persists, find which ordering promise is missing — who publishes the state, who consumes it, and what guarantees the order — instead of widening the sleep. Reproduce races deliberately by tightening the window: run the suite under load, in parallel, or with the suspicious delay forced to zero.
