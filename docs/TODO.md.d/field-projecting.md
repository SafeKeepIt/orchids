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

Frozen plan, agreed with the operator 2026-07-22 (recorded as Decision-051 —
see there for the full rationale and the live-schema evidence gathered
during discovery):

- **type** — set GitHub's **native Issue Type** (`updateIssueIssueType`) for
  all five board types (bug/feature/refactor/housekeeping/completion). The
  org (`kaukea`) already has native types Bug and Feature; the missing three
  (Refactor, Housekeeping, Completion) are created org-wide via
  `createIssueType`, idempotent ensure-if-missing. The existing emoji label
  projection for type (Decision-035) is untouched and stays live alongside.
- **priority** — set GitHub's **native org Issue Field "Priority"**
  (`setIssueFieldValue`), sourced from board `urgency`. Mapping: `critical`→
  Urgent, empty/normal→Medium, `nice-to-have`→Low, `idea`→Low (`High` unused).
  The existing Projects-v2 "Urgency" custom field is KEPT and still written
  by `project_sync` — both stay live (operator ruling: Urgency stays
  "absolutely needed" alongside the new Priority field).
- **relationships** — board `⊘` (blocked_by) syncs to GitHub's **native Issue
  Dependencies** (`addBlockedBy`/`removeBlockedBy`), full reconciliation each
  push (add missing, remove stale), same "board is canonical" principle as
  the label sync. `blocking` needs no separate write — GitHub derives it as
  blocked_by's inverse view. `~<id>` (`related`) has **no native GitHub
  equivalent** (confirmed via GraphQL schema introspection — no
  `relatedIssues` field/mutation, and org Issue Fields don't support an
  issue-reference data type); it projects as a `### Related` body-text link
  list, the same mechanism already used for the parent/child sub-tasks list.
- Parent/child sub-issue nesting stays out of scope, already shipped via
  [[nested-tasks-projecting]] (body-text list, not GitHub's native sub-issue
  API). Label vocabulary (Decision-035) stays untouched.

**Filed as follow-up TODOs, not fixed here** (pre-existing, orthogonal bugs
found during discovery): `pull()` calls `ensure_label` (singular) but the
function is `ensure_labels` (plural) — latent `NameError`; `Component` is
written by `project_sync` without being declared in
`SELECT_FIELDS`/`TEXT_FIELDS` — works today only because it was created
out-of-band on the live GitHub Project.

**Build shape**: 3 steps inside `tools/board_gh.py`'s `project_sync` (Type,
Priority, Relationships), all via the existing `gql()` helper, no new
dependencies. Independent in logic but share one file — builders dispatch
sequentially rather than in parallel to avoid conflicting edits.

Expectation set by the operator: on the next synchronization after this
lands, every mirrored issue carries exactly the same values as the board.

## Testing

One live synchronization, then verify on a sample covering each case — an issue
with urgency set, one with ⊘ edges in both directions, one with tags — that
priority, type, both relationship directions, and labels equal the board's
values exactly; and that a badge field with no native GitHub counterpart shows
up as a created project field carrying the board's value.
