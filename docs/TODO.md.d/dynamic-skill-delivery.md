- created: 2026-07-12
- created_by: fable-5

## Blockers
- dot.ai territory — design only while the stopgap lives.

## Questions
- Operator vision: "add a text model and send skills dynamically" — protocol?

## Findings
- Today roles are fixed in manifest.conf and delivery is static (.ai.toml). Every
  skill description costs context in every session even when the role never fires.

## Proposal
Design note only: per-role physical delivery (only the session's role's skills
visible), then dynamic push. No stopgap implementation.

## Testing
n/a — design artifact.
