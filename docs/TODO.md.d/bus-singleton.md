# Bus singleton: exactly one bus sidecar per agent, as designed

- created: 2026-07-22
- created_by: Sebastien Lambla

## Blockers

- None.

## Questions

- None on the WHAT — Decision-051 rules it: the bus sidecar is a singleton
  PER AGENT. Every agent loads exactly one; duplicates and orphans are the
  defect. The HOW of enforcement (spawn guard, liveness-keyed reaping) is
  the build's to design and present.

## Findings

- The per-agent architecture (Decision-041) IS the design. The observed
  defect is multiplicity beyond it: the 2026-07-22 orchestrator session
  ran TWO bus sidecars at once (a second spawned by mistake for a
  broadcast instead of messaging the existing one), and stale bus
  entries survive their dead agents and keep rendering in the sidebar.
- Touches: `agents/bus.md` (self-guard: refuse to load if the parent
  already has a live bus), `hooks/bus-init.sh`/`bus-end.sh`, `tools/bus.py`
  (announce/registry hygiene), and stray-reaping at orchestrator hygiene
  passes. The gate-word relay and lifecycle choreography (Decisions
  041/047/048/049) must be preserved exactly.

## Proposal

Enforce the one-bus-per-agent invariant end to end: an agent asking to load
a bus when it already has a live one gets its EXISTING bus (no second
spawn); a bus whose parent session is gone is reaped promptly and its
registry/state entries cleared; the sidebar consequently shows exactly one
bus row per live agent, none for the dead (rendering handled by
[[sidebar-polish]] item 5).

## Testing

Provoke the two failure modes and observe them handled: (1) a parent
requests a second bus — the request lands on the existing sidecar, no new
instance appears; (2) kill an agent — its bus and registry entries are
gone after the reap, and the sidebar shows exactly one bus row per live
agent throughout.
