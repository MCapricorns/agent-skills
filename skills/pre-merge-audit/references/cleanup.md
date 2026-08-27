# Deep Cleanup

Read this before any cleanup edit that reaches beyond the current diff's inline rules — only when the user explicitly authorized deep cleanup. The automatic pre-commit pass uses only its inline diff-scoped rules in SKILL.md.

A cleanup request — "clean this up before we commit", "remove the dead code", "dedupe and simplify, then submit" — authorizes applying every safe, proven, in-scope cut end to end, without per-item approval. Do not stop at a candidate list when a safe cut is available. Finding no safe cut and making zero edits is a valid outcome; never force a deletion to look productive.

## A candidate is not a deletion

Static tools, search counts, apparent duplication, and earlier reconnaissance only produce leads. Re-read load-bearing files and repeat the decisive searches yourself; never inherit deletion proof from a prior report. Remove code only after proving all of:

- **Consumers** — real production consumers, distinguished from support-only references and ambiguous dynamic/plugin/reflection/codegen entrypoints. Search symbols, paths, strings, alternate call forms, docs, tests, and package metadata.
- **Reachability** — traced through entrypoints, configuration, registries, dynamic imports, dependency injection, events, queues, persistence, processes, and protocols. Start from central production surfaces, not isolated unused-looking symbols.
- **Ownership & history** — who creates, mutates, cancels, disposes, and observes each piece of state; the commit and decision history still explains why the code exists.
- **Boundaries** — generated, vendored, fixture, migration, and published surfaces are out of bounds.

Keep a candidate when a real consumer exists, dynamic reachability is unresolved, the original rationale still holds, the complexity merely moves elsewhere, or the cut is actually a product/API decision. State what behavior the cut gives up, even when the answer is "nothing observable".

## Hunt list

Dead exports, symbols, and config; unconsumed APIs; duplicate or near-repeated implementations (compare observable contracts, invariants, ordering, failure handling, and side effects — not text similarity); duplicate facts or lifecycle state; speculative abstractions; forwarding-only layers; abandoned compatibility residue; and hand-rolled infrastructure the platform or an installed dependency already provides.

## Protected surfaces

Never remove authorization, validation at trust boundaries, security controls, accessibility basics, data-loss protection, durable-data compatibility, public contracts, or resource-quiescence cleanup without explicit approval. If a cut would remove a user capability, public API, persisted format, wire contract, or compatibility path, keep it and report the tradeoff.

## Apply proven cuts

- Work within one ownership boundary at a time; keep batches reviewable.
- Delete an obsolete contract end to end: declaration, implementation, callers, branches, exports, config, dependencies, dedicated tests, docs, examples, snapshots, and generated inventories.
- For proven duplication, extract the smallest stable shared function, type, or module — preferring an existing canonical helper over a new framework — migrate every in-scope caller, and remove the superseded copies. Keep duplication when the copies belong to different domain boundaries, intentionally differ in semantics, are likely to evolve independently, or cannot be unified without weakening types, errors, ordering, performance, security, or readability; state the concrete reason. Preserve tests for each surviving observable boundary and add focused shared-contract coverage when the extraction creates a new reusable unit.
- Synchronize every README, doc, example, API comment, and explanatory comment directly affected by the cleanup. Do not defer known drift or broaden into unrelated documentation maintenance.
- Re-search removed names and stale documentation. Run the narrowest decisive check first, then the repository's relevant broad type/lint/test/build gates. Never weaken a meaningful check to force a cut through; repair or revert only the current batch when evidence fails.
- Prefer net reduction: deletion first, then platform features, then dependencies already present. No replacement glue that erases the reduction.

## Report the cleanup

Re-verify the cleanup diff with the narrowest decisive checks, then the repository's relevant broad type/lint/test/build gates, and return only the outcome: exact files/contracts removed or consolidated, measurable net reduction, behavior tradeoffs, and checks actually run. Do not repeat the evidence-gathering chronology; report only unresolved blockers and still-failing checks. Never equate green tests with proof, or deletion volume with value.
