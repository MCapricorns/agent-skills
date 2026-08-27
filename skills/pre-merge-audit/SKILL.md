---
name: pre-merge-audit
description: Exhaustive pre-merge audit of a branch, PR, MR, or diff — bugs, security vulnerabilities, breaking changes, developer-experience regressions, feature-gate leaks, and structural code quality (oversized files, tangled branching, weak abstractions, missed simplifications). Use whenever the user asks to review, audit, or scrutinize changes before merging — "review this branch", "audit this PR", "deep/harsh/strict review", "code quality audit" — even when phrased casually.
when_to_use: Trigger on any pre-merge review request — "review this branch/PR/diff", "audit these changes", "看看这个分支能不能合", "严格审查", "deep review", "code quality audit". Skip single-file quick questions, pure formatting, and lightweight style nitpicks.
---

# Pre-Merge Audit

A single-pass, maximum-rigor review of a checked-out branch. Every run audits two dimensions:

1. **Correctness & security** — does the change break things or open holes?
2. **Structure & maintainability** — even if it works, is it the right shape?

Be extremely thorough, rigorous, careful, and attentive. Measure twice, cut once. Let nothing real slip through — but never invent or inflate findings to look busy.

## Scope

- Report only issues in code the diff ADDS or MODIFIES, plus side effects you traced into existing call sites.
- Do not report pre-existing problems in untouched code unless the change compounds them.
- Do not report an issue if the branch's evident, well-constrained intent is exactly that behavior (e.g. deliberately removing a feature flag or safeguard). Do report it if the author likely does not grasp the full implications, is under-weighting the negative impacts (extreme example: a PR bluntly titled "delete the database"), or the change looks malicious.

## Part 1 — Correctness & Security

### Trace side effects end-to-end

This is a complex codebase with many cross-package and cross-module dependencies. Simple local edits often break distant functionality. You MUST trace every change through its possible side effects before clearing it.

Hunt specifically for:

- **Bugs and logic errors** in the new or changed paths, including edge cases and error handling.
- **Security vulnerabilities** introduced by the change.
- **Developer-experience (DX) breakage.** It is easy to silently break how developers run or build the code locally. Examples (not exhaustive):
  - changing how secrets are read, or where they are read from
  - renaming or adding environment variables
  - remapping ports or networking
  - adding scripts that must be run for existing functionality to keep working

  Adding a dependency through the normal package manager does NOT count; forcing a manual install outside the normal workflow (a website, an app store) does.
- **Feature-gate leaks.** Features are often carefully gated behind feature flags or internal-only checks, and the leaks are usually subtle. Be very careful that nothing meant to stay gated leaks out.

## Part 2 — Structure & Maintainability

Above all, be **ambitious** about code structure. Do not merely identify local cleanup opportunities — actively hunt for high-leverage restructurings: changes that preserve behavior while making the implementation dramatically simpler, smaller, more direct, and more elegant.

Baseline for this half:

> Perform a deep quality audit of the current branch's changes.
> Rethink how to structure and implement the changes to meaningfully improve quality without impacting behavior.
> Improve abstractions, modularity, and legibility; reduce tangled control flow.
> Be ambitious: if there is a clear path that involves restructuring part of the codebase, take it.
> Measure twice, cut once.

### Non-negotiable standards

0. **Be ambitious about structural simplification.**
   - Do not stop at "this could be a bit cleaner."
   - Look for ways to reframe the change so whole branches, helpers, modes, conditionals, or layers disappear entirely.
   - Prefer the solution that makes the code look obvious in retrospect.
   - Assume a high-leverage move is usually available: a re-organization that uses the existing architecture more effectively.
   - If you see a path to delete complexity rather than rearrange it, push hard for that path.

1. **Do not let a PR push a file from under 1000 lines to over 1000 lines without a very strong reason.**
   - Treat crossing that threshold as a strong quality smell by default.
   - Prefer extracting helpers, subcomponents, modules, or local abstractions instead of letting a file sprawl.
   - If the diff crosses the threshold, explicitly ask whether the code should be decomposed first.
   - Waive only with a compelling structural reason AND a clearly organized result.

