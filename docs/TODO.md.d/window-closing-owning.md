# Window closing owning: agents close themselves; a listener kills at five

- created: 2026-07-22
- created_by: Sebastien Lambla

## Blockers

- None.

## Questions

- None on the WHAT — Decision-068 rules it fully. HOW (which agent is the
  designated bus-listening killer — the orchestrator's own supervision or a
  dedicated listener — and how the sidebar-polish build's shipped-but-
  untested exit-grace code is reused) is the build's to present.

## Findings

- Operator causality finding (2026-07-22): windows failed to close because
  the HOUSEKEEPER deleted worktree files under agents still mid-teardown —
  the floor vanished beneath the closing agent. The housekeeper charter now
  carries the hard precondition (never remove before on-closed); this task
  builds the mechanism proper.
- The sidebar-polish build already shipped exit-grace lifecycle code
  (evict-on-terminal-signal, grace tracking) — explicitly NOT live-tested,
  and recorded with a 10s default that Decision-068 corrects to FIVE
  seconds.

## Proposal

Per Decision-068: an agent closes its OWN window whenever it is ready,
broadcasting `on-closing` then `on-closed`; five seconds after `on-closing`
without an `on-closed`, ONE designated bus-listening agent kills the
process/window and broadcasts the death on its behalf (an agent may request
longer grace at announce time). The housekeeper's worktree removal waits on
`on-closed`/kill-broadcast, already chartered. Sidebar eviction consumes the
same signals (already built).

## Testing

Live: a well-behaved agent closes cleanly inside five seconds — both
broadcasts observed, window gone, worktree removal proceeds only after
on-closed. A deliberately-hung agent is killed at five seconds, the death
broadcast lands, its sidebar row evicts, and the close completes. The
sidebar-polish build's untested exit-grace path gets its live pass here.
