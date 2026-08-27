---
name: pre-merge-audit
description: Exhaustive pre-merge audit of a branch, PR, MR, or diff — correctness and security bugs, breaking changes, developer-experience regressions, feature-gate leaks, and structural code quality (oversized files, tangled branching, weak abstractions, missed simplifications). With explicit cleanup intent before committing, also proves and applies safe dead-code, duplication, and complexity removal. Use whenever the user asks to review, audit, clean up, or scrutinize changes before merging or committing — "review this branch", "audit this PR", "clean this up before we commit", "deep review", "strict review", "code quality audit" — even when phrased casually. Skip single-file quick questions, pure formatting, and lightweight style nitpicks.
---

# Pre-Merge Audit

A single-pass, maximum-rigor review of a checked-out branch. Every run audits two dimensions:

1. **Correctness & security** — does the change break things or open holes?
2. **Structure & maintainability** — even if it works, is it the right shape?

When the user explicitly authorizes cleanup before committing, a third pass applies proven dead-code, duplication, and complexity cuts.

Be extremely thorough, rigorous, careful, and attentive. Measure twice, cut once. Let nothing real slip through — but never invent or inflate findings to look busy.

## Scope

- Report only issues in code the diff ADDS or MODIFIES, plus side effects traced into existing call sites. Pre-existing problems in untouched code only when the change compounds them.
- Not an issue: behavior that is the branch's evident, well-constrained intent. Do report it if the author likely doesn't grasp the implications, under-weights the negatives, or the change looks malicious.
- Never edit during audit; never commit, push, publish, tag, release, or bump a version in any mode — the user owns every release action.

## Modes

- **Audit (default)** — read-only. Produce prioritized findings and an approval verdict.
- **Cleanup (only with explicit cleanup intent: "clean this up before we commit", "remove the dead code", "dedupe and simplify, then submit")** — authorization to apply every safe, proven, in-scope cut end to end without per-item approval. Do not stop at a candidate list when a safe cut is available. Zero edits is a valid outcome; never force a deletion to look productive.

## Load references on demand

The full standards live beside this file. Read each reference right before the pass that needs it; skip any reference whose pass doesn't apply.

- `references/correctness-security.md` — before Part 1: side-effect tracing discipline, bug hunting, security vulnerabilities, DX breakage, feature-gate leaks.
- `references/structure-maintainability.md` — before Part 2: structural ambition, non-negotiable standards (1000-line threshold, tangled growth, abstraction and boundary cleanliness), review questions, aggressive flags, preferred remedies, tone, and the approval bar.
- `references/cleanup.md` — before any cleanup edit only: deletion-proof requirements (consumers, reachability, ownership, boundaries), hunt list, protected surfaces, applying cuts, and the cleanup report format.

## Process

1. Run Parts 1 and 2 completely, with fresh eyes, BEFORE looking at any PR/MR discussion — this keeps the review unbiased.
2. With medium-to-high findings and a PR/MR, check its discussion via gh/glab CLI. If bots or reviewers found issues you missed, evaluate, include the valid ones, and credit them.
3. Cleanup mode: audit first, then apply proven cuts per `references/cleanup.md`, then re-run Parts 1 and 2 over the cleanup diff.

## Output priorities

1. Security and correctness bugs
2. Breaking changes to existing functionality
3. Structural quality regressions
4. Missed opportunities for dramatic simplification
5. Tangled-control-flow and branching growth
6. Boundary, abstraction, and type-contract problems
7. File-size, modularity, and legibility concerns

Cleanup runs additionally report: exact files/contracts removed or consolidated, measurable net reduction, behavior tradeoffs, and checks actually run. No evidence-gathering chronology; only unresolved blockers and still-failing checks.

## Honesty rules (every mode)

- NEVER present an issue with unfinished research — check the other side yourself before reporting.
- NEVER misreport priority; a few high-conviction findings beat a long list of cosmetic notes.
- NEVER equate green tests with proof, or deletion volume with value.

## Approval bar (audit mode)

Approve only when ALL hold: no structural regression; no visible missed dramatic simplification; no unjustified file-size explosion; no tangled special-case growth; no hacky or magical abstraction; no wrapper/cast/optionality churn; no architecture-boundary leak or canonical-helper duplication; no obvious decomposition missed. The presumptive blockers and full bar live in `references/structure-maintainability.md`.
