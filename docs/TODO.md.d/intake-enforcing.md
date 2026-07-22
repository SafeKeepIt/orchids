# Intake enforcing: typed requests in, board writes denied

- created: 2026-07-22
- created_by: Sebastien Lambla

## Blockers

- None.

## Questions

- None on the WHAT — Decision-069 plus the operator's wire format rule it.
  HOW details (hook implementation for the own-sidecar carve-out, schema
  file placement) are the build's.

## Findings

- Operator ruling (2026-07-22, Decision-069): prose rules do not hold —
  "artificial intelligence is lazy" — a lazy agent will write the board
  directly whenever that looks more efficient than messaging. Live-fired
  the same day: the sidebar-polish close buried the operator's requests
  in a footnote rather than returning them.
- Wire format specified by the operator verbatim:
  **`<orchard>:<todo>:<free text>`** — colon-separated: the orchard
  (repository), the todo (task reference, empty for new intake), then the
  free-text subject.
- The board-index deny at architect spawn is already chartered (the launch
  recipe writes the worktree's settings.local.json, Decision-069); this
  build delivers the rest.

## Proposal

1. **The intake message type**: `<orchard>:<todo>:<free text>` over the bus
   (one-way, with an optional response for request/response uses), carried
   in `bus.py` with a JSON Schema alongside `message.schema.json` (the
   fleet-documenting family). Every bug/item/request an agent holds for the
   orchestrator travels this way — no other channel.
2. **The sidecar guard hook**: a PreToolUse hook (shipped settings) denying
   Edit/Write under `docs/TODO.md.d/` unless the target is the session's
   OWN feature sidecar (resolved from the worktree id) — the carve-out a
   glob deny cannot express. The board index deny at spawn stays as
   chartered.
3. Agent defs reference the message type as the ONLY intake path (the
   ledger rule of 2026-07-22 feeds it at close).

## Testing

Live: an architect attempting to edit `docs/TODO.md` or a foreign sidecar
is DENIED by permission/hook (observed, not trusted); its own sidecar still
writes; an intake message in the wire format arrives at the orchestrator
and validates against its schema; a malformed one is rejected loudly.
