# Sync ingest failing: board-sync's GitHub→board direction exits 1

- created: 2026-07-22
- created_by: Sebastien Lambla

## Blockers

- None.

## Questions

- None yet — first the checker's reproduce (see Findings on log loss).

## Findings

- Two failures observed, both `issues`-event-triggered `board-sync` runs, both
  in the "Ingest GitHub-born changes into the board" step (exit 1):
  run 29831369050 (2026-07-21T12:44Z, issue "Testing, do not act on it") and
  run 29802639504 (2026-07-21T04:57Z, issue "Session and feature naming…").
  The push direction (board→issues) succeeds consistently in the same window.
- Step logs were no longer retrievable via `gh run view --log` at intake time
  (empty output) — the defect needs a live reproduce (open/edit a test issue)
  rather than log archaeology.
- Run annotations show two deprecations (Node 20 forced to 24 on
  actions/checkout@v4; `app-id` deprecated in favour of `client-id` on the
  callabloom token mint) — noted, not established as the cause.

## Proposal

Make the ingest direction survive issue events again: reproduce with a test
issue, find why the ingest step exits 1, fix it, and leave the sync
green-on-both-directions. Fold in the two cheap deprecation cleanups if they
prove related (or record them as separate follow-ups if not).

## Testing

A live issues-triggered run (open + edit a test issue) completes green in
both directions; the test issue's change lands on the board.
