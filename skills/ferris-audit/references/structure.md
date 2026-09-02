# Structural Bloat — Red Lines and Targets

Read this during deep cleanup and read-only surveys to hunt complexity beyond literal dead code — both what the change adds and high-leverage restructurings. The automatic pre-commit pass never loads this file: it stays within the diff-scoped rules in SKILL.md. In a survey these targets are leads to report, never edits. Above all, be ambitious: do not stop at "this could be a bit cleaner" — look for restructurings that preserve behavior while deleting whole categories of complexity, making the code look obvious in retrospect. Prefer deleting complexity over rearranging it; a refactor that moves the same mess to a new file is not a cut, and neither is a wrapper that hides rather than removes it.

## Red lines

1. **1000-line files.** Do not push a file from under 1000 lines to over 1000 without a very strong reason; treat crossing the threshold as a strong quality smell. Prefer extracting helpers, subcomponents, or modules. Waive only with a compelling structural reason AND a clearly organized result.
2. **No tangled growth.** New ad-hoc conditionals, scattered special cases, one-off branches, or narrow edge-case handling dropped into the middle of an already busy function are a design problem, not a stylistic nit. Push the logic into a dedicated abstraction, helper, state machine, policy object, or separate module.
3. **Clean the design, don't rubber-stamp working code.** If behavior can stay the same while structure becomes meaningfully cleaner, cut for the cleaner version. Prefer removing moving pieces over spreading the same complexity around.
4. **Direct, boring, maintainable over hacky or magical.** Treat brittle, ad-hoc, or "magic" behavior as a quality problem; be skeptical of generic mechanisms that hide simple data-shape assumptions; flag thin abstractions, identity wrappers, and pass-through helpers that add indirection without buying clarity.
5. **Type and boundary cleanliness.** Question unnecessary optionality, unchecked dynamic types (`any`, `unknown`, `void*`), and cast-heavy code when a clearer boundary could exist; prefer explicit typed models or shared contracts. If code silently falls back to paper over an unclear invariant, make the boundary explicit instead.
6. **Canonical layer and existing helpers.** Call out feature logic leaking into shared paths, or implementation details leaking through APIs; prefer existing canonical utilities over bespoke one-offs; push code toward the right package, service, or module.
7. **Orchestration smells.** Serialized independent work and non-atomic related updates are design smells when a cleaner structure is obvious; do not over-index on micro-optimizations — flag avoidable orchestration complexity that makes the implementation brittle.

Apply a restructuring when it is provably behavior-preserving and inside the requested scope; when it would change public contracts, cross module ownership, or exceed the brief, report it as a concrete proposal instead of applying it unilaterally.

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
