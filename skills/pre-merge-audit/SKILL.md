---
name: pre-merge-audit
description: ALWAYS use this skill BEFORE ANY git commit, push, merge, or PR submission — a MANDATORY pre-commit pass that tidies and gates the staged diff, even when the user does not ask for a review. Also use whenever the user asks to review, audit, or scrutinize changes — "review this branch", "audit this PR", "deep review", "strict review", "code quality audit" — even when phrased casually, or to clean up beyond the current diff — "clean this up before we commit", "remove the dead code". No exception for trivial or single-file commits; only formatting-only changes may skip.
---

# Pre-Merge Audit

Three tiers, escalating by frequency and authority:

1. **Pre-commit pass (automatic, every commit)** — tidy and gate the staged diff. May edit, but only within code the current change adds or modifies.
2. **Deep audit (on request or escalation)** — exhaustive review of a branch, PR, MR, or diff: correctness & security, then structure & maintainability. Read-only.
3. **Deep cleanup (explicit intent only)** — deep audit first, then proven cuts anywhere in scope per `references/cleanup.md`, then re-audit.

Be extremely thorough, rigorous, careful, and attentive. Measure twice, cut once. Let nothing real slip through — but never invent or inflate findings to look busy.

## Pre-commit pass

Mandatory before EVERY commit, push, merge, or PR submission — even when nobody asks for a review, and even for trivial or single-file changes. Only formatting-only changes may skip. Never commit unaudited changes.

1. Tidy the staged diff: remove dead code the diff introduces, obvious duplication within it, and leftover debris (commented-out code, unused imports/variables, debug output).
2. Cut only what the diff itself added or modified, and only with proof: no production consumers, unreachable, no behavior contract touched. Anything reaching beyond the diff is deep cleanup, not this pass.
3. Run the smallest targeted checks covering the change (typecheck, lint, touched tests).
4. Gate the final diff for obvious correctness and security bugs and breaking changes.
5. Report what was cleaned and the verdict; the user still owns the commit itself.

Zero cuts is a valid outcome; never force a deletion to look productive.

## Escalation

- Pre-commit pass → deep audit, automatically, when the pass finds medium-or-higher findings or the change is high-stakes: large diff, public API or contract change, auth/payment/security-sensitive path, release commit.
- Deep audit → deep cleanup only on explicit user intent; never escalate into edits on your own.

## Scope

- Report only issues in code the diff ADDS or MODIFIES, plus side effects traced into existing call sites. Pre-existing problems in untouched code only when the change compounds them.
- Not an issue: behavior that is the branch's evident, well-constrained intent. Do report it if the author likely doesn't grasp the implications, under-weights the negatives, or the change looks malicious.
- Deep audit never edits; the pass and deep cleanup edit only as their tier defines. Never commit, push, publish, tag, release, or bump a version in any mode — the user owns every release action.

## Load references on demand

The full standards live beside this file. Read each reference right before the tier that needs it; skip any reference whose tier doesn't apply. The pre-commit pass needs none — its rules are inline above.

- `references/correctness-security.md` — before deep-audit Part 1: side-effect tracing discipline, bug hunting, security vulnerabilities, DX breakage, feature-gate leaks.
- `references/structure-maintainability.md` — before deep-audit Part 2: structural ambition, non-negotiable standards (1000-line threshold, tangled growth, abstraction and boundary cleanliness), review questions, aggressive flags, preferred remedies, tone, and the approval bar.
- `references/cleanup.md` — before any deep-cleanup edit: deletion-proof requirements (consumers, reachability, ownership, boundaries), hunt list, protected surfaces, applying cuts, and the cleanup report format.

## Process

1. Deep audit: run Parts 1 and 2 completely, with fresh eyes, BEFORE looking at any PR/MR discussion — this keeps the review unbiased.
2. With medium-to-high findings and a PR/MR, check its discussion via gh/glab CLI. If bots or reviewers found issues you missed, evaluate, include the valid ones, and credit them.
3. Deep cleanup: audit first, then apply proven cuts per `references/cleanup.md`, then re-run Parts 1 and 2 over the cleanup diff.

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
