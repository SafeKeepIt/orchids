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
- ~~Which live-fire defects are in this corrective's scope?~~ RULED (operator,
  2026-07-21, scope round): IN — (1) teardown pane handle: re-key
  `architect-teardown.sh` and reaping off the clobbered `arch:<id>` pane title
  onto a stable handle (e.g. a tmux window user-option) — this task OWNS the
  stable-handle mechanism; the parallel sidebar-fixes corrective consumes it
  for its mount-idempotency defect, so define the handle as a small stable
  contract (name it in your plan); (2) bus wake/monitor
  teardown: the bus never wakes, never tears its monitor down, the monitor
  stays up and the architect never closes — deliver the active-wake mechanics
  (Decision-046) so closes wake the bus and the bus verifiably kills its
  watcher before departing; (3) premature bus release: charter pins release to
  the parent's close only, never an errand's end. OUT (explicit voluntary
  deferral): the `_closed`-marker-ordering tightening.
- ~~How does an operator approval reach the architect at the done gate?~~
  RULED (operator, 2026-07-21, Decision-047): a sanctioned operator relay — an
  operator-origin message class on the bus that gate-waiting agents accept;
  relayed verbatim, flagged operator-origin, never peer traffic. Mechanics are
  in scope for this corrective.

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
- Live-fire evidence from the fleet-sidebar close (2026-07-21), all verified:
  - `architect-teardown.sh` matches the architect pane by pane TITLE `arch:<id>`,
    which claude clobbers live with the session name — teardown finds no pane and
    neither returns focus nor closes it. Fix: match a reliable handle (window
    name, or a tmux window user-option), not the clobbered pane title. The same
    clobbering breaks reaping's pane-title check.
  - A bus blocked on its monitor never exits on its own: it must be WOKEN by an
    inbound message and tear its monitor down itself; killing the monitor
    externally leaves the bus asleep forever (Decision-046). Passive
    watch-and-wait makes closes take tens of minutes; closes must wake actively.
  - The native `--worktree` launcher (wrapper claude process) outlives its child
    architect and holds a blank window until reaped.
  - The architect never touched its stream's `_closed` marker before teardown
    (protocol orders it first); ingestion proceeded without it.
  - An operator approval given in the ORCHESTRATOR pane has no sanctioned
    delivery path to the architect: the bus relay is (correctly) rejected as
    peer traffic, and the flow silently stalls at the done gate until the
    operator types in the architect's own window (or keystrokes are injected).
  - One session's bus released itself after completing a relay errand, mid-parent-
    session — release belongs to the parent's close, not an errand's end.

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
