# <project-name> — project rules

Project-specific agent rules. Shared rules: `AGENTS.shared.md` (immutable). File formats:
`AGENTS.files.md`. Taxonomy: `ARCHITECTURE.md`.

## What this is

<One paragraph: what the project is, what it produces, where to read more (README.md).>

## Ground truth to reuse (do NOT re-derive)

<Solved problems the agent must reuse instead of re-investigating — files, patches,
reference implementations. Delete the section if none yet.>

## Hard constraints

<Non-negotiables specific to this project: secrets handling, forbidden operations,
security posture. Delete the section if none yet.>

## Conventions

- Follow the file registry in `AGENTS.shared.md` (docs/TODO.md + sidecars,
  docs/decisions.md, CHANGELOG.md, ARCHITECTURE.md). `main` is immutable; work on
  `f/<id>` branches; close per the `workflow-complete` skill.
- <Project overrides of shared skills go here — e.g. commit-trailer format, test rig.>
