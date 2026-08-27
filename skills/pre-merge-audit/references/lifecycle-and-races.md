# Lifecycle and Races

Read this whenever a candidate touches concurrency, cancellation, resource cleanup, defensive copies, or state crossing a process, trust, or lifetime boundary. Deleting the wrong guard here fails late, intermittently, and in production.

## Owned vs borrowed boundaries

For every validator, copy, freeze, retry, rollback, or containment layer, identify where the value came from, who owns it now, who may mutate it next, how long it lives, and what failure it defends against.

Defense on an owned boundary — untrusted input, config parsing, external payloads, queues, storage, protocols, plugins, workers, subprocesses, anything crossing an asynchronous lifetime boundary — is part of the contract; never remove it as incidental cleanup. Defense on a borrowed handoff — a private call whose types and ownership conventions one component already enforces — may be removable, but tests built on hostile fixtures or fake values prove only that someone assumed a contract. Confirm production actually promises that contract before deleting either the defense or its tests.

## Map the lifecycle

List every actor that can create, start, settle, cancel, stop, flush, or dispose the resource. Then map every flag, promise, queue, sentinel, callback, and controller to: the owner that writes it, the readers deciding from it, the transition it represents, the race or failure it prevents, and the cleanup guarantee it completes.

Two mechanisms are redundant only when they cover the same transition for the same owner across the same failure window — similar names prove nothing. Keep mechanisms that separately guarantee atomic publish-and-rollback, isolate callback failures, arbitrate competing terminal outcomes, own a worker or process, or bridge different durability levels. When several truly encode one fact, keep the representation already trusted at the strongest boundary and route other readers to it, instead of adding a coordinator that leaves both alive.

## Quiescence means nothing left in flight

Returning from `dispose` or setting a stopped flag is not completion. Establish that no owned task can publish, mutate durable state, retain resources, or fire callbacks after the terminal boundary. Check timers, event listeners, streams, child processes, pending promises, queues, retries, abort handlers, and deferred writes — and name the specific check that would expose a late effect.

## Model races before cutting

For asynchronous candidates, write the event table — transition, owner, allowed predecessors, terminal effect, late-event behavior — and exercise at least: the normal path, cancellation before start, cancellation mid-work, competing terminal outcomes, partial publication failure, and repeated cleanup, whenever those states are reachable. Remove a branch only after its ordering guarantee exists elsewhere or is proven unnecessary.
