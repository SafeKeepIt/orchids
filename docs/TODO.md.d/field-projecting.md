- created: 2026-07-21
- created_by: Sebastien Lambla

## Blockers

- None.

## Questions

- ~~**Labels overlap**: does the "labels" bullet drop as already-done (the
  tags-and-labels build shipped the full label vocabulary, Decision-035), or
  does it mean something additional?~~ RULED (operator, 2026-07-22): neither —
  the scope is the **sidecar fields generally**: every field the sidecar/board
  badge carries projects to GitHub. Where a GitHub field exists it MAPS; where
  none exists it is CREATED. The shipped label projection stands untouched.

## Findings

- Operator sizing note (2026-07-21): very mechanical work — mapping badge fields
  the board already carries onto GitHub fields GitHub already supports, inside
  the existing board→GitHub sync.
- 2026-07-22 recheck: nested-tasks-projecting's indentation fix (commit
  495a48d) is orthogonal to this task — it fixed line-parsing, not field
  content; no overlap there.
- 2026-07-22 recheck: `project_sync` in `tools/board_gh.py` already syncs
  Status, Urgency, Readiness, Component as GitHub Project custom fields — no
  Priority or Type field exists yet, and no relationship (blocked-by/blocking)
  sync exists.

## Proposal

The ruling (operator, 2026-07-22): **every field the sidecar/board badge
carries projects to GitHub — map it to an existing GitHub field where one
exists, create the field where none does.** The sync leaves no board field
unmirrored. Applied to today's inventory:

- **priority** — from the badge's urgency (critical / normal / nice-to-have /
  idea): map to GitHub's native priority representation if the project schema
  offers one, else create the field;
- **type** — from the badge's type (bug / feature / refactor / housekeeping /
  completion): map to GitHub's native issue type where available, else create;
- **relationships** — blocked-by AND blocking, from the board's ⊘ edges
  (blocking is the reverse direction of a blocked-by edge);
- **any remaining badge/sidecar field without a GitHub counterpart** — the
  field is created and synced (Status, Urgency, Readiness, Component already
  exist as created project fields; the same mechanism extends to whatever the
  badge carries next).

Already shipped and untouched: the label vocabulary projection
(tags-and-labels, Decision-035). Parent/child sub-issue nesting stays with
[[nested-tasks-projecting]].

Expectation set by the operator: on the next synchronization after this lands,
every mirrored issue carries exactly the same values as the board.

## Testing

One live synchronization, then verify on a sample covering each case — an issue
with urgency set, one with ⊘ edges in both directions, one with tags — that
priority, type, both relationship directions, and labels equal the board's
values exactly; and that a badge field with no native GitHub counterpart shows
up as a created project field carrying the board's value.
