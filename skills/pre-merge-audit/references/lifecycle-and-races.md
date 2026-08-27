# Lifecycle and Races

Read this whenever a candidate touches concurrency, cancellation, resource cleanup, defensive copies, or state crossing a process, trust, or lifetime boundary. Guards deleted here tend to fail late, intermittently, and only in production.

## Whose boundary is the guard standing on?

Every validator, defensive copy, freeze, retry, rollback, and containment wrapper pays for itself only where ownership actually changes hands. Before cutting one, answer in this order: What kind of defense is this? Where did the value enter from? Who may mutate it next, and until when? Which failure slips through without it?

A guard standing on a real handoff — untrusted input, parsed config, external payloads, queues, storage, protocol traffic, plugins, workers, subprocesses, anything passed across an asynchronous lifetime boundary — is contract, not clutter; leave it alone. A guard inside one component, on a private call whose types and conventions that component already enforces, can often go. Careful: tests that hammer such a guard with hostile fixtures only record what some author assumed. Check whether production ever promised that behavior before deleting the guard or its tests.

## Follow the state to its owners

Trace the resource end to end: who spins it up, who may end it, who waits on it, who tears it down or releases it. Then take each synchronization token in turn — status flags, promises, queues, sentinels, callbacks, controllers — and pin down who writes it, who reads it to decide, which transition it stands for, what race it exists to prevent, and what cleanup it finishes.

Never merge two mechanisms on resemblance. They are duplicates only if one owner, one transition, and one failure window would go unguarded after the merge. Mechanisms that each carry a distinct guarantee stay: one publishes atomically while another rolls back; one isolates callback failures; one referees dueling terminal states; one owns a worker; one bridges volatile to durable. When several tokens really do carry one fact, standardize on whichever the harshest consumer already trusts, point the remaining readers at it, and delete the rest — do not add a coordinator that keeps every copy breathing.

## Finished is not the same as stopped

A returned `dispose` call or a set `stopped` flag says nothing about what is still in flight. Two questions close the gap:

- What could still act after the terminal point — publish, write durable state, hold a resource, call back into caller code? Sweep for timers, listener registrations, open streams, child processes, unresolved promises, queued work, retry arms, abort paths, buffered writes.
- Which observation would catch a straggler if one existed? Name it before you cut.

## Rehearse the orderings you are about to delete

For an asynchronous candidate, tabulate the transitions you plan to touch: who drives each one, what must have happened before it may run, what it leaves behind when it lands, and what becomes of events arriving after it. Then rehearse the awkward orders — canceled before it began, canceled halfway, two endings arriving together, a publish that half-landed, cleanup running twice. Drop a branch only once its ordering promise lives on somewhere else, or once nothing depends on it.
