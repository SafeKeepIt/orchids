- created: 2026-07-12
- created_by: fable-5

## Blockers
- none

## Questions
- none

## Findings
- readme-sync trigger has fired (user-facing tool exists); no README/ARCHITECTURE/
  CHANGELOG/decisions in orchids yet; session rulings live only in chat + git log.

## Proposal
Write the registry set: README (readme-sync voice, install.txt is the agent path),
docs/decisions.md seeded with this session's rulings (.git-channel handover, .ai.toml
modes, fixed roles, owin.org), CHANGELOG, ARCHITECTURE (one page).

## Testing
readme-sync checklist passes; decisions greppable by #keyword.
