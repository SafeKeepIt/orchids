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

- `repository: orchids` — the branching model this repo follows. `orchids` (the
  default; missing or empty counts as it) is the canonical workflow shape and makes
  the repo eligible for `history-rewrite` migration. Any other value (e.g.
  `repository: gitflow`) means the repo keeps its own model — agents must not
  restructure its history.
- Follow the file registry in `AGENTS.shared.md` (docs/TODO.md + sidecars,
  docs/decisions.md, CHANGELOG.md, ARCHITECTURE.md). `main` is immutable; work on
  `f/<id>` branches; close per the `workflow-complete` skill.
- <Project overrides of shared skills go here — e.g. commit-trailer format, test rig.>
