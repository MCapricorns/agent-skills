# Lifecycle and Races

Use before consolidating guards, defensive copies, cancellation, cleanup, or cross-boundary state.

## Same-looking state can enforce different guarantees

For each validator, copy, retry, rollback, or containment wrapper, trace entry, subsequent mutation, lifetime, and the failure prevented. For each flag, promise, queue, callback, or controller, identify writers/readers, transitions, failure windows, and cleanup obligations. Hostile test inputs alone neither establish nor disprove a production contract.

Consolidate only when ownership, transitions, and failure guarantees match and survive elsewhere. Atomic publication, rollback, callback isolation, terminal-state arbitration, worker ownership, and durable completion are distinct. If state is truly redundant, retain the source the strictest consumer trusts rather than coordinating two copies.

## Cancellation is not quiescence

Trace resources from creation through cancellation and release. `dispose`, abort requests, and stopped flags do not prove that timers, listeners, streams, workers/subprocesses, promises, queued retries, or buffered writes have finished. Identify what can still publish, persist, hold resources, or invoke caller code after the terminal point, and the observation that would catch it.

Exercise transitions with their driver, precondition, outcome, and late-event handling: canceled-before-start, mid-flight cancellation, simultaneous endings, partial publication, and repeated cleanup. Cut a branch only when its ordering guarantee survives elsewhere or has no consumer; happy-path success cannot prove these orderings.