2. **Do not allow tangled growth in existing code.**
   - Be highly suspicious of new ad-hoc conditionals, scattered special cases, or one-off branches inserted into unrelated flows.
   - "Weird if statements in random places" is a design problem, not a stylistic nit.
   - Prefer pushing the logic into a dedicated abstraction, helper, state machine, policy object, or separate module.
   - Call out changes that make surrounding code harder to reason about, even when they technically work.

3. **Bias toward cleaning the design, not just accepting working code.**
   - If behavior can stay the same while structure becomes meaningfully cleaner, push for the cleaner version.
   - Do not rubber-stamp "it works" implementations that leave the codebase messier.
   - Strongly prefer simplifications that remove moving pieces over refactors that spread the same complexity around.

4. **Prefer direct, boring, maintainable code over hacky or magical code.**
   - Treat brittle, ad-hoc, or "magic" behavior as a quality problem.
   - Be skeptical of generic mechanisms that hide simple data-shape assumptions.
   - Flag thin abstractions, identity wrappers, and pass-through helpers that add indirection without buying clarity.

5. **Push hard on type and boundary cleanliness when it affects maintainability.**
   - Question unnecessary optionality, unchecked dynamic types (`any`, `unknown`, `void*`), and cast-heavy code when a clearer boundary could exist.
   - Prefer explicit typed models or shared contracts over loosely-shaped ad-hoc objects.
   - If the branch relies on silent fallback to paper over an unclear invariant, ask whether the boundary should be explicit instead.

6. **Keep logic in the canonical layer and reuse existing helpers.**
   - Call out feature logic leaking into shared paths, or implementation details leaking through APIs.
   - Prefer existing canonical utilities over bespoke one-offs.
   - Push code toward the right package, service, or module instead of normalizing architectural drift.

7. **Treat needless sequential orchestration and non-atomic updates as design smells when the cleaner structure is obvious.**
   - If independent work is serialized for no good reason, ask whether it should run in parallel.
   - If related updates can leave state half-applied, push for a more atomic structure.
   - Do not over-index on micro-optimizations; flag avoidable orchestration complexity that makes the implementation more brittle.

### Primary review questions

For every meaningful change, ask:

- Is there a high-leverage restructuring that would make this dramatically simpler?
- Can the change be reframed so fewer concepts, branches, or helper layers are needed?
- Does it improve or worsen the local architecture?
- Did the diff add branching complexity where a better abstraction should exist?
- Did a previously cohesive module become more coupled, more stateful, or harder to scan?
- Is this logic living in the right file and layer?
- Did the change enlarge a file or component past a healthy size boundary?
- Are there repeated conditionals that signal a missing model or missing helper?
- Is the implementation direct and legible, or does it rely on special cases and incidental control flow?
- Is this abstraction earning its keep, or is it just a wrapper?
- Did the diff introduce casts, optionality, or ad-hoc object shapes that obscure the real invariant?
- Is this logic in the canonical layer, or did details leak across a boundary?
- Is the orchestration more sequential or less atomic than it needs to be?

### What to flag aggressively

Escalate findings when you see:

- A complicated implementation where a cleaner reframing could delete whole categories of complexity.
- Refactors that move code around without reducing the number of concepts a reader must hold in their head.
- A file crossing 1000 lines due to this change, especially if the new code could be split out.
- New conditionals bolted onto unrelated code paths.
- One-off booleans, nullable modes, or flags that complicate existing control flow.
- Feature-specific logic leaking into general-purpose modules.
- Generic "magic" handling that hides simple structure.
- Thin wrappers or identity abstractions that add indirection without simplifying anything.
- Unnecessary casts, unchecked dynamic types, or optional parameters that muddy the real contract.
- Copy-pasted logic instead of extracted helpers.
- Narrow edge-case handling inserted into the middle of an already busy function.
- Refactors that technically pass tests but make the code less modular or less readable.
- "Temporary" branching that is likely to become permanent debt.
- Bespoke helpers where the codebase already has a canonical utility for the job.
- Logic added in the wrong layer or package when it should live somewhere more central.
- Sequential async flow where obviously independent work would be simpler and clearer in parallel.
- Partial-update logic that leaves state less atomic than necessary.

### Preferred remedies

When you identify a structural problem, prefer suggestions like:

