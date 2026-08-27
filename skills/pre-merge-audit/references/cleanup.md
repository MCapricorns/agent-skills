# Deep Cleanup

Read this before any cleanup edit that reaches beyond the current diff's inline rules — and read it as the proof standard for read-only surveys too. It applies when the user explicitly authorized deep cleanup; the automatic pre-commit pass uses only its inline diff-scoped rules in SKILL.md.

A cleanup request — "clean this up before we commit", "remove the dead code", "dedupe and simplify, then submit" — authorizes applying every safe, proven, in-scope cut end to end, without per-item approval. Do not stop at a candidate list when a safe cut is available. Finding no safe cut and making zero edits is a valid outcome; never force a deletion to look productive.

## A candidate is not a deletion

Static tools, search counts, apparent duplication, and earlier reconnaissance only produce leads. Re-read load-bearing files and repeat the decisive searches yourself; never inherit deletion proof from a prior report.

Proof climbs a ladder, and each rung must be earned in this session:

1. **Visible smell** — complexity or duplication someone noticed.
2. **Analyzer lead** — a search or tool reports no use.
3. **Classified references** — every hit triaged (below) and the relevant callers read.
4. **Contract resolved** — dynamic loading, persistence, compatibility, and decision history accounted for.
5. **Decisive check** — a runnable probe named that would fail if the cut were wrong.

Deleting on rungs one or two is how live code dies. High-confidence cuts normally need rung four plus the check from rung five.

Remove code only after proving all of:

- **Consumers** — every reference classified as production, support-only, or unresolved. Support-only (tests, docs, comments, snapshots, illustrative examples) is not a consumer. Unresolved (dynamic imports, plugin registration, reflection, codegen, string dispatch, persisted keys, external packages) blocks the cut until traced through registration, loading, and publication boundaries. Search symbols, paths, strings, alternate call forms, docs, tests, and package metadata.
- **Reachability** — traced through entrypoints, configuration, registries, dynamic imports, dependency injection, events, queues, persistence, processes, and protocols. Start from central production surfaces, not isolated unused-looking symbols.
- **Ownership & history** — who creates, mutates, cancels, disposes, and observes each piece of state; the commit and decision history still explains why the code exists. An old date or quiet file is a discovery hint, not evidence of dead weight.
- **Boundaries** — generated, vendored, fixture, migration, and published surfaces are out of bounds.

Keep a candidate when a real consumer exists, dynamic reachability is unresolved, the original rationale still holds, the complexity merely moves elsewhere, or the cut is actually a product/API decision. State what behavior the cut gives up, even when the answer is "nothing observable".

## Hunt list

Dead exports, symbols, and config; unconsumed APIs; duplicate or near-repeated implementations (compare observable contracts, invariants, ordering, failure handling, and side effects — not text similarity); duplicate facts or lifecycle state; speculative abstractions; forwarding-only layers; abandoned compatibility residue; feature outlines left behind where an implementation was already removed (schema, config, tests, or docs preserving a ghost); and hand-rolled infrastructure the platform or an installed dependency already provides.

## Protected surfaces

Never remove authorization, validation at trust boundaries, security controls, accessibility basics, data-loss protection, durable-data compatibility, public contracts, or resource-quiescence cleanup without explicit approval. If a cut would remove a user capability, public API, persisted format, wire contract, or compatibility path, keep it and report the tradeoff.

## Apply proven cuts

- Inspect `git status` first; preserve unrelated worktree changes.
- Work within one ownership boundary at a time; keep batches reviewable.
- Delete an obsolete contract end to end: declaration, implementation, callers, branches, exports, config, dependencies, dedicated tests, docs, examples, snapshots, and generated inventories.
- For proven duplication, extract the smallest stable shared function, type, or module — preferring an existing canonical helper over a new framework — migrate every in-scope caller, and remove the superseded copies. Keep duplication when the copies belong to different domain boundaries, intentionally differ in semantics, are likely to evolve independently, or cannot be unified without weakening types, errors, ordering, performance, security, or readability; state the concrete reason. Preserve tests for each surviving observable boundary and add focused shared-contract coverage when the extraction creates a new reusable unit.
- When several mechanisms appear to guard the same transition, keep the representation already trusted at the strongest boundary and route other readers to it — but only after `references/lifecycle-and-races.md` shows they truly cover the same owner, transition, and failure window.
- Synchronize every README, doc, example, API comment, and explanatory comment directly affected by the cleanup. Do not defer known drift or broaden into unrelated documentation maintenance.
- Re-search removed names and stale documentation. Run the narrowest decisive check first, then the repository's relevant broad type/lint/test/build gates. Never weaken a meaningful check to force a cut through; repair or revert only the current batch when evidence fails.
- Prefer net reduction: deletion first, then platform features, then dependencies already present. No replacement glue that erases the reduction.

## Design records

When a cut invalidates an ADR, RFC, or design note, move its still-unique rationale — remembered rejected alternatives, why the original motivation no longer wins — into the record that now owns the decision, then repair inbound links, indexes, and paired references. Never rewrite frozen history; update owners and links instead. Keep the record alive when the capability survives through another delivery route or its warning still prevents a recurring mistake. A cleanup is not a documentation purge — touch only records the cut actually displaced, and keep speculative questions in the report rather than as scattered TODOs.

## Findings from elsewhere

Before applying a candidate inherited from another branch, PR, issue, or agent run, re-prove it against the current HEAD: consumers, reachability, and history may have moved. Map each imported finding to apply, merge into the thread that owns the contract, or reject with a reason, and keep the strongest counterargument over the raw count. Results validated on an isolated branch do not prove the combined tree — re-run the residue searches and decisive checks after merging.

## Report the cleanup

Re-verify the cleanup diff with the narrowest decisive checks, then the repository's relevant broad type/lint/test/build gates, and return only the outcome: exact files/contracts removed or consolidated, measurable net reduction, behavior tradeoffs, checks actually run, and how to undo — source-only cuts reverse from the diff, while anything touching migrations, durable data, or published artifacts must name explicit restoration steps. Do not repeat the evidence-gathering chronology; report only unresolved blockers and still-failing checks. Never equate green tests with proof, or deletion volume with value.
