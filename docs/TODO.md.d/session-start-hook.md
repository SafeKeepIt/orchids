- created: 2026-07-12
- created_by: fable-5

## Blockers
- none

## Questions
- Is the static CLAUDE.md prefix (shipped) enough, or add a SessionStart hook that
  re-creates/repairs the prefix and injects "read the AGENTS files first"?

## Findings
- init writes the orchids:begin prefix (@AGENTS.shared.md, @AGENTS.md; files.md at
  close only). A hook would self-heal deletion/drift; operator is hook-skeptical.

## Proposal
Ship nothing yet; decide after the prefix has run in anger across repos.

## Testing
Delete the prefix in a scratch repo; observe whether the failure is noticed.
