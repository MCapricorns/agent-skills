---
name: pre-merge-audit
description: Exhaustive pre-merge audit of a branch, PR, MR, or diff — bugs, security vulnerabilities, breaking changes, developer-experience regressions, feature-gate leaks, and structural code quality (oversized files, tangled branching, weak abstractions, missed simplifications). Use whenever the user asks to review, audit, or scrutinize changes before merging — "review this branch", "audit this PR", "deep/harsh/strict review", "code quality audit" — even when phrased casually.
when_to_use: Trigger on any pre-merge review request — "review this branch/PR/diff", "audit these changes", "看看这个分支能不能合", "严格审查", "deep review", "code quality audit". Skip single-file quick questions, pure formatting, and lightweight style nitpicks.
---

# Pre-Merge Audit

A single-pass, maximum-rigor review of a checked-out branch. Every run audits two dimensions:

1. **Correctness & security** — does the change break things or open holes?
2. **Structure & maintainability** — even if it works, is it the right shape?

Be extremely thorough, rigorous, and attentive. Measure twice, cut once. Let no real defect slip through — but never invent or inflate findings to look busy.

## Scope

- Report only issues in code the diff ADDS or MODIFIES, plus side effects you traced into existing call sites.
- Do not report pre-existing problems in untouched code unless the change compounds them.
- Do not report an issue if the branch's evident, well-constrained intent is exactly that behavior (e.g. deliberately removing a feature flag). Do report it if the author likely does not grasp the full implications, is under-weighting the damage, or the change looks malicious.

## Part 1 — Correctness & Security

Trace every change end-to-end through cross-package and cross-module dependencies. Simple local edits often break distant functionality.

Hunt specifically for:

- **Bugs and logic errors** in the new or changed paths, including edge cases and error handling.
- **Security vulnerabilities** introduced by the change.
- **Developer-experience breakage** — changes to how or where secrets are read, environment variable renames or additions, port/network remaps, or new steps developers must perform for existing workflows to keep working. Adding a dependency through the normal package manager does NOT count; forcing a manual install outside the normal workflow does.
- **Feature-gate leaks** — features meant to stay behind feature flags or internal-only checks leaking out. These leaks are often subtle.

## Part 2 — Structure & Maintainability

Be ambitious. Do not merely collect local cleanups — hunt for high-leverage restructurings: changes that keep behavior identical while deleting whole categories of complexity, so the final shape looks obvious in retrospect. If a path exists to delete complexity rather than rearrange it, push hard for it.

Non-negotiable standards for the diff:

1. **1000-line ceiling.** A PR must not push a file from under 1000 lines to over it without a compelling structural reason and a clearly organized result. Otherwise demand decomposition first.
2. **No tangled growth.** Ad-hoc conditionals, one-off flags, and special cases bolted into unrelated flows are design problems, not style nits. Push the logic into a dedicated abstraction, helper, state machine, or module instead of tangling an existing path.
3. **Clean design beats "it works".** Never rubber-stamp an implementation that leaves the codebase messier. Prefer removing moving pieces altogether over refactors that spread the same complexity around.
4. **Direct and boring beats clever and magical.** Flag brittle ad-hoc behavior, generic mechanisms that hide simple data shapes, and thin wrappers or pass-through helpers that add indirection without clarity.
5. **Explicit contracts.** Question unnecessary casts, unchecked dynamic types (`any`, `unknown`, `void*`), stray optionality, and silent fallbacks papering over unclear invariants. Prefer explicit typed models and shared contracts.
6. **Canonical homes.** Feature logic must not leak into shared paths, nor implementation details leak through APIs. Reuse existing canonical helpers instead of near-duplicates; put logic in the layer or package that already owns the concept.
7. **Orchestration smells.** Flag needless serialization of independent work and non-atomic partial updates — but only when the cleaner structure is obvious; skip micro-optimization pedantry.

For every meaningful change, ask: Is there a restructuring that makes this dramatically simpler? Could the change be reframed so fewer concepts, branches, or helper layers are needed? Is the logic in the right file and layer? Do repeated conditionals signal a missing model or helper? Is the abstraction earning its keep, or is it just a wrapper?

## Honesty Rules

- NEVER present unfinished research. If you can check the other side yourself ("the client has issue X, but the backend probably handles it"), check it before reporting.
- NEVER misreport priority. Inflating findings to look thorough destroys trust over time. Trace issues end-to-end until you have complete confidence, then report the true severity.
- Prefer a small number of high-conviction findings over a long list of cosmetic notes when structural issues exist.

## Process

1. Run Parts 1 and 2 completely, with fresh eyes, BEFORE looking at any PR/MR discussion.
2. If you have medium-to-high findings and a PR/MR exists, check its discussion via the gh/glab CLI. If automated review bots or other reviewers found issues you missed, evaluate them, include the valid ones, and credit them in your report.

## Output

Order findings: security and breaking issues first, then structural regressions, then missed simplifications, then maintainability. For each finding give severity, evidence, and a concrete remedy — prefer remedies that delete complexity over ones that polish it.

## Approval Bar

Approve only when all of the following hold: no clear structural regression; no visible opportunity for a dramatic simplification missed; no unjustified file-size explosion; no tangled growth from special-case branching; no architecture-boundary leak or canonical-helper duplication; no clever abstraction obscuring the design. Mere behavioral correctness is not sufficient for approval.
