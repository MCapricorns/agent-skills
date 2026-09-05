# Cleanup and Simplification

Read for explicit cleanup or a read-only deletion audit, not the routine diff-local hygiene pass. A cleanup request authorizes proven in-scope cuts without per-item approval; a survey authorizes no edits. Inspect `git status` and preserve unrelated changes.

## Prove a cut

Search hits, analyzer warnings, and earlier reports are leads. Before deleting, establish all of:

1. **Consumers and reachability:** classify references as production, support-only, or unresolved. Tests and examples alone do not establish a production consumer, but may document a public contract. Trace entrypoints, configuration, registration, reflection, codegen, string dispatch, external packages, and persisted keys wherever applicable. Unresolved reachability blocks deletion.
2. **Contract and history:** read relevant callers and decision history; identify who creates, mutates, cancels, disposes, and observes the state. Compare behavior, ordering, errors, and side effects, not textual similarity. A quiet history is not proof of disuse.
3. **Decisive check:** name the behavior the cut gives up and a runnable check that would expose a mistaken cut. Resolve the contract first; passing tests alone cannot prove absence of consumers.

Never remove security controls, trust-boundary validation, accessibility, data-loss protection, durable-data compatibility, public APIs, or resource-quiescence cleanup without explicit approval. Generated, vendored, fixture, and migration surfaces are not ordinary dead-code targets. If the founding reason still stands, a consumer remains, or the cut is a product decision, keep it and report why.

## Remove complexity, not just lines

- Prefer deletion, then an existing canonical helper or platform facility. Remove dead switches, exports, configuration, dependencies, and docs when their implementation is already gone.
- Consolidate duplication only when contracts and ownership match. Keep copies that intentionally differ or evolve independently; do not weaken types, errors, ordering, performance, or security to unify them.
- Delete forwarding-only layers and speculative abstractions. Simplify the state model before introducing another helper, policy object, or coordinator.
- Keep feature logic in its owning layer and boundaries explicit. Split files before 1000 lines into coherent modules; do not move the same complexity behind a thin wrapper.
- Improve orchestration only where independence, atomicity, ordering, and failure behavior are understood. For lifecycle state or guards, use the lifecycle reference linked from SKILL.md before consolidating.

Apply behavior-preserving changes within scope. Propose cross-ownership or public-contract changes instead of silently expanding the task.

## Apply and verify

Work in reviewable batches. Remove each obsolete contract end to end: declaration, implementation, callers, config, exports, dedicated tests, docs, examples, and affected inventories. Preserve coverage for surviving observable boundaries. Synchronize directly affected comments and README text, not unrelated documentation.

If a cut displaces a design record, preserve still-useful rationale and rejected alternatives in its successor, repair links, and leave immutable history alone. Keep records whose rationale still applies.

Revalidate imported findings against the current code and inspect the integrated diff; isolated verification does not cover a merge. Re-search removed names and stale docs, then run decisive checks and the repository's relevant broader gates. Never weaken a meaningful check to force a cut through; repair or revert the failing batch.

Report removed/consolidated contracts, measurable reduction, behavior tradeoffs, checks run, and unresolved blockers. For surveys, separate confidence from benefit and name each missing fact and decisive check; disclose uncovered scope. Pure-code changes can be reversed from the diff; persisted-data or shipped-artifact changes need an explicit recovery procedure. Deletion volume is not a quality score.
