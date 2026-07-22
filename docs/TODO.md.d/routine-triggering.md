- created: 2026-07-21
- created_by: fable-5
- created_during: f/app-identifying

## Blockers

- Research-preview dependency: Anthropic Routines (cloud agents) are
  research-preview; API/behaviour may shift.

## Questions

- To scope when picked up.

## Findings

- Routines act as the USER's account and cannot own a bot identity
  (Decision-039) — they can never BE the cloud path's actor, only trigger it.

## Proposal

A Routine as an NL-trigger/bloomer layer: on natural-language policy ("a
feature with a spec appeared — bloom it; if uncontroversial, open the flow"),
it dispatches the GitHub Actions cloud-path workflow, which then runs as
callabloom[bot].

## Testing

To agree when bloomed.
