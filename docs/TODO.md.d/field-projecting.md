- created: 2026-07-21
- created_by: Sebastien Lambla

## Blockers

- None.

## Questions

- None open — value mappings (priority scale options, issue-type names) are read
  from or created in the GitHub schema at build time; no operator answer needed.

## Findings

- Operator sizing note (2026-07-21): very mechanical work — mapping badge fields
  the board already carries onto GitHub fields GitHub already supports, inside
  the existing board→GitHub sync.

## Proposal

GitHub supports native fields the board already carries; the mirror leaves them
empty today. Fill them at synchronization so the GitHub view shows exactly the
board's values:

- **priority** — from the badge's urgency (critical / normal / nice-to-have /
  idea);
- **type** — from the badge's type (bug / feature / refactor / housekeeping /
  completion);
- **relationships** — blocked-by AND blocking, from the board's ⊘ edges
  (blocking is the reverse direction of a blocked-by edge);
- **labels** — the additional labels of the tag/label vocabulary the board
  already carries (Decision-035).

Expectation set by the operator: on the next synchronization after this lands,
every mirrored issue carries exactly the same values as the board. Parent/child
sub-issue nesting stays with [[nested-tasks-projecting]]; the label vocabulary
itself stays with [[tags-and-labels]] — this task only projects what exists.

## Testing

One live synchronization, then verify on a sample covering each case — an issue
with urgency set, one with ⊘ edges in both directions, one with tags — that
priority, type, both relationship directions, and labels equal the board's
values exactly.
