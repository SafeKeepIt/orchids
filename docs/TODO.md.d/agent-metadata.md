- created: 2026-07-19
- created_by: fable-5
- created_during: f/status-channel
- completed: 2026-07-21
- completed_during: f/hook-choreography

## Blockers

- ~~Lands after [[message-bus]] merges.~~ Merged; built on it.

## Questions

- ~~Which wins when identity-at-birth and status-at-time disagree?~~ Resolved
  (Decision-028): mutable fields (model, effort) ride `orchid:status` ONLY — status is
  the live truth, identity the birth record. No tiebreak needed once they never carry
  the same mutable field.
- ~~Denominators: where do context-window size and the rate card come from?~~
  Voluntary deferral: not shipped with the fold. Token classes stay broken out so both
  consumers keep their own arithmetic; a denominator source can ride a later status
  extension if wanted.

## Findings

- Token count has TWO consumers with different needs: the agent (context occupancy — am I
  running out of room?) and the operator (money). They bill differently, so a single sum
  cannot yield cost — the classes have to stay broken out.
- Folded into [[hook-choreography]] (2026-07-21): `orchid:status` now carries model +
  effort alongside the broken-out token classes; effort reads null until an env source
  exists.

## Proposal

Add model, effort and the token denominators to agent metadata on the bus, with an explicit
rule for which source wins when the announcement and the live state disagree.

## Testing

~~To agree when ripened.~~ Covered by hook-choreography's integration run: status
verified carrying model=claude-opus-4-8 / effort=null.
