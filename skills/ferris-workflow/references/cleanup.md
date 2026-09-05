# Cleanup and Deletion Proof

For explicit cleanup or a read-only audit, not routine diff hygiene. Cleanup may cut proven in-scope dead code without per-item approval; an audit makes no edits.

## Before a cut

- **Reachability:** classify consumers as production, support-only, or unresolved. Check entrypoints, configuration, registration/reflection, codegen, string dispatch, external callers, and persisted keys where they apply. Tests and examples may document public contracts. Neither an empty search nor a green suite proves there are no consumers. Unresolved reachability blocks deletion.
- **Contract:** compare ownership, behavior, ordering, errors, and side effects, not textual similarity. Quiet history is not disuse. Name the behavior being surrendered and a check that would expose a mistaken cut.
- **Protected surfaces:** do not remove security controls, trust-boundary validation, accessibility, data-loss protection, durable compatibility, public APIs, or resource-quiescence cleanup without explicit approval. Generated/vendor files, fixtures, and migrations are not ordinary dead code.

## Simplify the owning layer

Prefer deletion, then a canonical helper. Consolidate only matching contracts; keep feature logic in its owner. Split a module before 1000 lines. Do not move complexity behind another coordinator.

Orchestration changes need understood independence, atomicity, ordering, and failure behavior. Lifecycle guards belong in the lifecycle reference.

## Finish the cut

Remove declarations, implementation, callers, config/exports/dependencies, dedicated tests, and affected docs together. Preserve coverage of surviving behavior. Leave immutable history intact.

Re-search removed names. Run the checks that would catch a bad cut; repair or revert rather than weakening them. Persisted-data or shipped-artifact changes need a recovery path; a Git diff only reverses code.
