# Lifecycle and Races

Read before simplifying concurrency, cancellation, cleanup, defensive copies, or state crossing a trust, process, or lifetime boundary.

## Identify the guarantee

For each validator, copy, retry, rollback, or containment wrapper, identify where the value enters, who can mutate it next, how long it remains live, and which failure the guard prevents. A real handoff guarantee is contract, not clutter. Private duplication is removable only when the same guarantee is enforced elsewhere; hostile test inputs alone neither establish nor disprove a production contract.

Trace each resource from creation through cancellation and release. For every flag, promise, queue, callback, or controller, identify its writer, readers, transition, failure window, and cleanup obligation.

Two mechanisms are duplicates only when ownership, transition, and failure guarantees match and all guarantees survive consolidation. Atomic publication, rollback, callback isolation, terminal-state arbitration, worker ownership, and durable completion are different guarantees. When state really is redundant, retain the source the strictest consumer trusts rather than adding a coordinator that keeps both copies.

## Prove quiescence

A returned `dispose`, abort request, or `stopped` flag does not prove nothing remains in flight. Check timers, listeners, streams, workers/subprocesses, pending promises, queued work, retries, and buffered writes. What can still publish, persist data, hold a resource, or call caller code after the terminal point? Name the observation that would catch a straggler before cutting.

Map the affected transitions: driver, precondition, resulting state, and handling of late events. Exercise canceled-before-start, mid-flight cancellation, simultaneous endings, partial publication, and repeated cleanup. Remove a branch only when its ordering guarantee survives elsewhere or no consumer depends on it. A passing happy-path test is not evidence for these orderings.
