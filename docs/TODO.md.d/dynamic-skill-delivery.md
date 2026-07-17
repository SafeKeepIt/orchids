- created: 2026-07-12
- created_by: fable-5

## Blockers
- dot.ai territory — design only while the stopgap lives.

## Questions
- Operator vision: "add a text model and send skills dynamically" — protocol?

## Findings
- Today roles are fixed in manifest.conf and delivery is static (.ai.toml). Every
  skill description costs context in every session even when the role never fires.
- 2026-07-17: this task's FIRST half is now live work, not a design note — see
  `role-delivery` and Decision-002/003. Per-role physical delivery is being built:
  authors declare a task-oriented role DAG in frontmatter, kauk filters at install.
  Measured cost of the problem: 10,190 bytes of `description` across 26 skills, every
  session, every repo.
- 2026-07-17: the framing above ("roles are fixed in manifest.conf") is superseded —
  roles move OUT of manifest.conf into the definitions, because authors know what their
  skill is for. Also corrected: delivery was never merely "static", it was inert — the
  role field filters nothing today (kauk `resolve_mode`, `bin/kauk:41-56`).

## Proposal
What remains here is only the SECOND half: dynamic push (a text model selecting and
sending skills at runtime). The per-role physical-delivery half has moved to
`role-delivery`. Still design-only, still dot.ai territory.

## Testing
n/a — design artifact.
