- created: 2026-07-21
- created_by: fable-5
- created_during: orchestrator session (operator report)

## Blockers

- None.

## Questions

- ~~Bus lifecycle: what releases a bus sidecar?~~ RULED (operator, 2026-07-21,
  Decision-041): parent release at close PLUS the bus self-exits when its
  parent is gone (the inbox watch doubles as the liveness monitor).
- ~~Who kills panes/sessions at close?~~ RULED (operator, 2026-07-21,
  Decision-041): the CLOSING AGENT kills itself — self-teardown is the last
  charter step; the orchestrator reaps only an agent that died first.
- ~~Charter text or mechanical enforcement?~~ RULED (operator, 2026-07-21,
  Decision-041): charters only — no verification apparatus, no reaper pass.

## Findings

- Operator report (2026-07-21): closes get stuck because agents do not clean up
  after themselves and do not close their sub-agents — the flow cannot finish.
- Observed instances, same session: the bus charter guaranteed it never returns
  while the end-of-task guard required no sub-agent in flight (structural
  contradiction); an architect's bus still announcing after its `finished`
  signal; two live orchestrator-role sessions with nobody retiring one.
- Delivered (2026-07-21, orchestrator on main): Decision-041 recorded; bus
  charter gains the Release section (released ⇒ depart + end; orphaned ⇒ end);
  architect charter gains self-teardown (release bus + architect-teardown.sh as
  final act, also on blocked/abandoned); orchestrator charter drops the
  teardown act, keeps it only as dead-agent fallback, and releases its own bus
  at retirement; handover guard counts a released bus as returned and the
  stream close gains a teardown step.

## Proposal

Make close mean CLOSED, by charter text alone (Decision-041): a bus is released
at close or self-exits when orphaned; the closing agent's last act is its own
teardown (bus, pane, session); parents reap only the dead. Delivered as charter
amendments — see Findings.

## Testing

First live release (2026-07-21, this orchestrator's own bus): the agent
released and departed cleanly, but its armed Monitor — the persistent
inotify watch on the inbox — OUTLIVED it, visible to the operator as an
open watcher on a sleeping session; a second zombie watcher from an
already-dead session was found beside it. Both killed by hand. The bus
charter now orders: stop the Monitor and VERIFY the watcher process is gone
before departing, on both the release and the orphan paths.

Agreed shape (pending its live run): the NEXT feature close is the test —
after `THAT IS ALL` / `ALL IT IS`, observe that no bus, pane, session, or
sub-agent of the closed feature remains (tmux list-panes, bus roster). Until
that observation, this stays open.
