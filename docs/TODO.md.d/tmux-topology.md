- created: 2026-07-20
- created_by: Sebastien Lambla

## Blockers

- None hard; co-designed with [[fleet-sidebar]] (shared layout) and it reshapes the
  close choreography [[hook-choreography]] carries today.

## Questions

- ~~Does closing the architect window on completion ride the housekeeper's return
  instead of a Stop-hook countersign match?~~ Resolved by [[hook-choreography]]: the
  close rides the bus `finished` signal (Decision-028); the Stop hook is retired.
- ~~Pane lifecycle for coders: bounded how?~~ Resolved by the 2026-07-21 refinement:
  builders stack in a dedicated RIGHT COLUMN of the architect's window, capped —
  the exact cap is a build-time knob (voluntary deferral), not a scope question.

## Findings

- Operator topology ruling (2026-07-20): SESSION per repository → WINDOW per architect
  (one per active task) → stacked PANE per coder/sub-agent, each visibly showing what it
  is doing. On task completion the architect's window closes and focus returns to that
  session's orchestrator window.
- This supersedes Decision-006 (architects as panes beside the orchestrator) AT LANDING —
  record the formal supersession in `docs/decisions.md` on the implementing branch, not
  before; Decision-006 governs live behaviour until then.
- Current mechanics this replaces: `.return-window` + the architect-close Stop hook
  (see [[hook-choreography]] — the 2026-07-20 flush-race diagnosis and the /tmp leak).
- Operator refinement (2026-07-21): architects — the sessions the operator interacts
  with — are NEVER side-by-side/horizontal panes; one WINDOW each. A given architect's
  builder subagents stack in a dedicated COLUMN OF THEIR OWN on the RIGHT of that
  architect's window (vertical stack within the column, capped) — NOT appended below
  the architect (the default `split-window -v` behaviour, unusable today).
- [[hook-choreography]] landed the bus-driven close (Decision-028); its teardown kills
  the `arch:<id>` pane by TITLE (window closes if it was the last pane), so the close
  choreography survives this task's window-per-architect move unchanged.

## Proposal

Rework spawn/return choreography to the session/window/pane topology: architect spawns
create titled windows; builder/coder dispatches split stacked panes in that window; the
completion path (post-housekeeper) closes the window and selects the orchestrator window.
Design together with [[fleet-sidebar]]; absorb or close [[hook-choreography]] with it.

## Testing

One repo session with two architect windows, one dispatching two coders: panes stack and
are readable; completing one task closes only its window and lands focus on the
orchestrator; the other architect is undisturbed.
