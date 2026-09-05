# Cleanup and Deletion Proof

For explicit cleanup or a read-only audit, not routine diff hygiene. Cleanup permits proven in-scope cuts without per-item approval; an audit permits no edits.

## Before a cut

- **Reachability:** classify consumers as production, support-only, or unresolved. Check entrypoints, configuration, registration/reflection, codegen, string dispatch, external callers, and persisted keys where applicable. Tests/examples may document public contracts; neither empty searches nor green tests prove absence of consumers. Unresolved reachability blocks deletion.
- **Contract/history:** read callers and decision rationale. Compare ownership, behavior, ordering, errors, and side effects, not textual similarity; quiet history is not disuse. Name the behavior being surrendered and a runnable check that would expose a mistaken cut.
- **Protected surfaces:** do not remove security controls, trust-boundary validation, accessibility, data-loss protection, durable compatibility, public APIs, or resource-quiescence cleanup without explicit approval. Generated/vendor files, fixtures, and migrations are not ordinary dead code. Keep and explain anything with a surviving consumer/rationale or unresolved product decision.

## Simplify the owning layer

Prefer deletion, then a canonical helper/platform facility. Consolidate only matching contracts and ownership; retain intentional differences without weakening types, errors, ordering, performance, or security. Remove forwarding-only/speculative layers, not move their complexity behind another coordinator. Keep feature logic in its owner and split coherent modules before 1000 lines.

Orchestration changes need understood independence, atomicity, ordering, and failure behavior. For lifecycle guards or state, apply the lifecycle reference linked from SKILL.md. Propose cross-ownership or public-contract changes rather than expanding scope silently.

## Finish the cut

Remove obsolete declarations, implementation, callers, config/exports/dependencies, dedicated tests, and affected docs/inventories together. Preserve coverage of surviving behavior. Carry still-useful design rationale/rejected alternatives into successor records, repair links, and leave immutable history intact.

Revalidate imported findings and the integrated diff. Re-search removed names/stale docs, run decisive checks and relevant repository gates, and repair or revert failing batches rather than weakening checks. Report contracts removed, measured reduction, tradeoffs, checks, blockers, and uncovered scope; audits distinguish confidence from benefit and name missing evidence. Persisted-data or shipped-artifact changes need an explicit recovery procedure; a Git diff only reverses code. Deletion volume is not a quality score.