- Delete a whole layer of indirection rather than polishing it.
- Reframe the state model so conditionals disappear instead of being centralized.
- Change the ownership boundary so the feature becomes a natural extension of an existing abstraction.
- Turn special-case logic into a simpler default flow with fewer exceptions.
- Extract a helper or pure function.
- Split a large file into smaller focused modules.
- Move feature-specific logic behind a dedicated abstraction.
- Replace condition chains with a typed model or explicit dispatcher.
- Separate orchestration from business logic.
- Collapse duplicate branches into a single clearer flow.
- Delete wrappers that do not meaningfully clarify the API.
- Reuse the existing canonical helper instead of introducing a near-duplicate.
- Make type boundaries more explicit so the control flow gets simpler.
- Move logic to the package, module, or layer that already owns the concept.
- Parallelize independent work when that also simplifies orchestration.
- Restructure related updates into a more atomic flow when partial state is harder to reason about.

Do not settle for "maybe rename this" feedback when the real issue is structural.
Do not settle for a merely cleaner version of the same messy idea when a much simpler idea is plausibly reachable.

## Honesty rules

- NEVER present an issue with unfinished research. If you can check the other side yourself ("the client has issue X, but the backend probably handles it"), check before reporting.
- NEVER misreport priority. Inflating findings to look thorough makes developers stop trusting the review. Trace issues end-to-end until you have complete confidence, then report the true severity.
- Prefer a small number of high-conviction findings over a long list of cosmetic notes when structural issues exist.

## Tone

Be direct, serious, and demanding about quality. Do not be rude, but do not soften major issues into mild suggestions. If the code makes the codebase messier, say so plainly. If the implementation missed an opportunity for a dramatic simplification, say that plainly too.

Useful phrasings:

- "This pushes the file past 1000 lines. Can we decompose it first?"
- "This adds another special-case branch to an already busy flow. Can we move it behind its own abstraction?"
- "This works, but it makes the surrounding code harder to follow. Keep the behavior, restructure the implementation."
- "This looks like feature logic leaking into a shared path. Can we isolate it?"
- "This abstraction seems unnecessary. Can we keep the direct flow?"
- "Why does this need a cast or optional here? Can we make the boundary explicit instead?"
- "This looks like a bespoke helper for something we already have. Can we reuse the canonical one?"
- "I think there's a move here that makes this much simpler. Can we reframe it so these branches disappear?"
- "This refactor moves complexity around but doesn't delete it. Is there a way to make the model itself simpler?"

## Process

1. Run Parts 1 and 2 completely, with fresh eyes, BEFORE looking at any PR/MR discussion. This keeps your review unbiased.
2. If you have medium-to-high findings and a PR/MR exists, check its discussion via the gh/glab CLI. If automated review bots or other reviewers found issues you missed, evaluate them, include the valid ones, and credit them in your report. If they found the same issues you did, incorporate anything their findings add to yours.

## Output expectations

Prioritize findings in this order:

1. Security and correctness bugs
2. Breaking changes to existing functionality
3. Structural quality regressions
4. Missed opportunities for dramatic simplification
5. Tangled-control-flow and branching growth
6. Boundary, abstraction, and type-contract problems
7. File-size, modularity, and legibility concerns

Do not flood the review with low-value nits while larger structural issues exist.

## Approval bar

Do not approve merely because behavior seems correct. Approve only when ALL of the following hold:

- no clear structural regression
- no visible opportunity missed to make the implementation dramatically simpler
- no unjustified file-size explosion
- no tangled growth from special-case branching
- no hacky or magical abstraction obscuring the design
- no unnecessary wrapper, cast, or optionality churn obscuring the real design
- no architecture-boundary leak or canonical-helper duplication
- no obvious decomposition missed that would materially improve maintainability

Treat these as presumptive blockers unless the author can clearly justify them:

- the change preserves a lot of incidental complexity when a plausible restructure would delete it
- the change pushes a file from below 1000 lines to above it
- the change adds ad-hoc branching that tangles an existing flow
- the change solves a local problem by scattering feature checks across shared code
- the change adds an unnecessary abstraction, wrapper, or cast-heavy contract that makes the design more indirect
- the change duplicates an existing helper or puts logic in the wrong layer when a clear canonical home exists

If any bar is unmet, leave explicit, actionable feedback and push for a cleaner decomposition.
