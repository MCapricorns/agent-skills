# AGENTS.md

These files apply on every turn in that repository. Revisit each line and delete what the current models no longer need. Task-specific workflows belong in a skill, not here.

## Read what the task needs

- Bad: `Before every edit, read architecture.md, database.md, and deployment.md.`
- Good: `Use architecture.md for service boundaries, database.md for schema changes, and deployment.md when preparing a deployment.`

Do not require a repo map or a doc stack for a typo. Point at a doc only when that change needs it, and keep the doc current.

## Checks

Do not add "always run the full suite" or extra verification the model already does. Preserve existing repository gates. Never weaken a meaningful check to make an instruction shorter.

For a local suite that uses disposable fixtures and has no production access, it is enough to say: run it, fix failures caused by the requested change, and rerun the affected tests without asking at each step.
