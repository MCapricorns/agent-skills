# Structural Bloat — Red Lines and Targets

Read this during deep cleanup and read-only surveys to hunt complexity beyond literal dead code — both what the change adds and high-leverage restructurings. The automatic pre-commit pass never loads this file: it stays within the diff-scoped rules in SKILL.md. In a survey these targets are leads to report, never edits. Above all, be ambitious: do not stop at "this could be a bit cleaner" — look for restructurings that preserve behavior while deleting whole categories of complexity, making the code look obvious in retrospect. Prefer deleting complexity over rearranging it; a refactor that moves the same mess to a new file is not a cut, and neither is a wrapper that hides rather than removes it.

## Red lines

0. **Be ambitious about structural simplification.** Assume a high-leverage move is usually available; if you see a path to delete complexity rather than rearrange it, push hard for that path.
1. **1000-line files.** Do not push a file from under 1000 lines to over 1000 without a very strong reason; treat crossing the threshold as a strong quality smell. Prefer extracting helpers, subcomponents, or modules. Waive only with a compelling structural reason AND a clearly organized result.
2. **No tangled growth.** New ad-hoc conditionals, scattered special cases, or one-off branches inserted into unrelated flows are a design problem, not a stylistic nit. Push the logic into a dedicated abstraction, helper, state machine, policy object, or separate module.
3. **Clean the design, don't rubber-stamp working code.** If behavior can stay the same while structure becomes meaningfully cleaner, cut for the cleaner version. Prefer removing moving pieces over spreading the same complexity around.
4. **Direct, boring, maintainable over hacky or magical.** Treat brittle, ad-hoc, or "magic" behavior as a quality problem; be skeptical of generic mechanisms that hide simple data-shape assumptions; flag thin abstractions, identity wrappers, and pass-through helpers that add indirection without buying clarity.
5. **Type and boundary cleanliness.** Question unnecessary optionality, unchecked dynamic types (`any`, `unknown`, `void*`), and cast-heavy code when a clearer boundary could exist; prefer explicit typed models or shared contracts. If code silently falls back to paper over an unclear invariant, make the boundary explicit instead.
6. **Canonical layer and existing helpers.** Call out feature logic leaking into shared paths, or implementation details leaking through APIs; prefer existing canonical utilities over bespoke one-offs; push code toward the right package, service, or module.
7. **Orchestration smells.** Serialized independent work and non-atomic related updates are design smells when a cleaner structure is obvious; do not over-index on micro-optimizations — flag avoidable orchestration complexity that makes the implementation brittle.

## Hunt restructurings that delete whole categories of complexity

- Reframe the state model so conditionals disappear instead of being centralized.
- Change the ownership boundary so the feature becomes a natural extension of an existing abstraction.
- Fold special cases into a simpler default flow with fewer exceptions.
- Un-serialize independent work when parallel is simpler and clearer.

Apply a restructuring when it is provably behavior-preserving and inside the requested scope; when it would change public contracts, cross module ownership, or exceed the brief, report it as a concrete proposal instead of applying it unilaterally.

## Flag aggressively

- A complicated implementation where a cleaner reframing could delete whole categories of complexity.
- Refactors that move code around without reducing the number of concepts a reader must hold.
- A file crossing 1000 lines due to this change, especially when the new code could be split out.
- New conditionals bolted onto unrelated code paths; one-off booleans, nullable modes, or flags complicating existing control flow.
- Feature-specific logic leaking into general-purpose modules.
- Generic "magic" handling that hides simple structure.
- Thin wrappers or identity abstractions that add indirection without simplifying anything.
- Unnecessary casts, unchecked dynamic types, or optional parameters that muddy the real contract.
- Copy-pasted logic instead of extracted helpers; bespoke helpers where a canonical utility already exists.
- Narrow edge-case handling inserted into the middle of an already busy function.
- Refactors that pass tests but make the code less modular or less readable; "temporary" branching likely to become permanent debt.
- Logic in the wrong layer or package when a clear canonical home exists.
- Sequential async flow where independent work would be simpler in parallel; partial-update logic leaving state less atomic than necessary.

## Preferred remedies

- Delete a whole layer of indirection rather than polishing it.
- Reframe the state model so conditionals disappear; turn special-case logic into a simpler default flow.
- Move the ownership boundary so the feature extends an existing abstraction naturally.
- Extract a helper or pure function; split a large file into focused modules.
- Replace condition chains with a typed model or explicit dispatcher; make type boundaries explicit so control flow gets simpler.
- Collapse duplicate branches into a single clearer flow; delete wrappers that do not meaningfully clarify the API.
- Reuse the canonical helper instead of a near-duplicate; move logic to the layer that already owns the concept.
- Separate orchestration from business logic; parallelize independent work when that also simplifies; restructure related updates into a more atomic flow.

Do not settle for a merely cleaner version of the same messy idea when a much simpler idea is plausibly reachable.
