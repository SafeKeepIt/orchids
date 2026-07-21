- created: 2026-07-21
- created_by: Sebastien Lambla
- created_during: fleet-sidebar

## Blockers

- ~~fleet-sidebar's squash-merge not yet on `main` — fixes branch from the merged
  code.~~ RESOLVED: squash-merged as 430597a, archive/fleet-sidebar, 2026-07-21.

## Questions

- ~~Which defects, specifically?~~ CONFIRMED (operator, 2026-07-21, scope
  round): the audit's six defects (Findings → "Defect inventory") ARE in, plus
  the operator's own observations, which lead the list:
  - **The sidebar does not appear at all.** In the operator's live session
    there is NO sidebar — whatever the unit suite says, the mounted surface is
    absent. Reproducing and fixing the mount path in a real session is the
    first fix, because every other defect is unverifiable until the sidebar is
    visibly there.
  - **The window names are wrong.** The live windows do not carry the
    Decision-045 display forms the close claimed; the naming delivered does
    not match what the operator sees.
  - The operator states plainly: "I have no way of knowing how badly this was
    done" — the corrective's testing MUST therefore restore observability
    first (a sidebar the operator can see), then walk every fix in that live
    view.

## Findings

- The feature was closed under operator waiver: the build's own unit tests (23/23) and
  smoke passed, but the operator's review judged the implementation to carry numerous
  mistakes and issues; the close was accepted with this corrective follow-up attached
  rather than amending in-branch.
- Known limitations already recorded by the build (candidates, not the full list):
  reader dedup is cross-scan by message id; a repolist entry with no bus activity
  renders an empty repo row.
- Defect candidate from the close itself: the window-naming amend renamed windows to
  the session-naming display forms without accounting for a coexisting launcher window
  of the same feature — two windows named `orchids ▸ fleet sidebar`, one blank; the
  operator landed on the blank one. Naming must be collision-safe.

### Defect inventory (draft — operator to confirm)

Audited read-only: `tools/sidebar_model.py`, `tools/sidebar.py`, `tools/sidebar_nav.py`,
`tools/sidebar-mount.sh`, the activity-broadcast sections of `agents/orchestrator.md`,
`agents/architect.md`, `agents/ripener.md`, against the fleet-sidebar Proposal and
Decisions 043–046.

1. **`tools/sidebar_nav.py` `resolve_window()`** · picks the FIRST tmux window whose
   `#{window_name}` matches, with no tie-break · Decision-045 names windows by the
   session-naming display form (`<repo> ▸ <human>`) but does not guarantee that form is
   UNIQUE (a stale/leftover window, or two architects on the same human name, produce
   duplicates) — `resolve_window`/`navigate_to` have no way to prefer the live one, so
   selecting a row can land on a blank/stale window. This is the exact operator-observed
   incident (two windows named `orchids ▸ fleet sidebar`, landed on the blank one).
   `tests/test_sidebar_nav.py` has no test at all for a duplicate-name window list —
   the collision path is untested as well as unhandled.
2. **`tools/sidebar_model.py` `_apply_message()`** · `state.last_notify_user =
   msg.get("notify_user") is True` runs unconditionally for every applied message,
   including identity/announce and lifecycle messages that never carry `notify_user` ·
   because messages are applied in `ts` order and last-write-wins per field, ANY later
   message from the same sender that lacks `notify_user` (e.g. a re-announce, a plain
   lifecycle signal) silently clears a still-open "waiting on operator" flash — the row
   can stop flashing before the operator has actually answered. Waiting/flash should be
   sticky until resolved by a new activity broadcast or an explicit un-block, not
   reset as a side effect of an unrelated field being applied.
3. **`tools/sidebar_model.py` `_BusAggregator._seen_ids`** · grows without bound for
   the life of a `watch()` process — ids are added on every scan and never pruned, even
   though the underlying messages are ephemeral (deleted by their recipient's
   `receive`) · a long-lived sidebar process (mounted for a whole tmux session) leaks
   memory proportional to total bus traffic ever seen, not traffic in flight. Not
   critical short-term but violates the module's own "ephemeral, don't hoard" framing.
4. **`tools/sidebar_model.py` `_assemble_repo()`** · a repo with no `orchestrator`
   session found in the accumulated state (e.g. resolved via repolist but the
   orchestrator hasn't announced yet, or never will) still renders with the
   `Repo(...)` default `status="running"` and `waiting=False` · this is the "empty repo
   row" already flagged as a known limitation, but the sharper defect is the specific
   default: an inactive/unknown repo shows the same green "running" dot as a genuinely
   busy one, which is misleading rather than merely blank. Needs a distinct
   idle/unknown status + emoji, not a silent `running` default.
5. **`tools/sidebar-mount.sh`** · idempotency check matches on pane TITLE
   (`'orchid-sidebar'`) via `tmux list-panes ... | grep -qx`, but the file's own docstring
   in `sidebar_nav.py` records that pane titles get clobbered by a status-glyph setter
   observed live (`⠐ orchids ▸ fleet sidebar`) — the exact failure mode the nav module
   had to work around for navigation. The mount script never worked around it: if
   something else re-titles the sidebar pane, the idempotency check stops matching and
   a SECOND sidebar pane can be split into the same window on the next mount.
6. **`tools/sidebar.py` `flatten()` / feature target** · the feature row's navigation
   `target` is built as `f"{repo.name}{TARGET_SEPARATOR}{feature.name}"`, and
   `feature.name` in turn is derived in `sidebar_model._assemble_repo()` as
   `feature_id.replace("-", " ")` — a second, independent re-derivation of the same
   transform `bus.py`'s `identity_of()` already computed once into the announced
   `name` field (`tools/bus.py` comment: "derived once here so the sidebar ... read one
   field instead of re-deriving — Decision-032"). The sidebar ignores the announced
   `arch.name` and recomputes from `feature_id` instead, so the two are only equal by
   the two code paths happening to agree today; a future change to either transform
   diverges them silently with no test catching it.

## Proposal

Corrective only — make the delivered fleet sidebar meet its original spec
([[fleet-sidebar]] Proposal): audit the shipped implementation, enumerate the defects
(operator walk-through + code audit), fix them. No new capability, no scope growth;
anything additive discovered en route becomes its own task.

## Testing

Re-run the original agreed method with the operator's live visual pass front and
centre — flash animation, keyboard navigation landing on the right window, a row
updating when a job's window closes — since that live pass is where the issues
surfaced. Unit suite stays green.
