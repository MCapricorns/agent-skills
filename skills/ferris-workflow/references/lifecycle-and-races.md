# Lifecycle and Races

Use before consolidating guards, defensive copies, cancellation, cleanup, or cross-boundary state.

## Same-looking state can enforce different guarantees

For each validator, copy, retry, rollback, or wrapper, name the failure it prevents and the lifetime it covers. For each flag, queue, callback, or controller, name writers, readers, transitions, and cleanup. Hostile tests neither prove nor disprove a production contract.

Consolidate only when ownership, transitions, and failure guarantees match. Atomic publication, rollback, callback isolation, terminal-state arbitration, worker ownership, and durable completion are distinct. If state is redundant, keep the copy the strictest consumer trusts.

## Cancellation is not quiescence

`dispose`, abort, and stopped flags do not prove timers, listeners, streams, workers, promises, queued retries, or buffered writes have finished. Name what can still publish, persist, or call back after the terminal point.

Cut a branch only when its ordering guarantee survives elsewhere or has no consumer. Happy-path success does not prove canceled-before-start, mid-flight cancel, simultaneous endings, or repeated cleanup.
