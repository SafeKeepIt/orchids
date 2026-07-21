- created: 2026-07-21
- created_by: fable-5
- created_during: f/app-identifying

## Blockers

- None.

## Questions

- Code-owners file scope: whole repo, or `main`-merge only? To scope when picked up.

## Findings

- Ruleset 19333120 is DELETED; org-level rulesets need a GitHub Team plan
  (kaukea is Free); the only live rule is the minimal "Baseline" ruleset
  (deletion, non_fast_forward, required_linear_history; no bypass actors).
- The status-check/bypass-actor contraption is retired (Decision-040).

## Proposal

Formalise the workflow's EXISTING close rules as code: require operator /
code-owner approval to merge `main`, with callabloom excepted so its serialized
merge is not itself blocked. NOT a status-check or bypass contraption — this
encodes the rules the close already follows, for GitHub and the local
interactive close alike.

## Testing

To agree when ripened — expected: an unapproved PR to main cannot merge; a
callabloom merge after operator approval passes.
