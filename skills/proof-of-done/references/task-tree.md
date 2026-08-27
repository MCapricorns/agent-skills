# Task Tree

Read this before splitting substantial work across parts, files, or subagents, and before dispatching any subagent.

## Find the real seams

The top of the tree is the request itself. Cut along real divisions — separate components, separate owners, or separate ways of verifying — never to satisfy a target count or depth. Each part must be a self-contained outcome: merge parts too small to stand alone, and split any part hiding two independently required outcomes. Pick the fewest parts that surface every stand-alone deliverable and every seam where separately built pieces must meet.

## Give every part a contract

Before any part starts, write down its side of the deal: which files it may touch, what it hands to and takes from its neighbors, which other parts must land first, what tools and directory it runs with, how it should behave when things fail, and which external shapes must stay compatible. Two concurrent parts must never own overlapping paths; when two parts must touch the same work, serialize them or promote the shared work to its own integration part.

Every part gets its own section in `ACCEPTANCE.md` (`## <part-name>`), and every branch that joins children gets integration items: rerun the children's checks, then exercise how the children connect — interfaces line up, the combined flow behaves, and nothing regressed. Local correctness does not imply composition.

## Delegating to subagents

A subagent brief must carry: the contract, the paths it owns, its acceptance items verbatim, and the rule that it reports evidence, not confidence. A returned "done" is a claim, not a result — rerun that part's runnable items yourself, review manual items directly, and attempt to break at least one passing item before accepting it. Record your rerun as the evidence; the subagent's own report is not.

## Completion climbs

Verify bottom-up, report only from the top. A part is done when its items hold current evidence; a branch is done when its children are re-verified and its integration items pass; the task is done only when the report audit in SKILL.md closes clean. A part with a waiver is not done — it is delivered-with-handoff, and that handoff must survive into the final report.

## When not to split

Keep the work in one pass whenever one working session can build and check the whole, with no independent outcome left implicit. Splitting carries its own coordination and reassembly cost; pay it only to protect focus, or for genuinely independent parts.
