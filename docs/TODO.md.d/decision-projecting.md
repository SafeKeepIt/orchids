- created: 2026-07-21
- created_by: Sebastien Lambla

## Blockers

- None.

## Questions

- None open — the concrete field mapping (issue type name, close reasons) is
  read from what GitHub currently offers at build time; the operator's rule is
  to duplicate the decisions file's existing semantics with the fields
  available, nothing new.

## Findings

## Proposal

Decisions (docs/decisions.md entries) synchronize to the GitHub task board the
same way tasks do, with a DIFFERENT type than tasks so they can be referenced
correctly from issues and from each other.

Lifecycle mirrors exactly what the decisions file already does, using the
fields GitHub currently has:

- each decision becomes a mirrored item of its own type, referenceable by
  number/link;
- a SUPERSEDED decision closes on GitHub, pointing at the decision that
  replaces it (the file's strike + superseded-by marker, projected);
- a decision considered a DUPLICATE closes as a duplicate;
- task issues close as they do today — the closing conventions apply to both
  issues and decisions.

No new vocabulary, no new lifecycle states: project the existing semantics
onto GitHub's available fields, nothing more.

## Testing

One live synchronization against the current decisions file: every decision
appears with the decision type and is referenceable; a superseded decision
(e.g. one carrying a strike + superseded-by marker) shows closed with its
replacement referenced; a live decision shows open. Duplicate-closing verified
on a crafted duplicate or the first real one.
