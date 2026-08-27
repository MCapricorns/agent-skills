# Part 2 — Structure & Maintainability

Read this before the structure pass of every audit run, and again before issuing the approval verdict.

Above all, be **ambitious** about code structure. Do not merely identify local cleanup opportunities — actively hunt for high-leverage restructurings: changes that preserve behavior while making the implementation dramatically simpler, smaller, more direct, and more elegant.

Baseline for this half:

> Perform a deep quality audit of the current branch's changes.
> Rethink how to structure and implement the changes to meaningfully improve quality without impacting behavior.
> Improve abstractions, modularity, and legibility; reduce tangled control flow.
> Be ambitious: if there is a clear path that involves restructuring part of the codebase, take it.
> Measure twice, cut once.

## Non-negotiable standards

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

## Primary review questions

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

## What to flag aggressively

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

## Preferred remedies

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
