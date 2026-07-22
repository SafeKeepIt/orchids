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
- Boundary with the parallel agent-closing corrective: the STABLE WINDOW
  HANDLE mechanism (replacing the live-clobbered `arch:<id>` pane title) is
  OWNED by agent-closing, running in parallel. For the mount-idempotency
  defect (inventory #5), consume that handle contract — do not invent a
  second one. If it has not landed when you reach #5, adopt the same contract
  shape (a tmux window user-option) and surface the coordination to the
  operator rather than diverging.

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

## Result

- outcome: **done** (built, tested; awaiting operator `THAT IS ALL`)
- branch `f/sidebar-fixes` · HEAD `13bf72b` · Base `8203b6f` (🎉 anchor `4253520`)
- commits: delivery/mount (🎉) · nav collision · four model/render defects ·
  terminal-flash fix

### What was fixed (all IN-scope items delivered)

- **Root cause of "no sidebar at all"** (new, not in the numbered inventory): both mount
  callers invoke `.claude/tools/sidebar-mount.sh`, which did not exist — the four sidebar
  tools were merged only under `tools/`, never delivered into `.claude/tools/` like every
  other tool, so each mount exited 127. Fixed by delivering the four files as
  `.claude/tools/` symlinks (kauk `link`, matching the existing 5), resolving the mount
  script's dir through the symlink (`readlink -f`), and surfacing a startup failure instead
  of a silently-vanishing pane.
- **#1 nav collision**: `resolve_window()` now prefers, among duplicate-name windows, one
  whose active pane is a real process over a bare login shell (the blank `--worktree`
  launcher leftover); falls back to first-match. Duplicate-name tests added.
- **#2 sticky waiting flash**: the flash is changed only by an activity broadcast (not
  cleared by a re-announce or plain lifecycle signal), and is cleared by a terminal
  lifecycle (finished/abandoned) so a completed row does not keep flashing.
- **#3 `_seen_ids`**: bounded to messages still on disk each scan (no unbounded growth in a
  long-lived `watch()`).
- **#4 idle status**: a repo with no orchestrator session renders a distinct idle glyph
  (⚪, dim) instead of the same green "running" dot as a busy repo.
- **#6 announced name**: the sidebar consumes the announced `arch.name` rather than
  re-deriving `feature_id.replace("-"," ")`; derives only as fallback.
- **#5 mount idempotency**: keyed on `pane_start_command` (running `sidebar.py`) instead of
  the clobber-prone pane title. **Operator decision (this session)**: implemented
  self-contained (a pane-presence concern), NOT consuming agent-closing's window-identity
  handle, which had not landed (that corrective was still planning its contract).

### Tested (agreed method: unit suite green + live visual pass)

- Unit: `python3 -m unittest discover -s tests` → **31/31 OK** (pre-existing baseline was
  22, not the sidecar's stale "23/23"; +9 new tests covering every fix).
- Live pass, self-driven through the REAL reader→model→renderer and REAL tmux:
  - sidebar mounts and renders in a throwaway tmux session; a second mount is idempotent
    (one sidebar pane).
  - `resolve_window` lands on the live window when two windows share a name.
  - synthetic bus traffic renders ⚪ idle repo, feature labelled by its announced name,
    waiting flash sticky then cleared by a new activity, finished row showing ✅ (no flash).
  - Remaining for the operator's own eyes in the live fleet (post-merge + `kauk sync`,
    since the delivered symlinks track the vendored clone): the flash animation over time
    and keyboard Enter switching the client to the target window.

### Spawned / deferred

- **Deferred to agent-closing / orchestrator**: the environmental SOURCE of the blank
  duplicate window (native `claude --worktree` launcher/wrapper leaving a blank same-named
  window; stale-window reaping). Nav is now collision-SAFE; eliminating the duplicate at
  source belongs with the stable-window-handle work, not this corrective.

## Changelog entry

### Fixed
- The fleet sidebar now actually appears: it was never delivered into `.claude/tools/`, so
  every mount attempt failed silently and no sidebar showed. The four sidebar tools are now
  delivered like every other tool.
- Selecting a sidebar row no longer lands on a blank leftover window when two windows share
  a name — navigation prefers the live one.
- The "waiting on operator" flash no longer stops early when an unrelated message arrives,
  and no longer keeps flashing after a job has finished.
- A repo with no active orchestrator now shows a distinct idle marker instead of a green
  "running" dot.
- A feature row is labelled from the name the agent announced, not a second re-derivation
  that could drift from it.
- Re-mounting the sidebar no longer risks a second sidebar pane when the pane title has been
  changed by a status-glyph setter.

## Readme delta

- No change needed (evidenced). README already states the sidebar "mounts automatically as a
  pinned left pane" (README.md:42) and documents `ORCHIDS_SIDEBAR_REPOS` /
  `sidebar-repos` (README.md:50); this corrective restores that documented behaviour and
  introduces no new flags, usage, or config.

## Architecture determination

- No `ARCHITECTURE.md` edit required (evidenced). No trigger fired: no component
  added/removed/repurposed, no boundary/responsibility change, no data-flow/wiring change,
  no style change. The `.claude/tools/` delivery was ALREADY documented as intended at
  ARCHITECTURE.md:172 (`sidebar-mount.sh (→ .claude/tools/)`); this corrective makes the
  code match that doc. The component diagram (ARCHITECTURE.md:105-107) and responsibilities
  (126-127) remain accurate. All edits are internal behaviour within the existing sidebar
  components plus the missing delivery symlinks.
