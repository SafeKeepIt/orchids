- created: 2026-07-21
- created_by: fable-5
- created_during: orchestrator session (operator report)

## Blockers

- None.

## Questions

- Bus lifecycle: what releases a bus sidecar? (parent's close signal · a
  reaper · a TTL). The bus charter says it is never returned — that guarantee
  and the end-of-task guard cannot both hold.
- Who kills panes/sessions at close now the finishing hooks are retired
  (hook-choreography moved this to the bus — but nothing observed doing it)?
- Scope: charters only, or also a mechanical reaper (a teardown tool an agent
  runs at close, like architect-teardown.sh, generalised)?

## Findings

- Operator report (2026-07-21): closes get stuck because agents do not clean up
  after themselves and do not close their sub-agents — the flow cannot finish.
- Observed instances, same session: the bus sidecar is DESIGNED never to return
  ("loads exactly one, at session start, and never returns it") while the
  end-of-task guard requires "no sub-agent left in flight" — structural
  contradiction; the app-identifying architect's bus was still announcing on
  the bus AFTER its `finished` signal; MOOD records two live orchestrator-role
  sessions with nobody retiring one; an orchestrator session left running
  inside a closed feature's worktree blocks that worktree's removal.
- The architect-close.sh Stop hook was retired (bus-driven choreography,
  hook-choreography task) — pane/session teardown has no owner observed doing
  the work.

## Proposal

Make close mean CLOSED: every agent charter gets an explicit teardown
obligation — release/terminate its bus and any listening sub-agents, kill its
pane/session where it owns one, leave no worktree occupied — and the close
choreography gets a deterministic owner for teardown (charter step or reaper
tool), so no flow is left unfinishable by a lingering child. Exact mechanism
to be scoped with the operator.

## Testing

To agree when ripened — expected: after a THAT IS ALL / ALL IT IS close, no
bus, pane, session, or sub-agent of the closed feature remains alive, verified
by observation (tmux list-panes, claude agents, bus roster).
